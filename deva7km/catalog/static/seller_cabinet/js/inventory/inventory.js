document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const selectedItems = document.getElementById('selected-items');
    const totalAmount = document.getElementById('total-amount');
    const inventoryButton = document.getElementById('inventory-button');
    const clearSearchButton = document.getElementById('clear-search');
    const clearCartButton = document.getElementById('clear-cart-button');
    const searchResultTemplate = document.getElementById('search-result-template').content;
    const selectedItemTemplate = document.getElementById('selected-item-template').content;
    const inventoryComment = document.getElementById('inventory-comment');
    const cartContainer = document.getElementById('cart-container');
    const inventoriesList = document.getElementById('inventories-list');

    let socket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/inventory/`);

        socket.onopen = function() {
            requestInventoryList();
        };

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            switch (data.type) {
                case 'search_results':
                    displaySearchResults(data.results);
                    break;
                case 'update_total':
                    updateTotalAmount(data.total);
                    break;
                case 'inventory_confirmation':
                    showNotification('success', 'Оприходование завершено', 'Оприходование успешно завершено!');
                    handleInventoryConfirmation(data.status);
                    break;
                case 'inventory_error':
                    showNotification('danger', 'Ошибка', data.message);
                    break;
                case 'item_added':
                    showNotification('success', 'Товар добавлен', `${data.custom_sku} добавлен в корзину для оприходования`);
                    break;
                case 'inventories_list':
                    displayInventoryList(data.inventories);
                    break;
                default:
                    console.warn('Неизвестный тип сообщения:', data.type);
            }
        };

        socket.onclose = function() {
            showNotification('warning', 'Соединение закрыто', 'Соединение WebSocket закрыто');
            showConnectionLostModal();
            setTimeout(connectWebSocket, 1000);
        };

        socket.onerror = function(e) {
            showNotification('danger', 'Ошибка WebSocket', 'Произошла ошибка WebSocket. Подробности в консоли.');
        };
    }

    connectWebSocket();

    function sendSocketMessage(message) {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(message));
        } else {
            socket.addEventListener('open', () => {
                socket.send(JSON.stringify(message));
            });
        }
    }

    function requestInventoryList() {
        sendSocketMessage({ 'type': 'get_inventory_list' });
    }

    // Обработчик фокуса для поля ввода
    searchInput.addEventListener('focus', function() {
        const query = searchInput.value.trim();
        if (query.length >= 3) {
            sendSocketMessage({
                'type': 'search',
                'query': query
            });
        }
    });

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        if (query.length >= 3) {
            sendSocketMessage({
                'type': 'search',
                'query': query
            });
        } else {
            searchResults.innerHTML = '';
            searchResults.classList.remove('show');
        }
    });

    clearSearchButton.addEventListener('click', function() {
        searchInput.value = '';
        searchResults.innerHTML = '';
        searchResults.classList.remove('show');
    });

    clearCartButton.addEventListener('click', function() {
        selectedItems.innerHTML = '';
        cartContainer.style.display = 'none';
        resetInventoryFields();
        updateTotal();
    });

    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            searchResults.classList.remove('show');
        }
    });

    inventoryButton.addEventListener('click', function() {
        const items = getSelectedItems();
        if (items.length === 0) {
            showNotification('warning', 'Ошибка', 'Корзина пуста');
        } else {
            const inventoryData = {
                'type': 'create_inventory',
                'user_id': 1,
                'telegram_user_id': null,
                'source': 'site',
                'comment': inventoryComment.value,
                'items': items
            };
            sendSocketMessage(inventoryData);
        }
    });

    function displaySearchResults(results) {
        searchResults.innerHTML = '';
        if (results.length > 0) {
            results.forEach(item => {
                const row = document.importNode(searchResultTemplate, true);
                row.querySelector('.search-item-thumbnail').src = item.thumbnail || '';
                row.querySelector('.search-item-sku').textContent = item.sku;
                row.querySelector('.item-details').textContent = `👗- ${item.stock} шт, 💵- ${item.price} грн`;

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

                addButton.addEventListener('click', () => addItem(item.sku, item.price, item.thumbnail, parseInt(quantityDisplay.textContent)));
                searchResults.appendChild(row);
            });
        } else {
            const noResultsMessage = document.createElement('div');
            noResultsMessage.textContent = 'Нет соответствия';
            noResultsMessage.classList.add('no-results-message');
            searchResults.appendChild(noResultsMessage);
        }
        searchResults.classList.add('show');
    }

    function displayInventoryList(inventories) {
        inventoriesList.innerHTML = '';
        if (inventories.length === 0) {
            inventoriesList.innerHTML = '<p>Оприходования отсутствуют.</p>';
        } else {
            let totalItems = 0;
            let totalAmount = 0;

            inventories.forEach(inventory_obj => {
                const inventoryTemplate = document.getElementById('inventory-item-template').content.cloneNode(true);
                inventoryTemplate.querySelector('.inventory-id').textContent = inventory_obj.id;
                inventoryTemplate.querySelector('.inventory-time').textContent = new Date(inventory_obj.created_at).toLocaleTimeString();
                inventoryTemplate.querySelector('.inventory-user').textContent = inventory_obj.user || 'Неизвестно';
                inventoryTemplate.querySelector('.inventory-total-amount').textContent = inventory_obj.total_amount;

                const inventoryProductsContainer = inventoryTemplate.querySelector('.inventory-products');
                inventory_obj.items.forEach(item => {
                    const productTemplate = document.getElementById('inventory-product-template').content.cloneNode(true);
                    const thumbnailElement = productTemplate.querySelector('.inventory-product-thumbnail');
                    if (item.thumbnail) {
                        thumbnailElement.src = item.thumbnail;
                    } else {
                        thumbnailElement.alt = 'Нет изображения';
                    }
                    productTemplate.querySelector('.inventory-product-sku').textContent = item.custom_sku;
                    productTemplate.querySelector('.inventory-product-quantity').textContent = `${item.quantity} шт.`;
                    productTemplate.querySelector('.inventory-product-price').textContent = `${item.total_price} грн`;
                    inventoryProductsContainer.appendChild(productTemplate);
                });

                inventoriesList.appendChild(inventoryTemplate);
                totalItems += inventory_obj.items.reduce((sum, item) => sum + item.quantity, 0);
                totalAmount += inventory_obj.total_amount;
            });

            document.getElementById('daily-total-items').textContent = totalItems;
            document.getElementById('daily-total-amount').textContent = totalAmount;
        }
    }

    window.addItem = function(sku, price, thumbnail, quantity) {
        const existingItem = [...selectedItems.querySelectorAll('tr')].find(row => row.querySelector('.selected-item-sku').textContent === sku);

        if (existingItem) {
            const existingQuantity = existingItem.querySelector('.quantity-display');
            existingQuantity.textContent = parseInt(existingQuantity.textContent) + quantity;
            updateTotal();
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
            cartContainer.style.display = 'block';
            updateTotal();

            sendSocketMessage({
                'type': 'item_added',
                'custom_sku': sku
            });

            if (searchInput.value.trim() !== '') {
                searchResults.classList.add('show');
            }
        }
    };

    window.removeItem = function(button) {
        button.closest('tr').remove();
        updateTotal();
        if (selectedItems.children.length === 0) {
            cartContainer.style.display = 'none';
            resetInventoryFields();
        }
    };

    function updateTotal() {
        let total = 0;
        selectedItems.querySelectorAll('tr').forEach(row => {
            total += parseFloat(row.querySelector('.selected-item-price').textContent) * parseInt(row.querySelector('.quantity-display').textContent);
        });
        if (totalAmount) {
            totalAmount.textContent = total;
        }
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
        return items;
    }

    function updateTotalAmount(total) {
        if (totalAmount) {
            totalAmount.textContent = total;
        }
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

    function handleInventoryConfirmation(status) {
        if (status === 'success') {
            selectedItems.innerHTML = '';
            cartContainer.style.display = 'none';
            resetInventoryFields();
            updateTotal();
            requestInventoryList();
        }
    }

    function resetInventoryFields() {
        inventoryComment.value = '';
    }

    requestInventoryList();
});
