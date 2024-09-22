document.addEventListener('DOMContentLoaded', function() {
    const reportControls = document.getElementById('report-controls');
    const salesReportContainer = document.getElementById('sales-report-container');
    const returnsReportContainer = document.getElementById('returns-report-container');
    const reportTitle = document.getElementById('report-title');
    const customPeriodButton = document.getElementById('custom-period-button');
    const customPeriodModal = new bootstrap.Modal(document.getElementById('customPeriodModal'));
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const applyCustomPeriodButton = document.getElementById('apply-custom-period');
    const salesChartContainer = document.getElementById('sales-chart');
    const returnsChartContainer = document.getElementById('returns-chart');
    const salesSummaryContainer = document.getElementById('sales-summary-container');
    const returnsSummaryContainer = document.getElementById('returns-summary-container');
    const netSummaryContainer = document.getElementById('net-summary-container');
    const stockButton = document.getElementById('stock-button');

    let salesChart;
    let returnsChart;

    // Инициализация календаря для выбора дат
    $(startDateInput).datepicker({
        dateFormat: 'dd-mm-yy',
        maxDate: new Date(),
        onSelect: function(selectedDate) {
            $(endDateInput).datepicker('option', 'minDate', selectedDate);
        }
    });

    $(endDateInput).datepicker({
        dateFormat: 'dd-mm-yy',
        maxDate: new Date(),
        onSelect: function(selectedDate) {
            $(startDateInput).datepicker('option', 'maxDate', selectedDate);
        }
    });

    // Обработчик клика на кнопку календаря
    customPeriodButton.addEventListener('click', function() {
        customPeriodModal.show(); // Открываем модальное окно
    });

    function initializeCharts() {
        salesChart = echarts.init(salesChartContainer);
        returnsChart = echarts.init(returnsChartContainer);

        // Устанавливаем заголовок при первоначальной загрузке
        const today = new Date();
        updateReportTitle('today', formatDate(today), formatDate(today));
    }

    function resetCharts() {
        if (salesChart) salesChart.clear();
        if (returnsChart) returnsChart.clear();
        salesChartContainer.parentElement.style.display = 'none'; // Скрываем контейнер графика продаж
        returnsChartContainer.parentElement.style.display = 'none'; // Скрываем контейнер графика возвратов
    }

    let socket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/reports/`);

        socket.onopen = function() {
            socket.send(JSON.stringify({ type: 'get_initial_data' }));
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if (data.event === 'report_data') {
                const salesData = data.sales_data.sales || null;
                const returnsData = data.sales_data.returns || null;
                const netData = data.sales_data.net || null;

                salesChart.hideLoading();  // Скрываем индикатор загрузки
                returnsChart.hideLoading();  // Скрываем индикатор загрузки
                // resetCharts(); // Не сбрасываем графики здесь

                updateSalesReport(salesData, returnsData, netData);
                updateCharts(salesData, returnsData);
            } else if (data.event === 'stock_data') {
                const stockData = data.stock_data;
                resetCharts(); // Скрываем графики
                updateStockReport(stockData);
            }
        };

        socket.onclose = function(e) {
            setTimeout(connectWebSocket, 1000);
        };

        socket.onerror = function(e) {
            console.error('Ошибка WebSocket:', e);
        };
    }

    connectWebSocket();

    applyCustomPeriodButton.addEventListener('click', function() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        if (startDate && endDate) {
            salesChart.showLoading();  // Показываем индикатор загрузки для графика продаж
            returnsChart.showLoading();  // Показываем индикатор загрузки для графика возвратов

            // Обновляем стили кнопок для выделения кастомного периода
            document.querySelectorAll('.report-period-button').forEach(button => {
                button.classList.remove('btn-primary', 'active');
                button.classList.add('btn-secondary');
            });

            customPeriodButton.classList.remove('btn-secondary');
            customPeriodButton.classList.add('btn-primary', 'active');

            // Убираем активное состояние с кнопки Остатки
            stockButton.classList.remove('btn-primary', 'active');
            stockButton.classList.add('btn-secondary');

            updateReportTitle('custom', startDate, endDate);
            socket.send(JSON.stringify({
                type: 'update_period',
                period: 'custom',
                start_date: startDate,
                end_date: endDate
            }));
            customPeriodModal.hide();
        }
    });

    function updateSalesReport(salesData, returnsData, netData) {
        // Очистка контейнеров
        salesSummaryContainer.innerHTML = '';
        returnsSummaryContainer.innerHTML = '';
        netSummaryContainer.innerHTML = '';
        salesReportContainer.innerHTML = '';
        returnsReportContainer.innerHTML = '';

        // Проверяем наличие данных по продажам и сортируем их по количеству продаж
        if (salesData && Object.keys(salesData).length > 1) {
            const sortedSalesData = Object.entries(salesData)
                .filter(([key]) => key !== 'total')
                .sort(([, a], [, b]) => b.total_quantity - a.total_quantity);

            // Обновляем заголовок с общей информацией по продажам
            const salesSummary = document.createElement('div');
            salesSummary.innerHTML = `
                <h4>Итого продано: ${salesData.total.total_quantity} шт</h4>
                <h4>Общая сумма продаж: ${Math.floor(salesData.total.total_sales_sum)} грн</h4>
                <h5>за наличные: ${Math.floor(salesData.total.cash_sales)} грн</h5>
                <h5>по безналу: ${Math.floor(salesData.total.non_cash_sales)} грн</h5>
            `;
            salesSummaryContainer.appendChild(salesSummary);

            const salesTitle = document.createElement('h3');
            salesTitle.textContent = 'Продажи';
            salesReportContainer.appendChild(salesTitle);

            // Генерация таблицы с информацией о продажах по продуктам и модификациям
            sortedSalesData.forEach(([productSku, product]) => {
                const sortedModifications = Object.entries(product.modifications)
                    .sort(([, a], [, b]) => b.quantity - a.quantity);

                const table = document.createElement('table');
                table.classList.add('table', 'table-striped', 'table-bordered', 'mb-4');

                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th colspan="3">
                            <div class="d-flex align-items-center">
                                ${product.collage_image_url ? `<img src="${product.collage_image_url}" alt="${product.product_title}" style="max-width: 25px;" class="me-2">` : ''}
                                <span>${product.product_title} (${productSku}) продано ${product.total_quantity} шт</span>
                            </div>
                        </th>
                    </tr>
                    <tr>
                        <th>Изображение</th>
                        <th>Товар</th>
                        <th>Количество проданного</th>
                    </tr>
                `;
                table.appendChild(thead);

                const tbody = document.createElement('tbody');

                sortedModifications.forEach(([modSku, mod]) => {
                    const modRow = document.createElement('tr');
                    const modThumbnailCell = document.createElement('td');
                    const modSkuCell = document.createElement('td');
                    const modQuantityCell = document.createElement('td');

                    if (mod.thumbnail_url) {
                        const modThumbnailImage = document.createElement('img');
                        modThumbnailImage.src = mod.thumbnail_url;
                        modThumbnailImage.alt = modSku;
                        modThumbnailImage.style.maxWidth = '35px';
                        modThumbnailCell.appendChild(modThumbnailImage);
                    } else {
                        modThumbnailCell.textContent = 'Нет изображения';
                    }

                    modSkuCell.textContent = modSku;
                    modQuantityCell.textContent = `${mod.quantity} шт`;

                    modRow.appendChild(modThumbnailCell);
                    modRow.appendChild(modSkuCell);
                    modRow.appendChild(modQuantityCell);
                    tbody.appendChild(modRow);
                });

                table.appendChild(tbody);
                salesReportContainer.appendChild(table);
            });
        } else {
            const noSalesMessage = document.createElement('h3');
            noSalesMessage.textContent = 'Продаж нет';
            salesReportContainer.appendChild(noSalesMessage);
        }

        // Обработка данных по возвратам
        if (returnsData && Object.keys(returnsData).length > 1) {
            const sortedReturnsData = Object.entries(returnsData)
                .filter(([key]) => key !== 'total')
                .sort(([, a], [, b]) => b.total_quantity - a.total_quantity);

            const returnsSummary = document.createElement('div');
            returnsSummary.innerHTML = `
                <h5>Итого возвращено: ${returnsData.total.total_quantity} шт</h5>
                <h5>Общая сумма возвратов: ${Math.floor(returnsData.total.total_sales_sum)} грн</h5>
            `;
            returnsSummaryContainer.appendChild(returnsSummary);

            const returnsTitle = document.createElement('h3');
            returnsTitle.textContent = 'Возвраты';
            returnsReportContainer.appendChild(returnsTitle);

            sortedReturnsData.forEach(([productSku, product]) => {
                const sortedModifications = Object.entries(product.modifications)
                    .sort(([, a], [, b]) => b.quantity - a.quantity);

                const table = document.createElement('table');
                table.classList.add('table', 'table-striped', 'table-bordered', 'mb-4');

                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th colspan="3">
                            <div class="d-flex align-items-center">
                                ${product.collage_image_url ? `<img src="${product.collage_image_url}" alt="${product.product_title}" style="max-width: 25px;" class="me-2">` : ''}
                                <span>${product.product_title} (${productSku}) возвращено ${product.total_quantity} шт</span>
                            </div>
                        </th>
                    </tr>
                    <tr>
                        <th>Изображение</th>
                        <th>Товар</th>
                        <th>Количество возвращенного</th>
                    </tr>
                `;
                table.appendChild(thead);

                const tbody = document.createElement('tbody');

                sortedModifications.forEach(([modSku, mod]) => {
                    const modRow = document.createElement('tr');
                    const modThumbnailCell = document.createElement('td');
                    const modSkuCell = document.createElement('td');
                    const modQuantityCell = document.createElement('td');

                    if (mod.thumbnail_url) {
                        const modThumbnailImage = document.createElement('img');
                        modThumbnailImage.src = mod.thumbnail_url;
                        modThumbnailImage.alt = modSku;
                        modThumbnailImage.style.maxWidth = '35px';
                        modThumbnailCell.appendChild(modThumbnailImage);
                    } else {
                        modThumbnailCell.textContent = 'Нет изображения';
                    }

                    modSkuCell.textContent = modSku;
                    modQuantityCell.textContent = `${mod.quantity} шт`;

                    modRow.appendChild(modThumbnailCell);
                    modRow.appendChild(modSkuCell);
                    modRow.appendChild(modQuantityCell);
                    tbody.appendChild(modRow);
                });

                table.appendChild(tbody);
                returnsReportContainer.appendChild(table);
            });
        } else {
            const noReturnsMessage = document.createElement('h3');
            noReturnsMessage.textContent = 'Возвратов нет';
            returnsReportContainer.appendChild(noReturnsMessage);
        }

        // Обработка данных по чистой кассе
        if (netData) {
            const netSummary = document.createElement('div');
            netSummary.innerHTML = `
                <h5><span class="badge bg-success">Чистая касса: ${Math.floor(netData.net_sales_sum)} грн, ${netData.net_sales_quantity} шт</span></h5>
            `;
            netSummaryContainer.appendChild(netSummary);
        }
    }

    function updateCharts(salesData, returnsData) {
        if (salesData && Object.keys(salesData).length > 1) {
            salesChartContainer.parentElement.style.display = 'block'; // Показываем контейнер графика продаж
            updateSalesChart(salesData);
        } else {
            salesChartContainer.parentElement.style.display = 'none'; // Скрываем контейнер графика продаж
        }

        if (returnsData && Object.keys(returnsData).length > 1) {
            returnsChartContainer.parentElement.style.display = 'block'; // Показываем контейнер графика возвратов
            updateReturnsChart(returnsData);
        } else {
            returnsChartContainer.parentElement.style.display = 'none'; // Скрываем контейнер графика возвратов
        }
    }

    function updateSalesChart(salesData) {
        const chartData = Object.entries(salesData)
            .filter(([key]) => key !== 'total')
            .map(([productSku, product]) => ({
                name: productSku,
                value: product.total_quantity
            }));

        const option = {
            title: {
                text: 'График продаж',
                left: 'center',
                textStyle: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    return `${params.name}: ${params.value} шт`;
                }
            },
            legend: {
                type: 'scroll',
                bottom: '0%',
                left: 'center',
                textStyle: {
                    color: '#ffffff'
                }
            },
            series: [
                {
                    name: 'Продажи',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '20',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: chartData
                }
            ]
        };

        salesChart.setOption(option);
        salesChart.resize();
    }

    function updateReturnsChart(returnsData) {
        const chartData = Object.entries(returnsData)
            .filter(([key]) => key !== 'total')
            .map(([productSku, product]) => ({
                name: productSku,
                value: product.total_quantity
            }));

        const option = {
            title: {
                text: 'График возвратов',
                left: 'center',
                textStyle: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    return `${params.name}: ${params.value} шт`;
                }
            },
            legend: {
                type: 'scroll',
                bottom: '0%',
                left: 'center',
                textStyle: {
                    color: '#ffffff'
                }
            },
            series: [
                {
                    name: 'Возвраты',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '20',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: chartData
                }
            ]
        };

        returnsChart.setOption(option);
        returnsChart.resize();
    }

    function updateStockReport(stockData) {
        // Очистка контейнеров
        salesSummaryContainer.innerHTML = '';
        returnsSummaryContainer.innerHTML = '';
        netSummaryContainer.innerHTML = '';
        salesReportContainer.innerHTML = '';
        returnsReportContainer.innerHTML = '';

        if (stockData && Object.keys(stockData).length > 0) {
            const sortedStockData = Object.entries(stockData).sort((a, b) => extractNumericPrefix(b[0]) - extractNumericPrefix(a[0]));

            sortedStockData.forEach(([productSku, product]) => {
                // Вычисляем общую сумму остатков по всем модификациям
                let totalStock = 0;
                Object.values(product.modifications).forEach(mod => {
                    totalStock += mod.stock_quantity;
                });

                const sortedModifications = Object.entries(product.modifications)
                    .sort(([, a], [, b]) => b.stock_quantity - a.stock_quantity);

                const table = document.createElement('table');
                table.classList.add('table', 'table-striped', 'table-bordered', 'mb-4');

                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th colspan="3">
                            <div class="d-flex align-items-center">
                                ${product.collage_image_url ? `<img src="${product.collage_image_url}" alt="${product.product_title}" style="max-width: 25px; margin-right: 10px;" class="me-2">` : ''}
                                <span>${product.product_title} (${productSku}) ${totalStock} шт</span>
                            </div>
                        </th>
                    </tr>
                    <tr>
                        <th>Изображение модификации</th>
                        <th>Товар</th>
                        <th>Остаток</th>
                    </tr>
                `;
                table.appendChild(thead);

                const tbody = document.createElement('tbody');

                sortedModifications.forEach(([modSku, mod]) => {
                    const modRow = document.createElement('tr');
                    const modThumbnailCell = document.createElement('td');
                    const modSkuCell = document.createElement('td');
                    const modStockCell = document.createElement('td');

                    if (mod.thumbnail_url) {
                        const modThumbnailImage = document.createElement('img');
                        modThumbnailImage.src = mod.thumbnail_url;
                        modThumbnailImage.alt = modSku;
                        modThumbnailImage.style.maxWidth = '35px';
                        modThumbnailCell.appendChild(modThumbnailImage);
                    } else {
                        modThumbnailCell.textContent = 'Нет изображения';
                    }

                    modSkuCell.textContent = modSku;
                    modStockCell.textContent = `${mod.stock_quantity} шт`;

                    modRow.appendChild(modThumbnailCell);
                    modRow.appendChild(modSkuCell);
                    modRow.appendChild(modStockCell);
                    tbody.appendChild(modRow);
                });

                table.appendChild(tbody);
                salesReportContainer.appendChild(table);
            });
        } else {
            const noStockMessage = document.createElement('h3');
            noStockMessage.textContent = 'Данных по остаткам нет';
            salesReportContainer.appendChild(noStockMessage);
        }
    }

    function extractNumericPrefix(sku) {
        const match = sku.match(/^(\d+)/);
        if (match) {
            return parseInt(match[1], 10);
        } else {
            return -Infinity; // Для SKU без числового префикса
        }
    }

    initializeCharts();

    reportControls.addEventListener('click', function(event) {
        if (event.target.classList.contains('report-period-button')) {
            document.querySelectorAll('.report-period-button').forEach(button => {
                button.classList.remove('btn-primary', 'active');
                button.classList.add('btn-secondary');
            });

            event.target.classList.remove('btn-secondary');
            event.target.classList.add('btn-primary', 'active');

            const period = event.target.getAttribute('data-period');

            // Убираем активное состояние с кнопки Остатки
            stockButton.classList.remove('btn-primary', 'active');
            stockButton.classList.add('btn-secondary');

            salesChart.showLoading();  // Показываем индикатор загрузки при смене периода
            returnsChart.showLoading();  // Показываем индикатор загрузки при смене периода

            updateReportTitle(period);
            socket.send(JSON.stringify({ type: 'update_period', period: period }));
        }
    });

    stockButton.addEventListener('click', function() {

        // Снимаем активное состояние с других кнопок
        document.querySelectorAll('.report-period-button').forEach(button => {
            button.classList.remove('btn-primary', 'active');
            button.classList.add('btn-secondary');
        });

        // Снимаем активное состояние с кнопки кастомного периода
        customPeriodButton.classList.remove('btn-primary', 'active');
        customPeriodButton.classList.add('btn-secondary');

        // Добавляем активное состояние к кнопке "Остатки"
        stockButton.classList.remove('btn-secondary');
        stockButton.classList.add('btn-primary', 'active');

        // Сбрасываем графики и контейнеры
        resetCharts();
        salesSummaryContainer.innerHTML = '';
        returnsSummaryContainer.innerHTML = '';
        netSummaryContainer.innerHTML = '';
        salesReportContainer.innerHTML = '';
        returnsReportContainer.innerHTML = '';

        // Обновляем заголовок отчёта
        reportTitle.textContent = 'Остатки товаров';

        // Отправляем запрос на получение данных по остаткам
        socket.send(JSON.stringify({ type: 'get_stock_data' }));
    });

    function updateReportTitle(period, startDate = null, endDate = null) {
        let titleText = '';
        let calculatedStartDate, calculatedEndDate;

        switch (period) {
            case 'today':
                calculatedStartDate = new Date();
                calculatedEndDate = new Date();
                titleText = `Продажи за сегодня (${formatDate(calculatedStartDate)} - ${formatDate(calculatedEndDate)})`;
                break;
            case 'yesterday':
                calculatedStartDate = new Date();
                calculatedStartDate.setDate(calculatedStartDate.getDate() - 1);
                calculatedEndDate = new Date(calculatedStartDate);
                titleText = `Продажи за вчера (${formatDate(calculatedStartDate)} - ${formatDate(calculatedEndDate)})`;
                break;
            case 'week':
                calculatedStartDate = new Date();
                calculatedStartDate.setDate(calculatedStartDate.getDate() - calculatedStartDate.getDay() + 1); // Начало недели (понедельник)
                calculatedEndDate = new Date();
                titleText = `Продажи за неделю (${formatDate(calculatedStartDate)} - ${formatDate(calculatedEndDate)})`;
                break;
            case 'month':
                calculatedStartDate = new Date();
                calculatedStartDate.setDate(1); // Начало месяца
                calculatedEndDate = new Date();
                titleText = `Продажи за месяц (${formatDate(calculatedStartDate)} - ${formatDate(calculatedEndDate)})`;
                break;
            case 'year':
                calculatedStartDate = new Date();
                calculatedStartDate.setMonth(0, 1); // Начало года
                calculatedEndDate = new Date();
                titleText = `Продажи за год (${formatDate(calculatedStartDate)} - ${formatDate(calculatedEndDate)})`;
                break;
            case 'custom':
                calculatedStartDate = parseDate(startDate);
                calculatedEndDate = parseDate(endDate);
                titleText = `Продажи за период с ${formatDate(calculatedStartDate)} по ${formatDate(calculatedEndDate)}`;
                break;
            default:
                titleText = 'Выберите период';
        }

        reportTitle.textContent = titleText;
    }

    function formatDate(date) {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы в JavaScript начинаются с 0
        const year = date.getFullYear();
        return `${day}-${month}-${year}`;
    }

    function parseDate(dateString) {
        const [day, month, year] = dateString.split('-');
        return new Date(year, month - 1, day); // Месяцы в JavaScript начинаются с 0
    }

});
