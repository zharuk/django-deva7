document.addEventListener('DOMContentLoaded', function() {
    const reportControls = document.getElementById('report-controls');
    const salesReportContainer = document.getElementById('sales-report-container');
    const reportTitle = document.getElementById('report-title');
    const customPeriodButton = document.getElementById('custom-period-button');
    const customPeriodModal = new bootstrap.Modal(document.getElementById('customPeriodModal'));
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const applyCustomPeriodButton = document.getElementById('apply-custom-period');
    const salesChartContainer = document.getElementById('sales-chart');

    // Инициализация графика
    let salesChart;

    function initializeSalesChart() {
        salesChart = echarts.init(salesChartContainer);
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
                updateSalesReport(data.sales_data);
                updateSalesChart(data.sales_data);
            }
        };

        socket.onclose = function(e) {
            showConnectionLostModal();
            setTimeout(connectWebSocket, 1000);
        };

        socket.onerror = function(e) {
            console.error('Ошибка WebSocket:', e);
        };
    }

    connectWebSocket();

    // Открытие модального окна для выбора периода
    customPeriodButton.addEventListener('click', function() {
        customPeriodModal.show();
    });

    // Инициализация календаря для выбора дат
    $(startDateInput).datepicker({
        dateFormat: 'dd-mm-yy',
        onSelect: function() {
            $(endDateInput).datepicker('option', 'minDate', startDateInput.value);
        }
    });

    $(endDateInput).datepicker({
        dateFormat: 'dd-mm-yy',
        onSelect: function() {
            $(startDateInput).datepicker('option', 'maxDate', endDateInput.value);
        }
    });

    applyCustomPeriodButton.addEventListener('click', function() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        if (startDate && endDate) {
            updateReportTitle('custom', startDate, endDate);
            socket.send(JSON.stringify({
                type: 'update_period',
                period: 'custom',
                start_date: startDate,
                end_date: endDate
            }));

            customPeriodModal.hide();

            document.querySelectorAll('.report-period-button').forEach(button => {
                button.classList.remove('btn-primary', 'active');
                button.classList.add('btn-secondary');
            });
            customPeriodButton.classList.add('btn-primary', 'active');
        } else {
            alert('Пожалуйста, выберите обе даты.');
        }
    });

    function updateSalesReport(salesData) {
        // Удаляем предыдущий элемент с итогами, если он существует
        const existingTotalContainer = document.getElementById('total-sales-summary');
        if (existingTotalContainer) {
            existingTotalContainer.remove();
        }

        const sortedSalesData = Object.entries(salesData)
            .filter(([key]) => key !== 'total')
            .sort(([, a], [, b]) => b.total_quantity - a.total_quantity);

        // Добавляем строку с общей суммой и количеством проданного сразу под графиком
        if (salesData.total) {
            const totalContainer = document.createElement('div');
            totalContainer.id = 'total-sales-summary';
            totalContainer.classList.add('mt-3');
            totalContainer.innerHTML = `
                <h5>Итого продано: ${salesData.total.total_quantity} шт</h5>
                <h5>Общая сумма продаж: ${Math.floor(salesData.total.total_sales_sum)} грн</h5>
            `;
            salesChartContainer.insertAdjacentElement('afterend', totalContainer);
        }

        salesReportContainer.innerHTML = '';  // Очистка контейнера перед обновлением

        for (const [productSku, product] of sortedSalesData) {
            const table = document.createElement('table');
            table.classList.add('table', 'table-striped', 'table-bordered', 'mb-4');

            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th colspan="3">
                        <div class="d-flex align-items-center">
                            ${product.collage_image_url ? `<img src="${product.collage_image_url}" alt="${product.product_title}" style="max-width: 50px;" class="me-2">` : ''}
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

            for (const modSku in product.modifications) {
                const mod = product.modifications[modSku];

                const modRow = document.createElement('tr');
                const modThumbnailCell = document.createElement('td');
                const modSkuCell = document.createElement('td');
                const modQuantityCell = document.createElement('td');

                if (mod.thumbnail_url) {
                    const modThumbnailImage = document.createElement('img');
                    modThumbnailImage.src = mod.thumbnail_url;
                    modThumbnailImage.alt = modSku;
                    modThumbnailImage.style.maxWidth = '50px';
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
            }

            table.appendChild(tbody);
            salesReportContainer.appendChild(table);
        }
    }

    function updateSalesChart(salesData) {
        const chartData = Object.entries(salesData).map(([productSku, product]) => ({
            name: productSku,
            value: product.total_quantity
        }));

        const option = {
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    return `${params.name}: ${params.value} шт`;
                }
            },
            legend: {
                type: 'plain',  // Используем режим plain, чтобы расположить все элементы без прокрутки
                bottom: 0,
                left: 'center',
                itemWidth: 14,  // Ширина символов легенды
                itemHeight: 14, // Высота символов легенды
                textStyle: {
                    color: '#ffffff',  // Цвет текста легенды для темной темы
                    fontSize: 12
                },
                pageIconColor: '#ffffff',
                pageTextStyle: {
                    color: '#ffffff'
                }
            },
            grid: {
                top: '10%',   // Оставляем больше места сверху для легенды
                bottom: '15%',  // Увеличиваем пространство снизу, чтобы уместить легенду
                containLabel: true
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
    }

    function showConnectionLostModal() {
        const connectionLostModal = new bootstrap.Modal(document.getElementById('connectionLostModal'), {
            backdrop: 'static',
            keyboard: false
        });
        connectionLostModal.show();
    }

    // Инициализация графика при загрузке страницы
    initializeSalesChart();

    // Обновление периода по клику на кнопки
    reportControls.addEventListener('click', function(event) {
        if (event.target.classList.contains('report-period-button')) {
            document.querySelectorAll('.report-period-button').forEach(button => {
                button.classList.remove('btn-primary', 'active');
                button.classList.add('btn-secondary');
            });

            event.target.classList.remove('btn-secondary');
            event.target.classList.add('btn-primary', 'active');

            const period = event.target.getAttribute('data-period');
            updateReportTitle(period); // Обновляем заголовок
            socket.send(JSON.stringify({ type: 'update_period', period: period }));
        }
    });

    function updateReportTitle(period, startDate = null, endDate = null) {
        let titleText = '';
        switch (period) {
            case 'today':
                titleText = 'Продажи за сегодня';
                break;
            case 'yesterday':
                titleText = 'Продажи за вчера';
                break;
            case 'week':
                titleText = 'Продажи за неделю';
                break;
            case 'month':
                titleText = 'Продажи за месяц';
                break;
            case 'year':
                titleText = 'Продажи за год';
                break;
            case 'custom':
                titleText = `Продажи за период с ${startDate} по ${endDate}`;
                break;
            default:
                titleText = 'Выберите период';
        }
        reportTitle.textContent = titleText;
    }
});
