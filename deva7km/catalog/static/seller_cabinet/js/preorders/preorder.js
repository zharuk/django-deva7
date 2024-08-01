document.addEventListener("DOMContentLoaded", function() {
    const preordersContainer = document.getElementById("preorders-container");
    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    const refreshStatusButton = document.getElementById("refresh-status-btn");
    const toastContainer = document.querySelector('.toast-container');
    const userId = document.getElementById("user-id").value;
    let activeFilter = 'all';
    let isWebSocketConnected = false;
    let socket;

    if (!preordersContainer || !searchInput || !clearSearchButton || !refreshStatusButton || !toastContainer || !userId) {
        console.error("One or more elements not found in the DOM.");
        return;
    }

    // Функция обновления счетчиков вкладок
    function updateFilterCounts(counts) {
        if (counts) {
            document.querySelector('[data-filter="all"] .count').textContent = `(${counts.all})`;
            document.querySelector('[data-filter="not-shipped"] .count').textContent = `(${counts.not_shipped})`;
            document.querySelector('[data-filter="not-receipted"] .count').textContent = `(${counts.not_receipted})`;
            document.querySelector('[data-filter="not-paid"] .count').textContent = `(${counts.not_paid})`;
        }
    }

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
        message.user_id = userId;  // Добавляем идентификатор пользователя в сообщение
        const wsMessage = JSON.stringify(message);
        socket.send(wsMessage);
    }

    // Установка WebSocket соединения
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    // Обработка открытия соединения WebSocket
    socket.onopen = function() {
        isWebSocketConnected = true;
        sendWebSocketMessage({ filter: activeFilter });
    };

    // Обработка входящих сообщений WebSocket
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.event) {
            if (data.event === 'preorder_list') {
                preordersContainer.innerHTML = data.html;
                updateFilterCounts(data.counts);
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
            } else if (data.event === 'preorder_saved' || data.event === 'preorder_updated') {
                const existingCard = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (existingCard) {
                    existingCard.outerHTML = data.html;
                } else {
                    preordersContainer.insertAdjacentHTML('afterbegin', data.html);
                }
                updateFilterCounts(data.counts);
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
            } else if (data.event === 'preorder_deleted') {
                const cardToRemove = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (cardToRemove) {
                    cardToRemove.remove();
                }
                updateFilterCounts(data.counts);
            } else if (data.event === 'update_complete') {
                showNotification('success', 'Обновление завершено', data.message);
            }
        }
    };

    // Обработка закрытия соединения WebSocket
    socket.onclose = function() {
        isWebSocketConnected = false;
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

                    showNotification('success', 'Скопировано!', `TTN: ${ttn}`);
                });
            });
        });
    }

    function showNotification(type, title, message) {
        const toastContainer = document.getElementById('notificationToast');
        toastContainer.className = 'toast-container bg-' + type;
        document.getElementById('notificationMessage').textContent = message;
        toastContainer.style.display = 'block';

        setTimeout(() => {
            toastContainer.style.display = 'none';
        }, 2000);
    }
});
