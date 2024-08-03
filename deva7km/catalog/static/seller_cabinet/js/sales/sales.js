document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const selectedItems = document.getElementById('selected-items');
    const totalAmount = document.getElementById('total-amount');
    const sellButton = document.getElementById('sell-button');
    const clearSearchButton = document.getElementById('clear-search');
    const clearCartButton = document.getElementById('clear-cart-button');
    const searchResultTemplate = document.getElementById('search-result-template').content;
    const selectedItemTemplate = document.getElementById('selected-item-template').content;

    let socket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/sales/`);

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log("Получены данные от сервера:", data);
            if (data.type === 'search_results') {
                displaySearchResults(data.results);
            } else if (data.type === 'update_total') {
                updateTotalAmount(data.total);
            } else if (data.type === 'sell_confirmation') {
                showNotification('success', 'Продажа завершена', 'Продажа успешно завершена!');
                handleSellConfirmation(data.status);
                loadSalesList();
            } else if (data.type === 'sell_error') {
                showNotification('danger', 'Ошибка', data.message);
            } else if (data.type === 'item_added') {
                showNotification('success', 'Товар добавлен', `${data.custom_sku} добавлен в корзину`);
            } else if (data.type === 'item_not_available') {
                showNotification('danger', 'Ошибка', `Товар ${data.custom_sku} отсутствует на складе`);
            } else if (data.type === 'sales_list') {
                displaySalesList(data.sales);
            }
        };

        socket.onclose = function(e) {
            console.error('WebSocket закрыт неожиданно, повторное подключение...');
            showConnectionLostModal();
            setTimeout(connectWebSocket, 1000);
        };

        socket.onerror = function(e) {
            console.error('Ошибка WebSocket:', e);
        };
    }

    connectWebSocket();

    function sendSocketMessage(message) {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(message));
        } else {
            console.error('WebSocket is not open:', socket.readyState);
        }
    }

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;
        fetch(`/seller_cabinet/sales/search-products/?query=${query}`)
            .then(response => response.json())
            .then(data => {
                console.log("Результаты поиска получены:", data);
                if (data.results) {
                    displaySearchResults(data.results);
                } else {
                    console.error('No results found');
                }
            })
            .catch(error => console.error('Error:', error));
    });

    clearSearchButton.addEventListener('click', function() {
        searchInput.value = '';
        searchResults.innerHTML = '';
        searchResults.classList.remove('show');
    });

    clearCartButton.addEventListener('click', function() {
        selectedItems.innerHTML = '';
        updateTotal();
    });

    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            searchResults.classList.remove('show');
        }
    });

    sellButton.addEventListener('click', function() {
        const items = getSelectedItems();
        if (items.length === 0) {
            showNotification('warning', 'Ошибка', 'Корзина пуста');
        } else {
            const saleData = {
                'type': 'create_sale',
                'user_id': 1,
                'telegram_user_id': null,
                'source': 'site',
                'payment_method': 'cash',
                'comment': '',
                'items': items
            };
            console.log("Отправка данных о продаже на сервер: ", saleData);
            sendSocketMessage(saleData);
        }
    });

    function displaySearchResults(results) {
        searchResults.innerHTML = '';
        results.forEach(item => {
            const row = document.importNode(searchResultTemplate, true);
            row.querySelector('.search-item-thumbnail').src = item.thumbnail || '';
            row.querySelector('.search-item-sku').textContent = item.sku;
            row.querySelector('.item-details').textContent = `остаток - ${item.stock} шт, цена - ${item.price} грн`;
            const addButton = row.querySelector('.search-item-add-button');
            const quantityDisplay = row.querySelector('.quantity-display');
            const incrementButton = row.querySelector('.increment-button');
            const decrementButton = row.querySelector('.decrement-button');

            incrementButton.addEventListener('click', () => {
                quantityDisplay.textContent = parseInt(quantityDisplay.textContent) + 1;
            });

            decrementButton.addEventListener('click', () => {
                if (parseInt(quantityDisplay.textContent) > 1) {
                    quantityDisplay.textContent = parseInt(quantityDisplay.textContent) - 1;
                }
            });

            addButton.addEventListener('click', () => checkAvailabilityAndAddItem(item.sku, item.price, item.stock, item.thumbnail, parseInt(quantityDisplay.textContent)));
            searchResults.appendChild(row);
        });
        searchResults.classList.add('show');
    }

    function displaySalesList(sales) {
        const salesList = document.getElementById('sales-list');
        salesList.innerHTML = '';
        let totalItems = 0;
        let totalAmount = 0;
        sales.forEach(sale => {
            const saleElement = document.createElement('div');
            saleElement.innerHTML = `
                <div><strong>Продажа №${sale.id} в ${new Date(sale.created_at).toLocaleTimeString()} ${sale.user || 'Неизвестно'}</strong></div>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Товары</th>
                            <th>Кол-во</th>
                            <th>Цена</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${sale.items.map(item => `
                            <tr>
                                <td><img src="${item.thumbnail}" width="20" alt="Миниатюра"> ${item.custom_sku}</td>
                                <td>${item.quantity} шт.</td>
                                <td>${item.total_price} грн</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                <div class="text-end"><strong>Итого: ${sale.total_amount} грн</strong></div>
                <hr>
            `;
            salesList.appendChild(saleElement);
            totalItems += sale.items.reduce((sum, item) => sum + item.quantity, 0);
            totalAmount += sale.total_amount;
        });
        document.getElementById('daily-total-items').textContent = totalItems;
        document.getElementById('daily-total-amount').textContent = totalAmount;
    }

    window.checkAvailabilityAndAddItem = function(sku, price, stock, thumbnail, quantity) {
        const existingItem = [...selectedItems.querySelectorAll('tr')].find(row => row.querySelector('.selected-item-sku').textContent === sku);
        const currentStock = stock - parseInt(quantity);

        if (currentStock < 0) {
            showNotification('danger', 'Ошибка', `Недостаточно товара ${sku} на складе`);
        } else if (existingItem) {
            const existingQuantity = existingItem.querySelector('.quantity-display');
            const newQuantity = parseInt(existingQuantity.textContent) + quantity;
            if (newQuantity <= stock) {
                existingQuantity.textContent = newQuantity;
                updateTotal();
            } else {
                showNotification('danger', 'Ошибка', `Недостаточно товара ${sku} на складе`);
            }
        } else {
            const row = document.importNode(selectedItemTemplate, true);
            row.querySelector('.selected-item-thumbnail').src = thumbnail || '';
            row.querySelector('.selected-item-sku').textContent = sku;
            row.querySelector('.quantity-display').textContent = quantity;
            row.querySelector('.selected-item-price').textContent = price;
            const removeButton = row.querySelector('.selected-item-remove-button');
            const incrementButton = row.querySelector('.increment-button');
            const decrementButton = row.querySelector('.decrement-button');
            const quantityDisplay = row.querySelector('.quantity-display');

            incrementButton.addEventListener('click', () => {
                quantityDisplay.textContent = parseInt(quantityDisplay.textContent) + 1;
                updateTotal();
            });

            decrementButton.addEventListener('click', () => {
                if (parseInt(quantityDisplay.textContent) > 1) {
                    quantityDisplay.textContent = parseInt(quantityDisplay.textContent) - 1;
                    updateTotal();
                }
            });

            removeButton.addEventListener('click', () => removeItem(removeButton));

            selectedItems.appendChild(row);
            updateTotal();

            sendSocketMessage({
                'type': 'item_added',
                'custom_sku': sku
            });
        }
    };

    window.removeItem = function(button) {
        button.closest('tr').remove();
        updateTotal();
    };

    function updateTotal() {
        let total = 0;
        selectedItems.querySelectorAll('tr').forEach(row => {
            total += parseFloat(row.querySelector('.selected-item-price').textContent) * parseInt(row.querySelector('.quantity-display').textContent);
        });
        totalAmount.textContent = total;
        sendSocketMessage({
            'type': 'update_total',
            'total': total
        });
    }

    function getSelectedItems() {
        const items = [];
        selectedItems.querySelectorAll('tr').forEach(row => {
            items.push({
                custom_sku: row.querySelector('.selected-item-sku').textContent,
                quantity: parseInt(row.querySelector('.quantity-display').textContent),
                price: parseFloat(row.querySelector('.selected-item-price').textContent)
            });
        });
        console.log("Собранные товары для продажи: ", items);
        return items;
    }

    function updateTotalAmount(total) {
        totalAmount.textContent = total;
    }

    function showNotification(type, title, message) {
        const toastContainer = document.getElementById('notificationToast');
        const toastMessage = document.createElement('div');
        toastMessage.className = `toast align-items-center text-bg-${type} border-0`;
        toastMessage.setAttribute('role', 'alert');
        toastMessage.setAttribute('aria-live', 'assertive');
        toastMessage.setAttribute('aria-atomic', 'true');

        toastMessage.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${title}</strong>: ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toastContainer.appendChild(toastMessage);

        const toast = new bootstrap.Toast(toastMessage);
        toast.show();

        setTimeout(() => {
            toast.hide();
            toastMessage.remove();
        }, 2000);
    }

    function showConnectionLostModal() {
        const connectionLostModal = new bootstrap.Modal(document.getElementById('connectionLostModal'), {
            backdrop: 'static',
            keyboard: false
        });
        connectionLostModal.show();
    }

    function handleSellConfirmation(status) {
        if (status === 'success') {
            selectedItems.innerHTML = '';
            updateTotal();
            loadSalesList();
        }
    }

    function loadSalesList() {
        fetch('/seller_cabinet/sales/list/')
            .then(response => response.json())
            .then(data => {
                console.log("Список продаж загружен:", data);
                displaySalesList(data.sales);
            })
            .catch(error => console.error('Error loading sales list:', error));
    }

    loadSalesList();
});
