$(document).on('click', '.cancel-sale-button', function() {
    const saleId = $(this).data('sale-id');
    $('#confirmDeleteButton').data('sale-id', saleId); // Сохранение ID продажи в кнопке подтверждения
    $('#confirmDeleteModal').modal('show'); // Показ модального окна
});

$('#confirmDeleteButton').click(function() {
    const saleId = $(this).data('sale-id');
    const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
    console.log("Отмена продажи ID:", saleId);
    $.ajax({
        url: cancel_sale_url,
        method: 'POST',
        data: {
            'sale_id': saleId,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(data) {
            console.log("Продажа успешно удалена");
            showAlert('success', 'Продажа успешно удалена');
            loadDailySales(); // Обновление таблицы продаж за день
            $('#confirmDeleteModal').modal('hide'); // Скрыть модальное окно после успешного удаления
        },
        error: function(xhr) {
            console.error("Ошибка при удалении продажи:", xhr);
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert('error', xhr.responseJSON.error);
            } else {
                showAlert('error', 'Произошла ошибка при удалении продажи');
            }
            $('#confirmDeleteModal').modal('hide'); // Скрыть модальное окно в случае ошибки
        }
    });
});
