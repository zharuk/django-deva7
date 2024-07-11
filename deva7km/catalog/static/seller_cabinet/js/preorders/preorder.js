document.addEventListener("DOMContentLoaded", function() {
    console.log("Document loaded");

    const preordersContainer = document.getElementById("preorders-container");
    const filterButtons = document.querySelectorAll('.filter-button');
    let activeFilter = 'all';

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            activeFilter = this.getAttribute('data-filter');
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            filterPreorders();
        });
    });

    function createPreorderCard(preorder) {
        console.log("Creating card for preorder:", preorder);
        const card = document.createElement("div");
        card.className = "col-md-4 mb-4";
        card.dataset.id = preorder.id;
        card.dataset.shipped = preorder.shipped_to_customer;
        card.dataset.receipt = preorder.receipt_issued;
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
                    <p class="card-text">${preorder.text}</p>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item"><strong>ТТН:</strong> <span class="badge bg-light ttn-badge">${preorder.ttn}</span></li>
                        <li class="list-group-item"><strong>Статус:</strong> ${preorder.status}</li>
                        <li class="list-group-item"><strong>Дроп:</strong> ${preorder.drop ? '<i class="fas fa-check-circle text-success"></i>' : '<i class="fas fa-times-circle text-danger"></i>'}</li>
                        <li class="list-group-item d-flex justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input shipped-switch ${preorder.shipped_to_customer ? 'bg-success' : 'bg-warning'}" type="checkbox" data-id="${preorder.id}" ${preorder.shipped_to_customer ? 'checked' : ''}>
                                <label class="form-check-label">Отправлен</label>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input receipt-switch ${preorder.receipt_issued ? 'bg-success' : 'bg-danger'}" type="checkbox" data-id="${preorder.id}" ${preorder.receipt_issued ? 'checked' : ''}>
                                <label class="form-check-label">Чек</label>
                            </div>
                        </li>
                        <li class="list-group-item text-muted"><small><strong>Дата создания:</strong> ${preorder.created_at}</small></li>
                        <li class="list-group-item text-muted"><small><strong>Дата изменения:</strong> ${preorder.updated_at}</small></li>
                    </ul>
                </div>
            </div>
        `;
        return card;
    }

    function getBadgesHTML(preorder) {
        let badges = '';
        if (!preorder.shipped_to_customer && !preorder.receipt_issued) {
            badges += '<span class="badge mb-1" style="background-color: #ee5f5b;">Не пробит</span>';
            badges += '<span class="badge" style="background-color: #f89406;">Не отправлен</span>';
        } else if (!preorder.shipped_to_customer) {
            badges += '<span class="badge" style="background-color: #f89406;">Не отправлен</span>';
        } else if (!preorder.receipt_issued) {
            badges += '<span class="badge" style="background-color: #ee5f5b;">Не пробит</span>';
        } else {
            badges += '<span class="badge" style="background-color: green;">Отправлен и пробит</span>';
        }
        return badges;
    }

    function addPreorderToContainer(preorder) {
        console.log("Adding preorder to container:", preorder);
        const card = createPreorderCard(preorder);
        if (preordersContainer) {
            preordersContainer.prepend(card);
            console.log("Preorder card appended at the beginning:", card);
            bindSwitchEvents(card);
            bindCopyEvent(card);
        } else {
            console.log("Preorders container not found");
        }
    }

    function updatePreorderInContainer(preorder) {
        console.log("Updating preorder in container:", preorder);
        const existingCard = document.querySelector(`.col-md-4[data-id='${preorder.id}']`);
        if (existingCard) {
            existingCard.querySelector('.card-title').textContent = preorder.full_name;
            existingCard.querySelector('.card-text').textContent = preorder.text;
            existingCard.querySelector('.list-group-item:nth-child(1)').innerHTML = `<strong>ТТН:</strong> <span class="badge bg-light ttn-badge">${preorder.ttn}</span>`;
            existingCard.querySelector('.list-group-item:nth-child(2)').innerHTML = `<strong>Статус:</strong> ${preorder.status}`;
            existingCard.querySelector('.list-group-item:nth-child(3)').innerHTML = `<strong>Дроп:</strong> ${preorder.drop ? '<i class="fas fa-check-circle text-success"></i>' : '<i class="fas fa-times-circle text-danger"></i>'}`;
            existingCard.querySelector('.list-group-item:nth-child(4)').innerHTML = `
                <div class="form-check form-switch">
                    <input class="form-check-input shipped-switch ${preorder.shipped_to_customer ? 'bg-success' : 'bg-warning'}" type="checkbox" data-id="${preorder.id}" ${preorder.shipped_to_customer ? 'checked' : ''}>
                    <label class="form-check-label">Отправлен</label>
                </div>
                <div class="form-check form-switch">
                    <input class="form-check-input receipt-switch ${preorder.receipt_issued ? 'bg-success' : 'bg-danger'}" type="checkbox" data-id="${preorder.id}" ${preorder.receipt_issued ? 'checked' : ''}>
                    <label class="form-check-label">Чек</label>
                </div>
            `;
            existingCard.querySelector('.list-group-item:nth-child(5)').innerHTML = `<small><strong>Дата создания:</strong> ${preorder.created_at}</small>`;
            existingCard.querySelector('.list-group-item:nth-child(6)').innerHTML = `<small><strong>Дата изменения:</strong> ${preorder.updated_at}</small>`;
            existingCard.querySelector('.badge-container').innerHTML = getBadgesHTML(preorder);
            existingCard.dataset.shipped = preorder.shipped_to_customer;
            existingCard.dataset.receipt = preorder.receipt_issued;
            bindSwitchEvents(existingCard);
            bindCopyEvent(existingCard);
            filterPreorders();
        } else {
            console.log("Preorder card not found for update, adding instead:", preorder);
            addPreorderToContainer(preorder);
        }
    }

    function removePreorderFromContainer(preorderId) {
        console.log("Removing preorder from container:", preorderId);
        const preorderCard = document.querySelector(`.col-md-4[data-id='${preorderId}']`);
        if (preorderCard) {
            preorderCard.remove();
            console.log("Preorder card removed:", preorderId);
        } else {
            console.log("Preorder card not found for removal:", preorderId);
        }
    }

    function updateSwitchStatus(endpoint, id, status) {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ 'id': id, 'status': status })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            filterPreorders();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; cookies.length; i++) {
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
                updateSwitchStatus('/preorder/toggle_receipt/', id, status);
                updateSwitchClass(event.target, status, 'receipt');
                updateBadges(container, id, status, 'receipt');
                filterPreorders();
            });
        });

        container.querySelectorAll('.shipped-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                updateSwitchStatus('/preorder/toggle_shipped/', id, status);
                updateSwitchClass(event.target, status, 'shipped');
                updateBadges(container, id, status, 'shipped');
                filterPreorders();
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
        }
    }

    function updateBadges(container, id, status, type) {
        const preorder = {
            id: id,
            shipped_to_customer: type === 'shipped' ? status : container.querySelector(`.shipped-switch[data-id='${id}']`).checked,
            receipt_issued: type === 'receipt' ? status : container.querySelector(`.receipt-switch[data-id='${id}']`).checked
        };
        container.querySelector('.badge-container').innerHTML = getBadgesHTML(preorder);
    }

    function filterPreorders() {
        const preorders = document.querySelectorAll('.col-md-4');
        preorders.forEach(preorder => {
            const shipped = preorder.dataset.shipped === 'true';
            const receipt = preorder.dataset.receipt === 'true';

            if (activeFilter === 'all') {
                preorder.style.display = 'block';
            } else if (activeFilter === 'not-shipped' && !shipped) {
                preorder.style.display = 'block';
            } else if (activeFilter === 'not-receipted' && !receipt) {
                preorder.style.display = 'block';
            } else {
                preorder.style.display = 'none';
            }
        });
    }

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        console.log("WebSocket connection established");
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("WebSocket message received:", data);

        if (data.event && data.preorder) {
            console.log("PreOrder update received:", data.event, data.preorder);
            if (data.event === 'preorder_saved') {
                updatePreorderInContainer(data.preorder);
            } else if (data.event === 'preorder_updated') {
                updatePreorderInContainer(data.preorder);
            } else if (data.event === 'preorder_deleted') {
                removePreorderFromContainer(data.preorder.id);
            }
        } else if (data.event && data.event === 'preorder_list') {
            data.preorders.forEach(preorder => {
                updatePreorderInContainer(preorder);
            });
        } else {
            console.log("Received message without event type");
        }
    };

    socket.onclose = function() {
        console.log("WebSocket connection closed");
    };

    bindSwitchEvents(document);
    bindCopyEvent(document);
    filterPreorders();
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
