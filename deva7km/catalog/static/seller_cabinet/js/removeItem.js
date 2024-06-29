$(document).on('click', '.remove-item-button', function() {
    const itemId = $(this).data('item-id');
    const productId = $(this).data('product-id');
    const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
    console.log("Удаление товара ID:", itemId);
    $.ajax({
        url: remove_item_from_sale_url,
        method: 'POST',
        data: {
            'item_id': itemId,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(data) {
            console.log("Товар успешно удален");
            $('#selected-items-table tbody').html(data.items_html);
            $('#total-amount').text(data.total_amount);
            showAlert('success', 'Товар успешно удален');
            let itemRow = $(`#available-items .item[data-item-id="${productId}"]`);
            if (itemRow.length) {
                let currentQuantity = parseInt(itemRow.data('quantity'));
                let newQuantity = currentQuantity + 1;
                itemRow.data('quantity', newQuantity);
                itemRow.find('.item-stock').text(`(${newQuantity} в наличии)`);
            } else {
                loadSearchResults(currentQuery, currentPage);
            }
        },
        error: function(xhr) {
            console.error("Ошибка при удалении товара:", xhr);
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert('error', xhr.responseJSON.error);
            } else {
                showAlert('error', 'Произошла ошибка при удалении товара');
            }
        }
    });
});
