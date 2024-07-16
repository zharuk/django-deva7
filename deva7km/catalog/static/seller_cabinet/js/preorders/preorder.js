document.addEventListener("DOMContentLoaded", function() {
    const preordersContainer = document.getElementById("preorders-container");
    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    let activeFilter = 'all';
    let isWebSocketConnected = false;

    // Обработка кликов по кнопкам фильтров
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            activeFilter = this.getAttribute('data-filter');
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            if (isWebSocketConnected) {
                sendWebSocketMessage({ filter: activeFilter });
            }
        });
    });

    // Обработка ввода текста в поле поиска
    searchInput.addEventListener('input', function() {
        if (isWebSocketConnected) {
            sendWebSocketMessage({ search_text: this.value });
        }
    });

    // Обработка нажатия кнопки очистки поля поиска
    clearSearchButton.addEventListener('click', function() {
        searchInput.value = '';
        if (isWebSocketConnected) {
            sendWebSocketMessage({ search_text: '' });
        }
    });

    // Функция отправки сообщения через WebSocket
    function sendWebSocketMessage(message) {
        const wsMessage = JSON.stringify(message);
        console.log("Sending WebSocket message:", wsMessage);
        socket.send(wsMessage);
    }

    // Установка WebSocket соединения
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    let socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        isWebSocketConnected = true;
        console.log("WebSocket connection opened");
        sendWebSocketMessage({ filter: activeFilter });
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("Received WebSocket message:", data);

        if (data.event) {
            console.log("Received HTML:", data.html);
            if (data.event === 'preorder_list') {
                console.log("Updating preorder list");
                preordersContainer.innerHTML = data.html;
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
                console.log("Updated DOM:", preordersContainer.innerHTML);
            } else if (data.event === 'preorder_saved' || data.event === 'preorder_updated') {
                console.log(`Preorder ${data.event}:`, data.preorder_id);
                const existingCard = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (existingCard) {
                    existingCard.outerHTML = data.html;
                } else {
                    preordersContainer.insertAdjacentHTML('afterbegin', data.html);
                }
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
                console.log("Updated DOM:", preordersContainer.innerHTML);
            } else if (data.event === 'preorder_deleted') {
                console.log(`Preorder deleted:`, data.preorder_id);
                const cardToRemove = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (cardToRemove) {
                    cardToRemove.remove();
                }
            }
        }
    };

    socket.onclose = function() {
        isWebSocketConnected = false;
        console.log("WebSocket connection closed");
    };

    // Привязка событий к переключателям
    function bindSwitchEvents(container) {
        container.querySelectorAll('.receipt-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                console.log(`Toggle receipt for preorder ${id}: ${status}`);
                sendWebSocketMessage({ type: 'toggle_receipt', id: id, status: status });
            });
        });

        container.querySelectorAll('.shipped-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                console.log(`Toggle shipped for preorder ${id}: ${status}`);
                sendWebSocketMessage({ type: 'toggle_shipped', id: id, status: status });
            });
        });

        container.querySelectorAll('.payment-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                console.log(`Toggle payment for preorder ${id}: ${status}`);
                sendWebSocketMessage({ type: 'toggle_payment', id: id, status: status });
            });
        });
    }

    // Привязка события копирования данных к клику на элементе
    function bindCopyEvent(container) {
        container.querySelectorAll('.ttn-badge').forEach(badge => {
            badge.addEventListener('click', event => {
                const ttn = event.target.textContent.trim();
                navigator.clipboard.writeText(ttn).then(() => {
                    console.log(`TTN copied: ${ttn}`);
                    badge.classList.add('badge-copied');
                    setTimeout(() => {
                        badge.classList.remove('badge-copied');
                    }, 2000);

                    const toast = document.createElement('div');
                    toast.className = 'alert alert-dismissible alert-light';
                    toast.innerHTML = `
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        <strong>Скопировано!</strong> TTN: ${ttn}
                    `;
                    const toastContainer = document.querySelector('.toast-container');
                    toastContainer.appendChild(toast);

                    // Удаляем алерт через 2 секунды
                    setTimeout(() => {
                        toast.remove();
                    }, 2000);
                });
            });
        });
    }
});
