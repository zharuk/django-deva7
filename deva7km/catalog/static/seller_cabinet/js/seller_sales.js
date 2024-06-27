$(document).ready(function() {
    let debounceTimer;
    let currentPage = 1;
    let currentQuery = '';

    // Загрузка текущих данных корзины при загрузке страницы
    if (pending_sale_id) {
        loadPendingSaleItems(pending_sale_id);
    }

    function loadPendingSaleItems(saleId) {
        $.ajax({
            url: get_pending_sale_items_url,
            method: 'GET',
            data: {
                'sale_id': saleId
            },
            success: function(data) {
                $('#selected-items-table tbody').html(data.items_html);
                $('#total-amount').text(data.total_amount);
            },
            error: function(xhr) {
                console.error("Error loading pending sale items:", xhr);
            }
        });
    }

    $('#search-article').on('input', function() {
        clearTimeout(debounceTimer);
        const query = $(this).val();
        currentQuery = query;
        currentPage = 1;
        debounceTimer = setTimeout(function() {
            if (query.length >= 3) {
                loadSearchResults(query, currentPage);
            } else {
                $('#available-items').empty();
            }
        }, 300);
    });

    $('#clear-search').click(function() {
        $('#search-article').val('');
        $('#available-items').empty();
    });

    function loadSearchResults(query, page, append = false) {
        $.ajax({
            url: search_article_url,
            method: 'GET',
            data: {
                'article': query,
                'page': page
            },
            success: function(data) {
                if (append) {
                    $('.more-results').remove();
                    $('#available-items').append(data);
                } else {
                    $('#available-items').html(data);
                }
                $('.search-results').show();
            },
            error: function(xhr) {
                showAlert('error', xhr.responseJSON.error);
            }
        });
    }

    function showAlert(type, message) {
        const alertDiv = type === 'success' ? $('#success-alert') : $('#error-alert');
        const alertMessage = type === 'success' ? $('#success-message') : $('#error-message');
        alertMessage.text(message);
        alertDiv.addClass('show');

        setTimeout(function() {
            alertDiv.removeClass('show');
        }, 2000);
    }

    $(document).on('click', '.add-item-button', function() {
        const itemId = $(this).data('item-id');
        const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: add_item_to_sale_url,
            method: 'POST',
            data: {
                'item_id': itemId,
                'quantity': 1,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(data) {
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
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    showAlert('error', xhr.responseJSON.error);
                } else {
                    showAlert('error', 'Произошла ошибка при добавлении товара');
                }
            }
        });
    });

    $(document).on('click', '.remove-item-button', function() {
        const itemId = $(this).data('item-id');
        const productId = $(this).data('product-id');
        const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: remove_item_from_sale_url,
            method: 'POST',
            data: {
                'item_id': itemId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(data) {
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
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    showAlert('error', xhr.responseJSON.error);
                } else {
                    showAlert('error', 'Произошла ошибка при удалении товара');
                }
            }
        });
    });

    $('#clear-order').click(function() {
        const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: clear_sale_url,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(data) {
                $('#selected-items-table tbody').empty();
                $('#total-amount').text('0');
                showAlert('success', 'Заказ успешно очищен');
            },
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    showAlert('error', xhr.responseJSON.error);
                } else {
                    showAlert('error', 'Произошла ошибка при очистке заказа');
                }
            }
        });
    });

    $('#sell-button').click(function() {
        const csrfToken = $('#csrf-form [name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: confirm_sale_url,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(data) {
                $('#selected-items-table tbody').empty();
                $('#total-amount').text('0');
                showAlert('success', 'Продажа успешно завершена!');
                loadDailySales();  // Обновление таблицы продаж за день
                // Сброс поля поиска и результатов поиска
                $('#search-article').val('');
                $('#available-items').empty();
            },
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    showAlert('error', xhr.responseJSON.error);
                } else {
                    showAlert('error', 'Произошла ошибка при завершении продажи');
                }
            }
        });
    });

    $(document).on('click', '#load-more-results', function() {
        const nextPage = $(this).data('next-page');
        currentPage = nextPage;
        loadSearchResults(currentQuery, currentPage, true);
    });

    function loadDailySales() {
        $.ajax({
            url: get_daily_sales_url,
            type: 'GET',
            success: function(response) {
                $('#daily-sales-table-body').html(response.sales_html);
                $('#total-daily-sales-amount').text(response.total_amount);
            },
            error: function(xhr) {
                console.error(xhr);
            }
        });
    }

    // Загрузка ежедневных продаж при загрузке страницы
    loadDailySales();
});
