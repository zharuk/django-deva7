document.addEventListener("DOMContentLoaded", function() {

    const preordersContainer = document.getElementById("preorders-container");

    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    const refreshStatusButton = document.getElementById("refresh-status-btn");
    const createPreorderBtn = document.getElementById("create-preorder-btn");
    const preorderModalElement = document.getElementById('preorderModal');
    const preorderModal = new bootstrap.Modal(preorderModalElement);
    const preorderForm = document.getElementById('preorder-form');
    const deletePreorderBtn = document.getElementById('delete-preorder-btn');
    const userId = document.getElementById("user-id") ? document.getElementById("user-id").value : null;
    const spinnerCreatePreorder = document.getElementById("spinner-create-preorder");
    const spinnerRefreshStatus = document.getElementById("spinner-refresh-status");
    const spinnerSavePreorder = document.getElementById("spinner-save-preorder");

    // Элементы для модального окна подтверждения удаления
    const confirmDeleteModalElement = document.getElementById('confirmDeleteModal');
    const confirmDeleteModal = new bootstrap.Modal(confirmDeleteModalElement);
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    let preorderIdToDelete = null; // Переменная для хранения ID предзаказа для удаления

    let activeFilter = 'all';
    let isWebSocketConnected = false;
    let socket;

    // Вспомогательная функция для управления отображением спиннера
    function toggleSpinner(spinner, show) {
        if (show) {
            spinner.classList.remove('d-none');
        } else {
            spinner.classList.add('d-none');
        }
    }

    if (!searchInput || !clearSearchButton || !refreshStatusButton) {
        return;
    }

    // Проверка наличия элемента модального окна
    if (!preorderModalElement) {
        console.error('Элемент модального окна не найден');
        return;
    }

    preorderModalElement.addEventListener('shown.bs.modal', function () {
        const textArea = document.getElementById('text');
        autoResizeTextArea(textArea);
        textArea.addEventListener('input', function() {
            autoResizeTextArea(textArea);
        });
    });

    function updateFilterCounts(counts) {
        if (counts) {
            document.querySelector('[data-filter="all"] .count').textContent = `(${counts.all})`;
            document.querySelector('[data-filter="not-shipped"] .count').textContent = `(${counts.not_shipped})`;
            document.querySelector('[data-filter="not-receipted"] .count').textContent = `(${counts.not_receipted})`;
            document.querySelector('[data-filter="not-paid"] .count').textContent = `(${counts.not_paid})`;
        }
    }

    function openPreorderModal(preorderId = null) {
        toggleSpinner(spinnerCreatePreorder, true); // Показать спиннер при открытии модального окна
        if (preorderId) {
            sendWebSocketMessage({
                type: 'get_preorder',
                id: preorderId,
                user_id: userId
            });
        } else {
            preorderForm.reset();
            preorderForm.dataset.id = '';
            deletePreorderBtn.classList.add('d-none');
            preorderModal.show();
            toggleSpinner(spinnerCreatePreorder, false); // Скрыть спиннер после загрузки модального окна
        }
    }

    createPreorderBtn.addEventListener('click', function() {
        openPreorderModal();
    });

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            activeFilter = this.getAttribute('data-filter');

            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            if (isWebSocketConnected) {
                sendWebSocketMessage({ type: 'filter', filter: activeFilter });
            } else {
                showNotification('warning', 'Ошибка', 'WebSocket не подключен.');
            }
        });
    });

    searchInput.addEventListener('input', function() {
        if (isWebSocketConnected) {
            const searchText = this.value;
            const message = { type: 'search', search_text: searchText };
            sendWebSocketMessage(message);
        }
    });

    clearSearchButton.addEventListener('click', function() {
        searchInput.value = '';
        activeFilter = 'all';  // Устанавливаем активный фильтр на "Все"
        filterButtons.forEach(button => {
            if (button.getAttribute('data-filter') === 'all') {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
        if (isWebSocketConnected) {
            sendWebSocketMessage({ type: 'search', search_text: '' });
            sendWebSocketMessage({ type: 'filter', filter: activeFilter });  // Отправляем обновленный фильтр
        }
    });

    refreshStatusButton.addEventListener('click', function() {
        toggleSpinner(spinnerRefreshStatus, true); // Показать спиннер при обновлении статусов
        if (isWebSocketConnected) {
            sendWebSocketMessage({
                type: 'update_ttns',
                ttns: getTtns()
            });
        }
    });

    function getTtns() {
        return Array.from(document.querySelectorAll('[data-ttn]'))
            .map(el => el.getAttribute('data-ttn'))
            .filter(ttn => ttn);
    }

    // Вспомогательная функция для отправки сообщения WebSocket
    function sendWebSocketMessage(message) {
        message.user_id = userId;
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(message));
        } else {
            console.error('WebSocket не подключен');
            showNotification('error', 'Ошибка', 'WebSocket не подключен');
        }
    }

    // Удаление предзаказа (после подтверждения)
    confirmDeleteBtn.addEventListener('click', function() {
        if (preorderIdToDelete) {
            sendWebSocketMessage({
                type: 'delete',
                id: preorderIdToDelete,
                user_id: userId
            });
            confirmDeleteModal.hide();
            preorderModal.hide();
        }
    });

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        isWebSocketConnected = true;
        sendWebSocketMessage({ type: 'filter', filter: 'all' });
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.event === 'get_preorder') {
            preloadPreorderForm(data);
            preorderModal.show();
            toggleSpinner(spinnerCreatePreorder, false); // Скрыть спиннер после загрузки данных
        } else if (data.event === 'preorder_list') {
            updatePreorderList(data);
        } else if (data.event === 'form_invalid') {
            showNotification('danger', 'Ошибка', 'Проверьте введенные данные.');
        } else if (data.event === 'update_complete') {
            showNotification('success', 'Обновление', data.message);
            toggleSpinner(spinnerRefreshStatus, false); // Скрыть спиннер после обновления статусов
        }
    };

    socket.onclose = function() {
        isWebSocketConnected = false;
        showConnectionLostModal();
    };

    function updatePreorderList(data) {
        if (data.html && data.counts) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = data.html;

            const newContent = tempDiv.querySelector('#preorders-container');
            if (newContent) {
                preordersContainer.innerHTML = newContent.innerHTML;
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
                updateFilterCounts(data.counts);
            } else {
                preordersContainer.innerHTML = '';
                updateFilterCounts(data.counts);
            }
        } else {
            preordersContainer.innerHTML = '';
            updateFilterCounts(data.counts);
        }

        if (data.additional_event === 'preorder_saved') {
            showNotification('success', 'Успех', 'Предзаказ успешно сохранен.');
            preorderModal.hide();
            toggleSpinner(spinnerSavePreorder, false); // Скрыть спиннер после сохранения
        }
    }

    preorderForm.addEventListener('submit', function(event) {
        event.preventDefault();
        toggleSpinner(spinnerSavePreorder, true); // Показать спиннер при сохранении предзаказа
        const formData = new FormData(event.target);
        const data = {};
        formData.forEach((value, key) => data[key] = value);
        data['drop'] = document.getElementById('drop').checked;
        const message = {
            type: 'create_or_edit',
            form_data: data,
            id: preorderForm.dataset.id || null,
            user_id: userId
        };
        sendWebSocketMessage(message);
    });

    // При клике на кнопку "Удалить" открываем модальное окно подтверждения
    deletePreorderBtn.addEventListener('click', function() {
        preorderIdToDelete = preorderForm.dataset.id; // Сохраняем ID предзаказа для удаления
        if (preorderIdToDelete) {
            confirmDeleteModal.show(); // Показываем окно подтверждения
        }
    });

    preordersContainer.addEventListener('click', function(event) {
        const editLink = event.target.closest('.edit-link');
        if (editLink) {
            event.preventDefault();
            const preorderId = editLink.getAttribute('data-id');
            if (preorderId) {
                openPreorderModal(preorderId);
            } else {
                console.error('ID предзаказа не найден');
            }
        }
    });

    function preloadPreorderForm(data) {
        preorderForm.dataset.id = data.preorder_id;

        document.getElementById('full_name').value = data.full_name || '';
        document.getElementById('text').value = data.text || '';

        const dropCheckbox = document.getElementById('drop');
        if (dropCheckbox) {
            dropCheckbox.checked = !!data.drop;
        }

        document.getElementById('receipt_issued').checked = !!data.receipt_issued;
        document.getElementById('ttn').value = data.ttn || '';
        document.getElementById('shipped_to_customer').checked = !!data.shipped_to_customer;
        document.getElementById('status').value = data.status || '';
        document.getElementById('payment_received').checked = !!data.payment_received;

        if (data.preorder_id) {
            deletePreorderBtn.classList.remove('d-none');
            deletePreorderBtn.dataset.id = data.preorder_id;
        } else {
            deletePreorderBtn.classList.add('d-none');
        }
    }

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

    function bindCopyEvent(container) {
        container.querySelectorAll('.ttn-badge').forEach(badge => {
            badge.style.cursor = "pointer";
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

    let notificationTimeout;
    function showNotification(type, title, message) {
        clearTimeout(notificationTimeout);

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

        notificationTimeout = setTimeout(() => {
            toast.hide();
            setTimeout(() => {
                toastMessage.remove();
            }, 500);
        }, 2000);
    }

    function autoResizeTextArea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }

    function showConnectionLostModal() {
        const connectionLostModal = new bootstrap.Modal(document.getElementById('connectionLostModal'), {
            backdrop: 'static',
            keyboard: false
        });
        connectionLostModal.show();
    }
});
