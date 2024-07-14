document.addEventListener("DOMContentLoaded", function() {
    const preordersContainer = document.getElementById("preorders-container");
    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    let activeFilter = 'all';

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            activeFilter = this.getAttribute('data-filter');
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            filterPreorders();
        });
    });

    searchInput.addEventListener('input', function() {
        searchPreorders(this.value);
    });

    clearSearchButton.addEventListener('click', function() {
        searchInput.value = '';
        searchPreorders('');
    });

    function createPreorderCard(preorder) {
    const card = document.createElement("div");
    card.className = "col-md-4 mb-4";
    card.dataset.id = preorder.id;
    card.dataset.shipped = preorder.shipped_to_customer;
    card.dataset.receipt = preorder.receipt_issued;
    card.dataset.payment = preorder.payment_received;
    card.dataset.createdAt = preorder.created_at;
    card.innerHTML = `
        <div class="card">
            <div class="badge-container mb-2 mt-2 ml-2">
                ${getBadgesHTML(preorder)}
            </div>
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <h5 class="card-title">${preorder.full_name}</h5>
                    <a href="/preorder/${preorder.id}/edit/" class="text-muted">
                        <i class="fas fa-edit"></i>
                    </a>
                </div>
                <p class="card-text" style="white-space: pre-wrap;">${preorder.text}</p>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item"><strong>ТТН:</strong> <span class="badge bg-light ttn-badge">${preorder.ttn}</span></li>
                    <li class="list-group-item"><strong>Статус:</strong> ${preorder.status}</li>
                    <li class="list-group-item"><strong>Дроп:</strong> ${preorder.drop ? '<i class="fas fa-check-circle text-success"></i>' : '<i class="fas fa-times-circle text-danger"></i>'}</li>
                    <li class="list-group-item switch-group">
                        <div class="switch-container">
                            <div class="form-check form-switch">
                                <input class="form-check-input shipped-switch ${preorder.shipped_to_customer ? 'bg-success' : 'bg-warning'}" type="checkbox" data-id="${preorder.id}" ${preorder.shipped_to_customer ? 'checked' : ''}>
                                <label class="form-check-label">Отправлен</label>
                            </div>
                        </div>
                        <div class="switch-container">
                            <div class="form-check form-switch">
                                <input class="form-check-input receipt-switch ${preorder.receipt_issued ? 'bg-success' : 'bg-danger'}" type="checkbox" data-id="${preorder.id}" ${preorder.receipt_issued ? 'checked' : ''}>
                                <label class="form-check-label">Чек</label>
                            </div>
                        </div>
                        <div class="switch-container">
                            <div class="form-check form-switch">
                                <input class="form-check-input payment-switch ${preorder.payment_received ? 'bg-success' : 'bg-secondary'}" type="checkbox" data-id="${preorder.id}" ${preorder.payment_received ? 'checked' : ''}>
                                <label class="form-check-label">Оплата</label>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item text-muted"><small><strong>Дата создания:</strong> ${formatDate(preorder.created_at)}</small></li>
                    <li class="list-group-item text-muted"><small><strong>Дата изменения:</strong> ${formatDate(preorder.updated_at)}</small></li>
                    <li class="list-group-item text-muted"><small><strong>Изменено пользователем:</strong> ${preorder.last_modified_by}</small></li>
                </ul>
            </div>
        </div>
    `;
    return card;
}

    function formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric'
        });
    }

    function getBadgesHTML(preorder) {
        let badges = '';

        const shipped = preorder.shipped_to_customer;
        const receipt = preorder.receipt_issued;
        const payment = preorder.payment_received;

        if (!shipped && !receipt && !payment) {
            badges += '<span class="badge mb-1" style="background-color: #f89406;">Не отправлен</span>';
            badges += '<span class="badge" style="background-color: #ee5f5b;">Не пробит</span>';
            badges += '<span class="badge" style="background-color: #6c757d;">Не оплачен</span>';
        } else {
            if (!shipped) {
                badges += '<span class="badge" style="background-color: #f89406;">Не отправлен</span>';
            }
            if (!receipt) {
                badges += '<span class="badge" style="background-color: #ee5f5b;">Не пробит</span>';
            }
            if (!payment) {
                badges += '<span class="badge" style="background-color: #6c757d;">Не оплачен</span>';
            }
            if (shipped && receipt && payment) {
                badges += '<span class="badge" style="background-color: green;">Готов</span>';
            }
        }

        return badges;
    }

    function addPreorderToContainer(preorder) {
        const card = createPreorderCard(preorder);
        preordersContainer.appendChild(card);
        sortPreorders();
        bindSwitchEvents(card);
        bindCopyEvent(card);
    }

    function sortPreorders() {
        const preorders = Array.from(preordersContainer.children);
        preorders.sort((a, b) => new Date(b.dataset.createdAt) - new Date(a.dataset.createdAt));
        preorders.forEach(preorder => preordersContainer.appendChild(preorder));
    }

    function updatePreorderInContainer(preorder) {
        const existingCard = document.querySelector(`.col-md-4[data-id='${preorder.id}']`);
        if (existingCard) {
            existingCard.querySelector('.card-title').textContent = preorder.full_name;
            existingCard.querySelector('.card-text').textContent = preorder.text;
            existingCard.querySelector('.card-text').style.whiteSpace = "pre-wrap";
            existingCard.querySelector('.list-group-item:nth-child(1)').innerHTML = `<strong>ТТН:</strong> <span class="badge bg-light ttn-badge">${preorder.ttn}</span>`;
            existingCard.querySelector('.list-group-item:nth-child(2)').innerHTML = `<strong>Статус:</strong> ${preorder.status}`;
            existingCard.querySelector('.list-group-item:nth-child(3)').innerHTML = `<strong>Дроп:</strong> ${preorder.drop ? '<i class="fas fa-check-circle text-success"></i>' : '<i class="fas fa-times-circle text-danger"></i>'}`;
            existingCard.querySelector('.list-group-item:nth-child(4)').innerHTML = `
                <div class="switch-container">
                    <div class="form-check form-switch">
                        <input class="form-check-input shipped-switch ${preorder.shipped_to_customer ? 'bg-success' : 'bg-warning'}" type="checkbox" data-id="${preorder.id}" ${preorder.shipped_to_customer ? 'checked' : ''}>
                        <label class="form-check-label">Отправлен</label>
                    </div>
                </div>
                <div class="switch-container">
                    <div class="form-check form-switch">
                        <input class="form-check-input receipt-switch ${preorder.receipt_issued ? 'bg-success' : 'bg-danger'}" type="checkbox" data-id="${preorder.id}" ${preorder.receipt_issued ? 'checked' : ''}>
                        <label class="form-check-label">Чек</label>
                    </div>
                </div>
                <div class="form-check form-switch">
                    <div class="switch-container">
                        <input class="form-check-input payment-switch ${preorder.payment_received ? 'bg-success' : 'bg-secondary'}" type="checkbox" data-id="${preorder.id}" ${preorder.payment_received ? 'checked' : ''}>
                        <label class="form-check-label">Оплата</label>
                    </div>
                </div>`;
            existingCard.querySelector('.badge-container').innerHTML = getBadgesHTML(preorder);
            existingCard.querySelector('.list-group-item:nth-child(5)').innerHTML = `<small><strong>Дата создания:</strong> ${formatDate(preorder.created_at)}</small>`;
            existingCard.querySelector('.list-group-item:nth-child(6)').innerHTML = `<small><strong>Дата изменения:</strong> ${formatDate(preorder.updated_at)}</small>`;
            existingCard.querySelector('.list-group-item:nth-child(7)').innerHTML = `<small><strong>Изменено пользователем:</strong> ${preorder.last_modified_by}</small>`;
            existingCard.dataset.shipped = preorder.shipped_to_customer;
            existingCard.dataset.receipt = preorder.receipt_issued;
            existingCard.dataset.payment = preorder.payment_received;
            existingCard.dataset.createdAt = preorder.created_at;
            sortPreorders();
            bindSwitchEvents(existingCard);
            bindCopyEvent(existingCard);
        } else {
            addPreorderToContainer(preorder);
        }
    }

    function removePreorderFromContainer(id) {
        const card = document.querySelector(`.col-md-4[data-id='${id}']`);
        if (card) {
            card.remove();
        }
    }

    function updateSwitchStatus(url, id, status, switchElement, originalStatus) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ 'id': id, 'status': status })
        })
        .then(response => response.json())
        .then(data => {
            sortPreorders();
            filterPreorders();  // Вызов функции фильтрации после обновления статуса
        })
        .catch((error) => {
            console.error('Error:', error);
            switchElement.checked = originalStatus;
            updateSwitchClass(switchElement, originalStatus, switchElement.classList.contains('receipt-switch') ? 'receipt' : switchElement.classList.contains('shipped-switch') ? 'shipped' : 'payment');
        });
    }

    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function bindSwitchEvents(container) {
        container.querySelectorAll('.receipt-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                const originalStatus = !status; // сохраняем оригинальный статус
                updateSwitchStatus('/preorder/toggle_receipt/', id, status, event.target, originalStatus);
                updateSwitchClass(event.target, status, 'receipt');
                updateBadges(container, id, status, 'receipt');
                sortPreorders();
            });
        });

        container.querySelectorAll('.shipped-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                const originalStatus = !status; // сохраняем оригинальный статус
                updateSwitchStatus('/preorder/toggle_shipped/', id, status, event.target, originalStatus);
                updateSwitchClass(event.target, status, 'shipped');
                updateBadges(container, id, status, 'shipped');
                sortPreorders();
            });
        });

        container.querySelectorAll('.payment-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                const originalStatus = !status; // сохраняем оригинальный статус
                updateSwitchStatus('/preorder/toggle_payment/', id, status, event.target, originalStatus);
                updateSwitchClass(event.target, status, 'payment');
                updateBadges(container, id, status, 'payment');
                sortPreorders();
            });
        });
    }

    function updateSwitchClass(switchElement, status, type) {
        if (type === 'receipt') {
            if (status) {
                switchElement.classList.remove('bg-danger');
                switchElement.classList.add('bg-success');
            } else {
                switchElement.classList.remove('bg-success');
                switchElement.classList.add('bg-danger');
            }
        } else if (type === 'shipped') {
            if (status) {
                switchElement.classList.remove('bg-warning');
                switchElement.classList.add('bg-success');
            } else {
                switchElement.classList.remove('bg-success');
                switchElement.classList.add('bg-warning');
            }
        } else if (type === 'payment') {
            if (status) {
                switchElement.classList.remove('bg-secondary');
                switchElement.classList.add('bg-success');
            } else {
                switchElement.classList.remove('bg-success');
                switchElement.classList.add('bg-secondary');
            }
        }
    }

    function updateBadges(container, id, status, type) {
        const preorder = {
            id: id,
            shipped_to_customer: type === 'shipped' ? status : container.querySelector(`.shipped-switch[data-id='${id}']`).checked,
            receipt_issued: type === 'receipt' ? status : container.querySelector(`.receipt-switch[data-id='${id}']`).checked,
            payment_received: type === 'payment' ? status : container.querySelector(`.payment-switch[data-id='${id}']`).checked
        };

        container.querySelector(`.col-md-4[data-id='${id}'] .badge-container`).innerHTML = getBadgesHTML(preorder);
    }

    function filterPreorders() {
        const preorders = document.querySelectorAll('.col-md-4');
        preorders.forEach(preorder => {
            const shipped = preorder.dataset.shipped === 'true';
            const receipt = preorder.dataset.receipt === 'true';
            const payment = preorder.dataset.payment === 'true';

            if (activeFilter === 'all') {
                preorder.style.display = 'block';
            } else if (activeFilter === 'not-shipped' && !shipped) {
                preorder.style.display = 'block';
            } else if (activeFilter === 'not-receipted' && !receipt) {
                preorder.style.display = 'block';
            } else if (activeFilter === 'not-paid' && !payment) {
                preorder.style.display = 'block';
            } else {
                preorder.style.display = 'none';
            }
        });
    }

    function searchPreorders(searchText) {
        const wsMessage = JSON.stringify({ search_text: searchText });
        socket.send(wsMessage);
    }

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        console.log("WebSocket connection established");
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.event && data.preorder) {
            if (data.event === 'preorder_saved' || data.event === 'preorder_updated') {
                updatePreorderInContainer(data.preorder);
            } else if (data.event === 'preorder_deleted') {
                removePreorderFromContainer(data.preorder.id);
            }
        } else if (data.event && data.event === 'preorder_list') {
            preordersContainer.innerHTML = ''; // Очищаем контейнер перед добавлением новых предзаказов
            data.preorders.forEach(preorder => {
                addPreorderToContainer(preorder);
            });
        }
    };

    socket.onclose = function() {
        console.log("WebSocket connection closed");
    };

    bindSwitchEvents(document);
    bindCopyEvent(document);
    filterPreorders();
    sortPreorders();
});

function bindCopyEvent(container) {
    container.querySelectorAll('.ttn-badge').forEach(badge => {
        badge.addEventListener('click', event => {
            const ttn = event.target.textContent.trim();
            navigator.clipboard.writeText(ttn).then(() => {
                badge.classList.add('badge-copied');
                setTimeout(() => {
                    badge.classList.remove('badge-copied');
                }, 2000);

                const toast = document.createElement('div');
                toast.className = 'toast align-items-center text-white bg-dark border-0';
                toast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            Скопировано
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                `;
                document.querySelector('.toast-container').appendChild(toast);
                const bsToast = new bootstrap.Toast(toast);
                bsToast.show();
                setTimeout(() => {
                    toast.remove();
                }, 2000);
            });
        });
    });
}
