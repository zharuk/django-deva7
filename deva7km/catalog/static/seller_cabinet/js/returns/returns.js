document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const selectedItems = document.getElementById('selected-items');
    const totalAmount = document.getElementById('total-amount');
    const returnButton = document.getElementById('return-button');
    const clearSearchButton = document.getElementById('clear-search');
    const clearCartButton = document.getElementById('clear-cart-button');
    const searchResultTemplate = document.getElementById('search-result-template').content;
    const selectedItemTemplate = document.getElementById('selected-item-template').content;
    const returnComment = document.getElementById('return-comment');
    const cartContainer = document.getElementById('cart-container');
    const returnsList = document.getElementById('returns-list');

    let socket;

    // Функция подключения WebSocket
    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/returns/`);

        socket.onopen = function() {
            requestReturnsList();
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
                case 'return_confirmation':
                    showNotification('success', 'Возврат завершен', 'Возврат успешно завершен!');
                    handleReturnConfirmation(data.status);
                    break;
                case 'return_error':
                    showNotification('danger', 'Ошибка', data.message);
                    break;
                case 'item_added':
                    showNotification('success', 'Товар добавлен', `${data.custom_sku} добавлен в корзину для возврата`);
                    break;
                case 'returns_list':
                    displayReturnsList(data.returns);
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

    function requestReturnsList() {
        sendSocketMessage({ 'type': 'get_returns_list' });
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
        resetReturnFields();
        updateTotal();
    });

    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            searchResults.classList.remove('show');
        }
    });

    returnButton.addEventListener('click', function() {
        const items = getSelectedItems();
        if (items.length === 0) {
            showNotification('warning', 'Ошибка', 'Корзина пуста');
        } else {
            const returnData = {
                'type': 'create_return',
                'user_id': 1,
                'telegram_user_id': null,
                'source': 'site',
                'comment': returnComment.value,
                'items': items
            };
            sendSocketMessage(returnData);
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

                addButton.addEventListener('click', () => addItem(item.sku, parseFloat(item.price), item.thumbnail, parseInt(quantityDisplay.textContent)));
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

    function displayReturnsList(returns) {
        returnsList.innerHTML = '';
        if (returns.length === 0) {
            returnsList.innerHTML = '<p>Возвраты отсутствуют.</p>';
        } else {
            let totalItems = 0;
            let totalAmount = 0;

            returns.forEach(return_obj => {
                const returnTemplate = document.getElementById('return-item-template').content.cloneNode(true);
                returnTemplate.querySelector('.return-id').textContent = return_obj.id;
                returnTemplate.querySelector('.return-time').textContent = new Date(return_obj.created_at).toLocaleTimeString();
                returnTemplate.querySelector('.return-user').textContent = return_obj.user || 'Неизвестно';
                returnTemplate.querySelector('.return-total-amount').textContent = return_obj.total_amount;

                const commentContainer = returnTemplate.querySelector('.return-comment-container');
                const commentElement = commentContainer.querySelector('.return-comment');
                if (return_obj.comment) {
                    commentElement.textContent = return_obj.comment;
                    commentContainer.style.display = 'block';
                } else {
                    commentContainer.style.display = 'none';
                }

                const returnProductsContainer = returnTemplate.querySelector('.return-products');
                return_obj.items.forEach(item => {
                    const productTemplate = document.getElementById('return-product-template').content.cloneNode(true);
                    const thumbnailElement = productTemplate.querySelector('.return-product-thumbnail');
                    if (item.thumbnail) {
                        thumbnailElement.src = item.thumbnail;
                    } else {
                        thumbnailElement.alt = 'Нет изображения';
                    }
                    productTemplate.querySelector('.return-product-sku').textContent = item.custom_sku;
                    productTemplate.querySelector('.return-product-quantity').textContent = `${item.quantity} шт.`;
                    productTemplate.querySelector('.return-product-price').textContent = `${formatPrice(item.total_price)} грн`;
                    returnProductsContainer.appendChild(productTemplate);
                });

                returnsList.appendChild(returnTemplate);
                totalItems += return_obj.items.reduce((sum, item) => sum + item.quantity, 0);
                totalAmount += return_obj.total_amount;
            });

            document.getElementById('daily-total-items').textContent = totalItems;
            document.getElementById('daily-total-amount').textContent = formatPrice(totalAmount);
        }
    }

    function formatPrice(price) {
        const numericPrice = parseFloat(price);
        return numericPrice % 1 === 0 ? numericPrice.toFixed(0) : numericPrice.toFixed(2);
    }

    window.addItem = function(sku, price, thumbnail, quantity) {
        const existingItem = [...selectedItems.querySelectorAll('tr')].find(row => row.querySelector('.selected-item-sku').textContent === sku);

        if (existingItem) {
            const existingQuantity = existingItem.querySelector('.quantity-display');
            existingQuantity.textContent = parseInt(existingQuantity.textContent) + quantity;

            const totalPriceElement = existingItem.querySelector('.selected-item-price');
            const newTotalPrice = (parseInt(existingQuantity.textContent) * parseFloat(price)).toFixed(2);
            totalPriceElement.textContent = formatPrice(newTotalPrice);

            updateTotal();
        } else {
            const row = document.importNode(selectedItemTemplate, true);
            row.querySelector('.selected-item-thumbnail').src = thumbnail || '';
            row.querySelector('.selected-item-sku').textContent = sku;
            row.querySelector('.quantity-display').textContent = quantity;

            const totalPriceElement = row.querySelector('.selected-item-price');
            totalPriceElement.textContent = formatPrice(quantity * price);

            const removeButton = row.querySelector('.selected-item-remove-button');
            const incrementButton = row.querySelector('.increment-button');
            const decrementButton = row.querySelector('.decrement-button');
            const quantityDisplay = row.querySelector('.quantity-display');

            incrementButton.addEventListener('click', () => {
                quantityDisplay.textContent = parseInt(quantityDisplay.textContent) + 1;
                totalPriceElement.textContent = formatPrice(parseInt(quantityDisplay.textContent) * parseFloat(price));
                updateTotal();
            });

            decrementButton.addEventListener('click', () => {
                if (parseInt(quantityDisplay.textContent) > 1) {
                    quantityDisplay.textContent = parseInt(quantityDisplay.textContent) - 1;
                    totalPriceElement.textContent = formatPrice(parseInt(quantityDisplay.textContent) * parseFloat(price));
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
            resetReturnFields();
        }
    };

    function updateTotal() {
        let total = 0;
        selectedItems.querySelectorAll('tr').forEach(row => {
            const price = parseFloat(row.querySelector('.selected-item-price').textContent);
            const quantity = parseInt(row.querySelector('.quantity-display').textContent);
            total += price * quantity;
        });
        if (totalAmount) {
            totalAmount.textContent = formatPrice(total);
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
            totalAmount.textContent = formatPrice(total);
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

    function handleReturnConfirmation(status) {
        if (status === 'success') {
            selectedItems.innerHTML = '';
            cartContainer.style.display = 'none';
            resetReturnFields();
            updateTotal();
            requestReturnsList();
        }
    }

    function resetReturnFields() {
        returnComment.value = '';
    }

    requestReturnsList();
});
