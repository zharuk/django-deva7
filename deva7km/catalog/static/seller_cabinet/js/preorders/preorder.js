document.addEventListener("DOMContentLoaded", function() {
    const preordersContainer = document.getElementById("preorders-container");
    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    const refreshStatusButton = document.getElementById("refresh-status-btn");
    const toastContainer = document.querySelector('.toast-container');
    let activeFilter = 'all';
    let isWebSocketConnected = false;
    let socket;

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

    // Обработка нажатия кнопки обновления статусов
    refreshStatusButton.addEventListener('click', function() {
        if (isWebSocketConnected) {
            sendWebSocketMessage({ ttns: getTtns() });
        }
    });

    // Получение списка TTN из элементов на странице
    function getTtns() {
        return Array.from(document.querySelectorAll('[data-ttn]'))
            .map(el => el.getAttribute('data-ttn'))
            .filter(ttn => ttn);
    }

    // Функция отправки сообщения через WebSocket
    function sendWebSocketMessage(message) {
        const wsMessage = JSON.stringify(message);
        console.log("Sending WebSocket message:", wsMessage);
        socket.send(wsMessage);
    }

    // Установка WebSocket соединения
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        isWebSocketConnected = true;
        console.log("WebSocket connection opened");
        sendWebSocketMessage({ filter: activeFilter });
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("Received WebSocket message:", data);

        if (data.event) {
            if (data.event === 'preorder_list') {
                preordersContainer.innerHTML = data.html;
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
            } else if (data.event === 'preorder_saved' || data.event === 'preorder_updated') {
                const existingCard = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (existingCard) {
                    existingCard.outerHTML = data.html;
                } else {
                    preordersContainer.insertAdjacentHTML('afterbegin', data.html);
                }
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
            } else if (data.event === 'preorder_deleted') {
                const cardToRemove = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (cardToRemove) {
                    cardToRemove.remove();
                }
            } else if (data.event === 'update_complete') {
                const toast = document.createElement('div');
                toast.className = 'alert alert-dismissible alert-light';
                toast.innerHTML = `
                    <strong>Обновление завершено!</strong> ${data.message}
                `;
                toastContainer.appendChild(toast);

                setTimeout(() => {
                    toast.remove();
                }, 3000);
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
                sendWebSocketMessage({ type: 'toggle_receipt', id: id, status: status });
            });
        });

        container.querySelectorAll('.shipped-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                sendWebSocketMessage({ type: 'toggle_shipped', id: id, status: status });
            });
        });

        container.querySelectorAll('.payment-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                sendWebSocketMessage({ type: 'toggle_payment', id: id, status: status });
            });
        });
    }

    // Привязка события копирования данных к клику на элементе
    function bindCopyEvent(container) {
        container.querySelectorAll('.ttn-badge').forEach(badge => {
            badge.style.cursor = "pointer";  // Добавляем стиль курсора pointer
            badge.addEventListener('click', event => {
                const ttn = event.target.textContent.trim();
                navigator.clipboard.writeText(ttn).then(() => {
                    badge.classList.add('badge-copied');
                    setTimeout(() => {
                        badge.classList.remove('badge-copied');
                    }, 2000);

                    const toast = document.createElement('div');
                    toast.className = 'alert alert-dismissible alert-light';
                    toast.innerHTML = `
                        <strong>Скопировано!</strong> TTN: ${ttn}
                    `;
                    toastContainer.appendChild(toast);

                    setTimeout(() => {
                        toast.remove();
                    }, 2000);
                });
            });
        });
    }
});
