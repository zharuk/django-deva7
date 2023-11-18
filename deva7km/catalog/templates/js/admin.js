// Ваш JavaScript-файл (например, admin.js)
(function($) {
    $(document).ready(function() {
        // Функция для обновления списка модификаций на основе выбранного основного товара
        window.change_product_modifications = function(mainProductId) {
            // Отправляем AJAX-запрос для получения модификаций
            $.ajax({
                url: '{% url "get_modifications" %}',  // Используйте правильный URL для вашего представления
                data: {'main_product_id': mainProductId},
                success: function(data) {
                    // Обновляем список модификаций
                    var modificationSelect = $('#id_product_modification');
                    modificationSelect.empty();

                    $.each(data, function(index, modification) {
                        modificationSelect.append(
                            $('<option>', {
                                value: modification.id,
                                text: modification.custom_sku
                            })
                        );
                    });
                }
            });
        };
    });
})(django.jQuery);