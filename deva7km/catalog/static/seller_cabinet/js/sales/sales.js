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
    const salesList = document.getElementById('sales-list');
    const saleItemTemplate = document.getElementById('sale-item-template').content;
    const saleProductTemplate = document.getElementById('sale-product-template').content;

    let socket;

    function connectWebSocket() {
        socket = new WebSocket('wss://' + window.location.host + '/ws/sales/');

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log("Получены данные от сервера:", data);
            switch (data.type) {
                case 'search_results':
                    displaySearchResults(data.results);
                    break;
                case 'update_total':
                    updateTotalAmount(data.total);
                    break;
                case 'sell_confirmation':
                    showNotification('success', 'Продажа завершена', 'Продажа успешно завершена!');
                    handleSellConfirmation(data.status);
                    loadSalesList(); // Обновляем список продаж после завершения продажи
                    break;
                case 'sell_error':
                    showNotification('danger', 'Ошибка', data.message);
                    break;
                case 'item_added':
                    showNotification('success', 'Товар добавлен', `${data.custom_sku} добавлен в корзину`);
                    break;
                case 'item_not_available':
                    showNotification('danger', 'Ошибка', `Товар ${data.custom_sku} отсутствует на складе`);
                    break;
                case 'sales_list':
                    displaySalesList(data.sales);
                    break;
                default:
                    console.warn('Неизвестный тип данных:', data.type);
            }
        };

        socket.onclose = function() {
            console.error('WebSocket закрыт неожиданно, повторное подключение...');
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
            row.querySelector('.search-item-stock').textContent = `${item.stock} шт`;
            row.querySelector('.search-item-price').textContent = `${item.price} грн`;
            const addButton = row.querySelector('.search-item-add-button');
            addButton.addEventListener('click', () => checkAvailabilityAndAddItem(item.sku, item.price, item.stock, item.thumbnail));
            searchResults.appendChild(row);
        });
        searchResults.classList.add('show');
    }

    function displaySalesList(sales) {
        salesList.innerHTML = '';
        sales.forEach(sale => {
            const saleElement = document.importNode(saleItemTemplate, true);
            saleElement.querySelector('.sale-id').textContent = sale.id;
            saleElement.querySelector('.sale-time').textContent = new Date(sale.created_at).toLocaleTimeString();
            saleElement.querySelector('.sale-user').textContent = sale.user || 'Неизвестно';
            const saleProductsContainer = saleElement.querySelector('.sale-products');

            sale.items.forEach(item => {
                const productElement = document.importNode(saleProductTemplate, true);
                productElement.querySelector('.sale-product-thumbnail').src = item.thumbnail || '';
                productElement.querySelector('.sale-product-sku').textContent = item.custom_sku;
                productElement.querySelector('.sale-product-quantity').textContent = `${item.quantity} шт.`;
                productElement.querySelector('.sale-product-price').textContent = `${item.total_price} грн`;
                saleProductsContainer.appendChild(productElement);
            });

            saleElement.querySelector('.sale-total-amount').textContent = `${sale.total_amount} грн`;
            salesList.appendChild(saleElement);
        });
    }

    window.checkAvailabilityAndAddItem = function(sku, price, stock, thumbnail) {
        if (stock <= 0) {
            showNotification('danger', 'Ошибка', `Товар ${sku} отсутствует на складе`);
        } else {
            const row = document.importNode(selectedItemTemplate, true);
            row.querySelector('.selected-item-thumbnail').src = thumbnail || '';
            row.querySelector('.selected-item-sku').textContent = sku;
            row.querySelector('.selected-item-price').textContent = price;
            const removeButton = row.querySelector('.selected-item-remove-button');
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
            total += parseFloat(row.querySelector('.selected-item-price').textContent);
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
                quantity: parseInt(row.querySelector('.selected-item-quantity').textContent),
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
        const toastMessage = document.getElementById('notificationMessage');
        toastMessage.innerHTML = `
            <div class="toast show align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>${title}</strong>: ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        toastContainer.style.display = 'block';

        setTimeout(() => {
            toastContainer.style.display = 'none';
        }, 2000);
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
