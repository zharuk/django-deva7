$('#sell-button').click(function() {
    const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
    const comment = $('#sale-comment').val();
    const saleId = pending_sale_id;
    console.log("Подтверждение продажи", saleId);

    if (!saleId) {
        console.error("Sale ID is missing");
        showAlert('error', 'Sale ID is missing');
        return;
    }

    $.ajax({
        url: confirm_sale_url,
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'comment': comment,
            'sale_id': saleId
        },
        success: function(data) {
            console.log("Продажа успешно завершена");
            $('#selected-items-table tbody').empty();
            $('#total-amount').text('0');
            $('#sale-comment').val('');
            showAlert('success', 'Продажа успешно завершена!');
            loadDailySales();
            $('#search-article').val('');
            clearSearchResults();

            // Создание новой продажи после завершения текущей
            $.ajax({
                url: create_new_sale_url,
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(data) {
                    console.log("Новая продажа инициализирована", data.sale_id);
                    pending_sale_id = data.sale_id; // обновляем pending_sale_id
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
        },
        error: function(xhr) {
            console.error("Ошибка при подтверждении продажи:", xhr);
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert('error', xhr.responseJSON.error);
            } else {
                showAlert('error', 'Произошла ошибка при завершении продажи');
            }
        }
    });
});
