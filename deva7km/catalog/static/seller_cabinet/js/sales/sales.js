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
    const saleType = document.getElementById('sale-type');
    const saleComment = document.getElementById('sale-comment');
    const cartContainer = document.getElementById('cart-container');

    let socket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/sales/`);

        socket.onopen = function() {
            requestSalesList();
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
                case 'sell_confirmation':
                    showNotification('success', 'Продажа завершена', 'Продажа успешно завершена!');
                    handleSellConfirmation(data.status);
                    requestSalesList();
                    break;
                case 'sell_error':
                    showNotification('danger', 'Ошибка', data.message);
                    break;
                case 'item_added':
                    showNotification('success', 'Товар добавлен', `${data.custom_sku} добавлен в корзину`);
                    break;
                case 'item_not_available':
                    showNotification('danger', 'Ошибка', `Товар ${data.custom_sku} отсутствует на складе`);
                    updateItemStock(data.custom_sku, data.available_stock);  // Обновляем количество товара в интерфейсе
                    break;
                case 'sales_list':
                    displaySalesList(data.sales);
                    break;
                default:
                    console.warn('Неизвестный тип сообщения:', data.type);
            }
        };

        socket.onclose = function(e) {
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
        }
    }

    function requestSalesList() {
        sendSocketMessage({ 'type': 'get_sales_list' });
    }

    searchInput.addEventListener('focus', function() {
        const query = searchInput.value.trim();
        if (query.length >= 3) {
            sendSocketMessage({
                'type': 'search',
                'query': query
            });
        }
    });

    searchInput.addEventListener('focus', function() {
        if (searchResults.innerHTML !== '') {
            searchResults.classList.add('show');
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
        resetSaleFields();
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
                'payment_method': saleType.value,
                'comment': saleComment.value,
                'items': items
            };
            sendSocketMessage(saleData);
        }
    });

    function displaySearchResults(results) {
        searchResults.innerHTML = '';
        if (results.length > 0) {
            results.forEach(item => {
                const row = document.importNode(searchResultTemplate, true);
                row.querySelector('.search-item-thumbnail').src = item.thumbnail || '';
                row.querySelector('.search-item-sku').textContent = item.custom_sku;
                row.querySelector('.item-details').textContent = `👗- ${item.stock} шт, 💵- ${Math.floor(item.price)} грн`;

                const addButton = row.querySelector('.search-item-add-button');
                const quantityDisplay = row.querySelector('.quantity-display');
                const incrementButton = row.querySelector('.increment-button');
                const decrementButton = row.querySelector('.decrement-button');

                incrementButton.addEventListener('click', () => {
                    if (parseInt(quantityDisplay.textContent) < item.stock) {
                        quantityDisplay.textContent = parseInt(quantityDisplay.textContent) + 1;
                    } else {
                        showNotification('danger', 'Ошибка', `Товара ${item.custom_sku} больше нет на складе`);
                    }
                });

                decrementButton.addEventListener('click', () => {
                    if (parseInt(quantityDisplay.textContent) > 1) {
                        quantityDisplay.textContent = parseInt(quantityDisplay.textContent) - 1;
                    }
                });

                addButton.addEventListener('click', () => checkAvailabilityAndAddItem(item.custom_sku, Math.floor(item.price), item.stock, item.thumbnail, parseInt(quantityDisplay.textContent)));
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

    function displaySalesList(sales) {
        const salesList = document.getElementById('sales-list');
        salesList.innerHTML = '';

        if (sales.length === 0) {
            salesList.innerHTML = '<p>Продажи отсутствуют.</p>';
        } else {
            let totalItems = 0;
            let totalAmount = 0;

            sales.forEach(sale => {
                const saleTemplate = document.getElementById('sale-item-template').content.cloneNode(true);
                saleTemplate.querySelector('.sale-id').textContent = sale.id;
                saleTemplate.querySelector('.sale-time').textContent = new Date(sale.created_at).toLocaleTimeString();
                saleTemplate.querySelector('.sale-user').textContent = sale.user || 'Неизвестно';
                saleTemplate.querySelector('.sale-total-amount').textContent = Math.floor(sale.total_amount);
                saleTemplate.querySelector('.sale-type').textContent = sale.payment_method;

                if (sale.comment) {
                    saleTemplate.querySelector('.sale-comment').textContent = sale.comment;
                } else {
                    saleTemplate.querySelector('.sale-comment-container').style.display = 'none';
                }

                const saleProductsContainer = saleTemplate.querySelector('.sale-products');
                sale.items.forEach(item => {
                    const productTemplate = document.getElementById('sale-product-template').content.cloneNode(true);
                    productTemplate.querySelector('.sale-product-thumbnail').src = item.thumbnail;
                    productTemplate.querySelector('.sale-product-sku').textContent = item.custom_sku;
                    productTemplate.querySelector('.sale-product-quantity').textContent = `${item.quantity} шт.`;
                    productTemplate.querySelector('.sale-product-price').textContent = `${Math.floor(item.total_price)} грн`;
                    saleProductsContainer.appendChild(productTemplate);
                });

                salesList.appendChild(saleTemplate);
                totalItems += sale.items.reduce((sum, item) => sum + item.quantity, 0);
                totalAmount += sale.total_amount;
            });

            document.getElementById('daily-total-items').textContent = totalItems;
            document.getElementById('daily-total-amount').textContent = Math.floor(totalAmount);
        }
    }

    window.checkAvailabilityAndAddItem = function(sku, price, stock, thumbnail, quantity) {
        const existingItem = [...selectedItems.querySelectorAll('tr')].find(row => row.querySelector('.selected-item-sku').textContent === sku);

        if (existingItem) {
            const existingQuantity = existingItem.querySelector('.quantity-display');
            const totalElement = existingItem.querySelector('.selected-item-total');
            const newQuantity = parseInt(existingQuantity.textContent) + quantity;

            if (newQuantity <= stock) {
                existingQuantity.textContent = newQuantity;
                totalElement.textContent = Math.floor(price * newQuantity);
                updateTotal();
            } else {
                showNotification('danger', 'Ошибка', `Недостаточно товара ${sku} на складе`);
            }
        } else if (quantity <= stock) {
            const row = document.importNode(selectedItemTemplate, true);
            row.querySelector('.selected-item-thumbnail').src = thumbnail || '';
            row.querySelector('.selected-item-sku').textContent = sku;
            row.querySelector('.quantity-display').textContent = quantity;
            row.querySelector('.selected-item-total').textContent = Math.floor(price * quantity);

            const incrementButton = row.querySelector('.increment-button');
            const decrementButton = row.querySelector('.decrement-button');
            const removeButton = row.querySelector('.selected-item-remove-button');
            const quantityDisplay = row.querySelector('.quantity-display');
            const totalElement = row.querySelector('.selected-item-total');

            incrementButton.addEventListener('click', () => {
                const currentQuantity = parseInt(quantityDisplay.textContent);
                if (currentQuantity < stock) {
                    quantityDisplay.textContent = currentQuantity + 1;
                    totalElement.textContent = Math.floor(price * (currentQuantity + 1));
                    updateTotal();
                } else {
                    showNotification('danger', 'Ошибка', `Товара ${sku} больше нет на складе`);
                }
            });

            decrementButton.addEventListener('click', () => {
                if (parseInt(quantityDisplay.textContent) > 1) {
                    quantityDisplay.textContent = parseInt(quantityDisplay.textContent) - 1;
                    totalElement.textContent = Math.floor(price * parseInt(quantityDisplay.textContent));
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
        } else {
            showNotification('danger', 'Ошибка', `Недостаточно товара ${sku} на складе`);
        }
    };

    window.removeItem = function(button) {
        button.closest('tr').remove();
        updateTotal();
        if (selectedItems.children.length === 0) {
            cartContainer.style.display = 'none';
            resetSaleFields();
        }
    };

    function updateTotal() {
        let total = 0;
        selectedItems.querySelectorAll('tr').forEach(row => {
            const priceElement = row.querySelector('.selected-item-total');
            const quantityElement = row.querySelector('.quantity-display');

            if (priceElement && quantityElement) {
                total += parseInt(priceElement.textContent, 10);
            }
        });

        totalAmount.textContent = Math.floor(total);
        sendSocketMessage({
            'type': 'update_total',
            'total': total
        });
    }

    function getSelectedItems() {
        const items = [];
        selectedItems.querySelectorAll('tr').forEach(row => {
            const skuElement = row.querySelector('.selected-item-sku');
            const quantityElement = row.querySelector('.quantity-display');
            const totalElement = row.querySelector('.selected-item-total');

            if (skuElement && quantityElement && totalElement) {
                items.push({
                    custom_sku: skuElement.textContent.trim(),
                    quantity: parseInt(quantityElement.textContent.trim(), 10),
                    total: parseInt(totalElement.textContent.trim(), 10)
                });
            }
        });
        return items;
    }

    function updateTotalAmount(total) {
        totalAmount.textContent = Math.floor(total);
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
            cartContainer.style.display = 'none';
            resetSaleFields();
            updateTotal();
            requestSalesList();
        }
    }

    function resetSaleFields() {
        saleType.value = 'cash';
        saleComment.value = '';
    }

    requestSalesList();
});
