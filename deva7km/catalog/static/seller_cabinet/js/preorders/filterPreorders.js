function filterPreorders(filter, title) {
    activeFilter = filter;
    document.getElementById('preorderTitle').textContent = title;
    applyFilter(filter);
}