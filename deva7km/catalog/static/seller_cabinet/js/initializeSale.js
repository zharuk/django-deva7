$(document).ready(function() {
    if (!pending_sale_id) {
        console.log("Нет текущей продажи, создаем новую...");
        $.ajax({
            url: create_new_sale_url,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf_token
            },
            success: function(data) {
                console.log("Новая продажа инициализирована", data.sale_id);
                pending_sale_id = data.sale_id; // обновляем pending_sale_id
                $('#selected-items-table tbody').empty();
                $('#total-amount').text('0');
                $('#sale-comment').val('');
                showAlert('success', 'Новая продажа инициализирована');
            },
            error: function(xhr) {
                console.error("Ошибка при инициализации новой продажи:", xhr);
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    showAlert('error', xhr.responseJSON.error);
                } else {
                    showAlert('error', 'Произошла ошибка при инициализации новой продажи');
                }
            }
        });
    } else {
        loadPendingSaleItems(pending_sale_id);
    }
});
