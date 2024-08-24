document.addEventListener("DOMContentLoaded", function() {

    const preordersContainer = document.getElementById("preorders-container");

    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    const refreshStatusButton = document.getElementById("refresh-status-btn");
    const createPreorderBtn = document.getElementById("create-preorder-btn");
    const preorderModalElement = document.getElementById('preorderModal');
    const preorderModal = new bootstrap.Modal(preorderModalElement);
    const preorderFormContainer = document.getElementById('preorder-form-container');
    const preorderForm = document.getElementById('preorder-form');
    const deletePreorderBtn = document.getElementById('delete-preorder-btn');
    const userId = document.getElementById("user-id") ? document.getElementById("user-id").value : null;
    let activeFilter = 'all';
    let isWebSocketConnected = false;
    let socket;

    if (!searchInput || !clearSearchButton || !refreshStatusButton) {
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
        if (isWebSocketConnected) {
            sendWebSocketMessage({ type: 'search', search_text: '' });
        }
    });

    refreshStatusButton.addEventListener('click', function() {
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

    function sendWebSocketMessage(message) {
        message.user_id = userId;
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(message));
        }
    }

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        isWebSocketConnected = true;
        sendWebSocketMessage({ filter: activeFilter });
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.event === 'preorder_list') {
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
                    preordersContainer.innerHTML = ''; // Очищаем контейнер, если новый контент не найден
                    updateFilterCounts(data.counts);
                }
            } else {
                preordersContainer.innerHTML = ''; // Очищаем контейнер, если HTML не получен
                updateFilterCounts(data.counts);
            }
        } else if (data.event === 'get_preorder') {
            preloadPreorderForm(data);
            preorderModal.show();
        }
    };

    socket.onclose = function() {
        isWebSocketConnected = false;
        showConnectionLostModal();
    };

    preorderForm.addEventListener('submit', function(event) {
        event.preventDefault();
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

    deletePreorderBtn.addEventListener('click', function() {
        const preorderId = preorderForm.dataset.id;
        if (preorderId) {
            sendWebSocketMessage({
                type: 'delete',
                id: preorderId,
                user_id: userId
            });
            preorderModal.hide();
        }
    });

    preordersContainer.addEventListener('click', function(event) {
        if (event.target.closest('.edit-link')) {
            event.preventDefault();
            const preorderId = event.target.closest('.edit-link').getAttribute('data-id');
            openPreorderModal(preorderId);
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
