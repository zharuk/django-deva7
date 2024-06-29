let debounceTimer;
let currentPage = 1;
let currentQuery = '';

$('#search-article').on('input', function() {
    clearTimeout(debounceTimer);
    const query = $(this).val();
    currentQuery = query;
    currentPage = 1;
    debounceTimer = setTimeout(function() {
        if (query.length >= 3) {
            loadSearchResults(query, currentPage);
        } else {
            clearSearchResults();
        }
    }, 300);
});

$('#clear-search').click(function() {
    $('#search-article').val('');
    clearSearchResults();
});

function clearSearchResults() {
    $('#available-items').empty().addClass('hidden');
}

function loadSearchResults(query, page, append = false) {
    console.log("Поиск товаров по артикулу:", query, "Страница:", page);
    $.ajax({
        url: search_article_url,
        method: 'GET',
        data: {
            'article': query,
            'page': page
        },
        success: function(data) {
            console.log("Результаты поиска загружены");
            if (append) {
                $('.more-results').remove();
                $('#available-items').append(data);
            } else {
                $('#available-items').html(data);
            }
            $('#available-items').removeClass('hidden').show();
        },
        error: function(xhr) {
            console.error("Ошибка при загрузке результатов поиска:", xhr);
            showAlert('error', xhr.responseJSON.error);
        }
    });
}
