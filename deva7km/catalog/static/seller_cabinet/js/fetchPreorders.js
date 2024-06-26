// Обновляем fetchPreorders для добавления обработчиков иконок редактирования
function fetchPreorders() {
    $.ajax({
        url: '/api/get_preorders/',
        method: 'GET',
        success: function (data) {
            var preordersContainer = $('#preorderContainer');
            preordersContainer.empty(); // Очистить контейнер перед добавлением новых данных
            data.preorders.forEach(function (preorder) {
                var preorderHtml = '<div class="col-md-4 mb-4 preorder-item all ' +
                    (preorder.shipped_to_customer ? '' : 'not-shipped') + ' ' +
                    (preorder.receipt_issued ? '' : 'not-receipted') +
                    '" id="preorder-' + preorder.id + '">' +
                    '<div class="card">' +
                    '<div class="card-body">' +
                    '<div class="d-flex justify-content-between align-items-start">' +
                    '<h5 class="card-title">' + preorder.full_name + '</h5>' +
                    '<i class="fas fa-edit edit-icon" data-id="' + preorder.id + '" style="cursor:pointer;"></i>' +
                    '</div>' +
                    '<div class="badge-container">' +
                    (preorder.shipped_to_customer && preorder.receipt_issued ?
                        '<span class="badge bg-success mb-2">Отправлен и пробит</span>' :
                        (preorder.shipped_to_customer ? '' : '<span class="badge bg-warning text-dark mb-2">Не отправлено</span>') +
                        (preorder.receipt_issued ? '' : '<span class="badge bg-danger text-white mb-2">Не пробит чек</span>')) +
                    '</div>' +
                    '<div class="info-block">' +
                    '<p class="card-text mt-3">' +
                    '<strong>Инфо:</strong> ' + preorder.text.replace(/\n/g, '<br>') + '<br>' +
                    '<strong>Дроп:</strong> ' + (preorder.drop ? '<i class="fas fa-check-circle text-success"></i>' : '<i class="fas fa-times-circle text-danger"></i>') + '<br>' +
                    '<strong>Дата создания:</strong> ' + preorder.created_at + '<br>' +
                    '<strong>Дата изменения:</strong> ' + preorder.updated_at + '<br>' +
                    '<strong>ТТН:</strong> <span class="badge bg-light ttn-badge" id="ttn-' + preorder.id + '">' + preorder.ttn + '</span><br>' +
                    '<strong>Статус посылки:</strong> ' + preorder.status + '<br>' +
                    '</p>' +
                    '</div>' +
                    '<div class="form-check form-switch d-inline-block me-3">' +
                    '<input class="form-check-input ' + (preorder.shipped_to_customer ? 'bg-success' : 'bg-warning') +
                    '" type="checkbox" id="shipped_to_customer_' + preorder.id + '"' +
                    (preorder.shipped_to_customer ? ' checked' : '') +
                    ' onchange="toggleShipped(' + preorder.id + ', this.checked)">' +
                    '<label class="form-check-label" for="shipped_to_customer_' + preorder.id + '">Отправлен</label>' +
                    '</div>' +
                    '<div class="form-check form-switch d-inline-block">' +
                    '<input class="form-check-input ' + (preorder.receipt_issued ? 'bg-success' : 'bg-danger') +
                    '" type="checkbox" id="receipt_issued_' + preorder.id + '"' +
                    (preorder.receipt_issued ? ' checked' : '') +
                    ' onchange="toggleReceipt(' + preorder.id + ', this.checked)">' +
                    '<label class="form-check-label" for="receipt_issued_' + preorder.id + '">Чек</label>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>';
                preordersContainer.append(preorderHtml);
            });

            // Применить текущий активный фильтр после обновления данных
            applyFilter(activeFilter);

            // Добавим обработчики для иконок редактирования после обновления предзаказов
            addEditIconListeners();
        }
    });
}

// Применение фильтра
function applyFilter(filter) {
    const allPreorders = document.querySelectorAll('.preorder-item');
    allPreorders.forEach(preorder => {
        preorder.style.display = 'none';
        if (filter === 'all' || preorder.classList.contains(filter)) {
            preorder.style.display = 'block';
        }
    });
}

// Запуск функции fetchPreorders каждые 5 секунд
setInterval(fetchPreorders, 5000);

// Вызовите fetchPreorders сразу после загрузки страницы
$(document).ready(function () {
    fetchPreorders();
});