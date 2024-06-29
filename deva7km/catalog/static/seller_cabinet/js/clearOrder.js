$('#clear-order').click(function() {
    const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
    console.log("Очистка заказа");
    $.ajax({
        url: clear_sale_url,
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(data) {
            console.log("Заказ успешно очищен");
            $('#selected-items-table tbody').empty();
            $('#total-amount').text('0');
            showAlert('success', 'Заказ успешно очищен');
        },
        error: function(xhr) {
            console.error("Ошибка при очистке заказа:", xhr);
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert('error', xhr.responseJSON.error);
            } else {
                showAlert('error', 'Произошла ошибка при очистке заказа');
            }
        }
    });
});
