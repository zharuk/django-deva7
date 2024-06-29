function loadDailySales() {
    console.log("Загрузка ежедневных продаж");
    $.ajax({
        url: get_daily_sales_url,
        type: 'GET',
        success: function(response) {
            console.log("Ежедневные продажи успешно загружены");
            $('#daily-sales-table-body').html(response.sales_html);
            $('#total-daily-sales-amount').text(response.total_amount);
        },
        error: function(xhr) {
            console.error("Ошибка при загрузке ежедневных продаж:", xhr);
        }
    });
}

loadDailySales();
