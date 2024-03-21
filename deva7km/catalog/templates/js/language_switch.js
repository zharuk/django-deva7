document.addEventListener('DOMContentLoaded', function() {
    var languageSelect = document.getElementById('language-select');

    languageSelect.addEventListener('change', function() {
        var languageForm = document.getElementById('language-form');
        languageForm.submit(); // Отправляем форму на сервер
    });
});