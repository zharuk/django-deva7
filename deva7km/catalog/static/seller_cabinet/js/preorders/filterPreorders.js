if (typeof activeFilter === 'undefined') {
    var activeFilter = 'all';
}

function filterPreorders(filter, title) {
    // Обновляем заголовок
    document.getElementById('preorderTitle').innerText = title;

    // Обновляем состояние кнопок
    const topButtons = document.querySelectorAll('[name="btnradio-top"]');
    const bottomButtons = document.querySelectorAll('[name="btnradio-bottom"]');

    topButtons.forEach(button => {
        if (button.id.includes(filter)) {
            button.checked = true;
        } else {
            button.checked = false;
        }
    });

    bottomButtons.forEach(button => {
        if (button.id.includes(filter)) {
            button.checked = true;
        } else {
            button.checked = false;
        }
    });

    // Фильтруем предзаказы
    const allPreorders = document.querySelectorAll('.preorder-item');
    allPreorders.forEach(preorder => {
        preorder.style.display = 'none';
        if (filter === 'all' || preorder.classList.contains(filter)) {
            preorder.style.display = 'block';
        }
    });

    activeFilter = filter;
}
