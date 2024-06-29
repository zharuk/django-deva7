function loadPendingSaleItems(saleId) {
    console.log("Запрос данных для продажи ID:", saleId);
    $.ajax({
        url: get_pending_sale_items_url,
        method: 'GET',
        data: {
            'sale_id': saleId
        },
        success: function(data) {
            console.log("Данные текущей корзины успешно загружены");
            $('#selected-items-table tbody').html(data.items_html);
            $('#total-amount').text(data.total_amount);
        },
        error: function(xhr) {
            console.error("Ошибка при загрузке данных текущей корзины:", xhr);
        }
    });
}

if (pending_sale_id) {
    console.log("Загрузка данных текущей корзины для продажи ID:", pending_sale_id);
    loadPendingSaleItems(pending_sale_id);
}
