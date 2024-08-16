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

    let salesChart;
    let returnsChart;

    function initializeCharts() {
        salesChart = echarts.init(salesChartContainer);
        returnsChart = echarts.init(returnsChartContainer);
        console.log("Графики инициализированы.");
    }

    function resetCharts() {
        salesChart.clear();
        returnsChart.clear();
        salesChartContainer.style.display = 'none';
        returnsChartContainer.style.display = 'none';
    }

    let socket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/reports/`);

        socket.onopen = function() {
            console.log("WebSocket соединение установлено.");
            socket.send(JSON.stringify({ type: 'get_initial_data' }));
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log("Полученные данные:", data);

            const salesData = data.sales_data.sales || null;
            const returnsData = data.sales_data.returns || null;
            const netData = data.sales_data.net || null;

            console.log("Данные для графика продаж:", salesData);
            console.log("Данные для графика возвратов:", returnsData);

            if (data.event === 'report_data') {
                resetCharts(); // Сброс графиков перед обновлением
                updateSalesReport(salesData, returnsData, netData);
                updateCharts(salesData, returnsData);
            }
        };

        socket.onclose = function(e) {
            console.log("WebSocket соединение закрыто.");
            setTimeout(connectWebSocket, 1000);
        };

        socket.onerror = function(e) {
            console.error('Ошибка WebSocket:', e);
        };
    }

    connectWebSocket();

    function updateSalesReport(salesData, returnsData, netData) {
        salesSummaryContainer.innerHTML = '';
        returnsSummaryContainer.innerHTML = '';
        netSummaryContainer.innerHTML = '';
        salesReportContainer.innerHTML = '';
        returnsReportContainer.innerHTML = '';

        if (salesData && Object.keys(salesData).length > 1) {
            const salesSummary = document.createElement('div');
            salesSummary.innerHTML = `
                <h5>Итого продано: ${salesData.total.total_quantity} шт</h5>
                <h5>Общая сумма продаж: ${Math.floor(salesData.total.total_sales_sum)} грн</h5>
            `;
            salesSummaryContainer.appendChild(salesSummary);

            const salesTitle = document.createElement('h3');
            salesTitle.textContent = 'Продажи';
            salesReportContainer.appendChild(salesTitle);

            for (const [productSku, product] of Object.entries(salesData).filter(([key]) => key !== 'total')) {
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
        } else {
            const noSalesMessage = document.createElement('h3');
            noSalesMessage.textContent = 'Продаж нет';
            salesReportContainer.appendChild(noSalesMessage);
        }

        if (returnsData && Object.keys(returnsData).length > 1) {
            const returnsSummary = document.createElement('div');
            returnsSummary.innerHTML = `
                <h5>Итого возвращено: ${returnsData.total.total_quantity} шт</h5>
                <h5>Общая сумма возвратов: ${Math.floor(returnsData.total.total_sales_sum)} грн</h5>
            `;
            returnsSummaryContainer.appendChild(returnsSummary);

            const returnsTitle = document.createElement('h3');
            returnsTitle.textContent = 'Возвраты';
            returnsReportContainer.appendChild(returnsTitle);

            for (const [productSku, product] of Object.entries(returnsData).filter(([key]) => key !== 'total')) {
                const table = document.createElement('table');
                table.classList.add('table', 'table-striped', 'table-bordered', 'mb-4');

                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th colspan="3">
                            <div class="d-flex align-items-center">
                                ${product.collage_image_url ? `<img src="${product.collage_image_url}" alt="${product.product_title}" style="max-width: 50px;" class="me-2">` : ''}
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
                returnsReportContainer.appendChild(table);
            }
        } else {
            const noReturnsMessage = document.createElement('h3');
            noReturnsMessage.textContent = 'Возвратов нет';
            returnsReportContainer.appendChild(noReturnsMessage);
        }

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
            salesChartContainer.parentElement.style.display = 'block'; // Показываем контейнер графика
            updateSalesChart(salesData);
        } else {
            salesChartContainer.parentElement.style.display = 'none'; // Скрываем контейнер графика
        }

        if (returnsData && Object.keys(returnsData).length > 1) {
            returnsChartContainer.parentElement.style.display = 'block'; // Показываем контейнер графика
            updateReturnsChart(returnsData);
        } else {
            returnsChartContainer.parentElement.style.display = 'none'; // Скрываем контейнер графика
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
        console.log("График продаж обновлен.");
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
        console.log("График возвратов обновлен.");
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
            updateReportTitle(period);
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
