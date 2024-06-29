$(document).on('click', '.add-item-button', function() {
    const itemId = $(this).data('item-id');
    const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
    console.log("Добавление товара ID:", itemId);
    $.ajax({
        url: add_item_to_sale_url,
        method: 'POST',
        data: {
            'item_id': itemId,
            'quantity': 1,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(data) {
            console.log("Товар успешно добавлен");
            if (data.error) {
                showAlert('error', data.error);
            } else {
                $('#selected-items-table tbody').html(data.items_html);
                $('#total-amount').text(data.total_amount);
                showAlert('success', 'Товар успешно добавлен');
                let itemRow = $(`#available-items .item[data-item-id="${itemId}"]`);
                let currentQuantity = parseInt(itemRow.data('quantity'));
                if (currentQuantity > 1) {
                    let newQuantity = currentQuantity - 1;
                    itemRow.data('quantity', newQuantity);
                    itemRow.find('.item-stock').text(`(${newQuantity} в наличии)`);
                } else {
                    itemRow.remove();
                }
                loadDailySales();  // Обновление таблицы продаж за день
            }
        },
        error: function(xhr) {
            console.error("Ошибка при добавлении товара:", xhr);
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert('error', xhr.responseJSON.error);
            } else {
                showAlert('error', 'Произошла ошибка при добавлении товара');
            }
        }
    });
});
