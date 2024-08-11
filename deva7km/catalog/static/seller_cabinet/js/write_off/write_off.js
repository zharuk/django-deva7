document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const selectedItems = document.getElementById('selected-items');
    const totalAmount = document.getElementById('total-amount');
    const writeOffButton = document.getElementById('write-off-button');
    const clearSearchButton = document.getElementById('clear-search');
    const clearCartButton = document.getElementById('clear-cart-button');
    const searchResultTemplate = document.getElementById('search-result-template').content;
    const selectedItemTemplate = document.getElementById('selected-item-template').content;
    const writeOffComment = document.getElementById('write-off-comment');
    const cartContainer = document.getElementById('cart-container');
    const writeOffsList = document.getElementById('write-offs-list');

    let socket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        socket = new WebSocket(`${protocol}//${window.location.host}/ws/write_off/`);

        socket.onopen = function() {
            requestWriteOffList();
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
                case 'write_off_confirmation':
                    showNotification('success', 'Списание завершено', 'Списание успешно завершено!');
                    handleWriteOffConfirmation(data.status);
                    break;
                case 'write_off_error':
                    showNotification('danger', 'Ошибка', data.message);
                    break;
                case 'item_added':
                    showNotification('success', 'Товар добавлен', `${data.custom_sku} добавлен в корзину для списания`);
                    break;
                case 'write_offs_list':
                    displayWriteOffList(data.write_offs);
                    break;
            }
        };

        socket.onclose = function() {
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
            socket.addEventListener('open', () => {
                socket.send(JSON.stringify(message));
            });
        }
    }

    function requestWriteOffList() {
        sendSocketMessage({ 'type': 'get_write_off_list' });
    }

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
        resetWriteOffFields();
        updateTotal();
    });

    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target)) {
            searchResults.classList.remove('show');
        }
    });

    writeOffButton.addEventListener('click', function() {
        const items = getSelectedItems();
        if (items.length === 0) {
            showNotification('warning', 'Ошибка', 'Корзина пуста');
        } else {
            const writeOffData = {
                'type': 'create_write_off',
                'user_id': 1,
                'telegram_user_id': null,
                'source': 'site',
                'comment': writeOffComment.value,
                'items': items
            };
            sendSocketMessage(writeOffData);
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

    function displayWriteOffList(writeOffs) {
        writeOffsList.innerHTML = '';
        if (writeOffs.length === 0) {
            writeOffsList.innerHTML = '<p>Списания отсутствуют.</p>';
        } else {
            let totalItems = 0;
            let totalAmount = 0;

            writeOffs.forEach(writeOff => {
                const writeOffTemplate = document.getElementById('write-off-item-template').content.cloneNode(true);
                writeOffTemplate.querySelector('.write-off-id').textContent = writeOff.id;
                writeOffTemplate.querySelector('.write-off-time').textContent = new Date(writeOff.created_at).toLocaleTimeString();
                writeOffTemplate.querySelector('.write-off-user').textContent = writeOff.user || 'Неизвестно';
                writeOffTemplate.querySelector('.write-off-total-amount').textContent = writeOff.total_amount;

                const writeOffProductsContainer = writeOffTemplate.querySelector('.write-off-products');
                writeOff.items.forEach(item => {
                    const productTemplate = document.getElementById('write-off-product-template').content.cloneNode(true);
                    const thumbnailElement = productTemplate.querySelector('.write-off-product-thumbnail');
                    if (item.thumbnail) {
                        thumbnailElement.src = item.thumbnail;
                    } else {
                        thumbnailElement.alt = 'Нет изображения';
                    }
                    productTemplate.querySelector('.write-off-product-sku').textContent = item.custom_sku;
                    productTemplate.querySelector('.write-off-product-quantity').textContent = `${item.quantity} шт.`;
                    productTemplate.querySelector('.write-off-product-price').textContent = `${item.total_price} грн`;
                    writeOffProductsContainer.appendChild(productTemplate);
                });

                writeOffsList.appendChild(writeOffTemplate);
                totalItems += writeOff.items.reduce((sum, item) => sum + item.quantity, 0);
                totalAmount += writeOff.total_amount;
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
            resetWriteOffFields();
        }
    };

    function updateTotal() {
        let total = 0;
        selectedItems.querySelectorAll('tr').forEach(row => {
            total += parseFloat(row.querySelector('.selected-item-price').textContent) * parseInt(row.querySelector('.quantity-display').textContent);
        });
        if (totalAmount) {
            totalAmount.textContent = total;
        } else {
            console.error("Element with id 'total-amount' not found.");
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
        } else {
            console.error("Element with id 'total-amount' not found.");
        }
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

    function handleWriteOffConfirmation(status) {
        if (status === 'success') {
            selectedItems.innerHTML = '';
            cartContainer.style.display = 'none';
            resetWriteOffFields();
            updateTotal();
            requestWriteOffList();
        }
    }

    function resetWriteOffFields() {
        writeOffComment.value = '';
    }
});
