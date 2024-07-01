if (typeof activeFilter === 'undefined') {
    var activeFilter = 'all';
}

function filterPreorders(filter, title) {
    document.getElementById('preorderTitle').innerText = title;
    const allPreorders = document.querySelectorAll('.preorder-item');
    allPreorders.forEach(preorder => {
        preorder.style.display = 'none';
        if (filter === 'all' || preorder.classList.contains(filter)) {
            preorder.style.display = 'block';
        }
    });

    activeFilter = filter;
}
