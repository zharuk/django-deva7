let activeFilter = 'all'; // Определим активный фильтр по умолчанию

console.log('preorders.js loaded');

document.addEventListener('DOMContentLoaded', function () {
    console.log('Document loaded');
    fetchPreorders();
    setupWebSocket();
    setupEventListeners();
});

function setupWebSocket() {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/preorders/');

    socket.onmessage = function(event) {
        console.log('WebSocket message received:', event.data);
        const data = JSON.parse(event.data);
        updatePreorders(data.preorders);
    };

    socket.onclose = function(event) {
        console.error('WebSocket closed unexpectedly');
    };

    console.log('WebSocket connection established');
}

function setupEventListeners() {
    document.getElementById('preorderForm').addEventListener('submit', function(event) {
        event.preventDefault();
        if (document.getElementById('preorderId').value) {
            updatePreorder();
        } else {
            createPreorder();
        }
    });

    const addModalButton = document.querySelector('button[data-bs-target="#preorderModal"]');
    if (addModalButton) {
        addModalButton.addEventListener('click', openAddModal);
    }

    console.log('Event listeners set up');
}

function openAddModal() {
    document.getElementById('preorderForm').reset();
    document.getElementById('preorderId').value = '';
    document.getElementById('preorderModalLabel').innerText = 'Добавить предзаказ';
    console.log('Add modal opened');
}

function createPreorder() {
    const formData = new FormData(document.getElementById('preorderForm'));
    fetch('/preorders/create/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            full_name: formData.get('full_name'),
            text: formData.get('text'),
            drop: formData.get('drop') === 'on',
            ttn: formData.get('ttn'),
            status: formData.get('status')
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log('Preorder created successfully');
            const preorderModal = bootstrap.Modal.getInstance(document.getElementById('preorderModal'));
            preorderModal.hide();
        } else {
            console.error('Error creating preorder:', data.error);
        }
    })
    .catch(error => {
        console.error('Error creating preorder:', error);
    });
}

function updatePreorders(preorders) {
    console.log('Updating preorders:', preorders);

    const preordersContainer = document.getElementById('preorderContainer');
    preordersContainer.innerHTML = '';

    preorders.forEach(preorder => {
        const preorderHtml = `
            <div class="col-md-4 mb-4 preorder-item all ${(preorder.shipped_to_customer ? '' : 'not-shipped')} ${(preorder.receipt_issued ? '' : 'not-receipted')}" id="preorder-${preorder.id}">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <h5 class="card-title">${preorder.full_name}</h5>
                            <i class="fas fa-edit edit-icon" data-id="${preorder.id}" style="cursor:pointer;"></i>
                        </div>
                        <div class="badge-container">
                            ${preorder.shipped_to_customer && preorder.receipt_issued ?
                                '<span class="badge bg-success mb-2">Отправлен и пробит</span>' :
                                (preorder.shipped_to_customer ? '' : '<span class="badge bg-warning text-dark mb-2">Не отправлено</span>') +
                                (preorder.receipt_issued ? '' : '<span class="badge bg-danger text-white mb-2">Не пробит чек</span>')}
                        </div>
                        <div class="info-block">
                            <p class="card-text mt-3">
                                <strong>Инфо:</strong> <span class="info-text">${preorder.text.replace(/\n/g, '<br>')}</span><br>
                                <strong>Дроп:</strong> ${preorder.drop ? '<i class="fas fa-check-circle text-success"></i>' : '<i class="fas fa-times-circle text-danger"></i>'}<br>
                                <strong>Дата создания:</strong> ${preorder.created_at}<br>
                                <strong>Дата изменения:</strong> ${preorder.updated_at}<br>
                                <strong>ТТН:</strong> <span class="badge bg-light ttn-badge" id="ttn-${preorder.id}">${preorder.ttn}</span><br>
                                <strong>Статус посылки:</strong> <span class="status-text">${preorder.status}</span><br>
                            </p>
                        </div>
                        <div class="form-check form-switch d-inline-block me-3">
                            <input class="form-check-input ${(preorder.shipped_to_customer ? 'bg-success' : 'bg-warning')}" type="checkbox" id="shipped_to_customer_${preorder.id}" ${(preorder.shipped_to_customer ? ' checked' : '')} onchange="toggleShipped(${preorder.id}, this.checked)">
                            <label class="form-check-label" for="shipped_to_customer_${preorder.id}">Отправлен</label>
                        </div>
                        <div class="form-check form-switch d-inline-block">
                            <input class="form-check-input ${(preorder.receipt_issued ? 'bg-success' : 'bg-danger')}" type="checkbox" id="receipt_issued_${preorder.id}" ${(preorder.receipt_issued ? ' checked' : '')} onchange="toggleReceipt(${preorder.id}, this.checked)">
                            <label class="form-check-label" for="receipt_issued_${preorder.id}">Чек</label>
                        </div>
                    </div>
                </div>
            </div>`;
        preordersContainer.insertAdjacentHTML('beforeend', preorderHtml);
    });

    // Применяем текущий активный фильтр после обновления данных
    applyFilter(activeFilter);

    // Добавляем обработчики для иконок редактирования после обновления предзаказов
    addEditIconListeners();
    console.log('Preorders updated successfully');
}

function fetchPreorders() {
    fetch('/api/preorders/')
        .then(response => response.json())
        .then(data => {
            updatePreorders(data.preorders);
        })
        .catch(error => {
            console.error('Error fetching preorders:', error);
        });
}

function toggleShipped(preorderId, shipped) {
    console.log('Toggling shipped status:', preorderId, shipped);
    const data = { shipped_to_customer: shipped };

    fetch(`/preorders/toggle_shipped/${preorderId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Shipped status updated successfully');
        } else {
            console.error('Error updating shipped status:', data.error);
        }
    })
    .catch(error => {
        console.error('Error updating shipped status:', error);
    });
}

function toggleReceipt(preorderId, receipted) {
    console.log('Toggling receipt status:', preorderId, receipted);
    const data = { receipt_issued: receipted };

    fetch(`/preorders/toggle_receipt/${preorderId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Receipt status updated successfully');
        } else {
            console.error('Error updating receipt status:', data.error);
        }
    })
    .catch(error => {
        console.error('Error updating receipt status:', error);
    });
}

function applyFilter(filter) {
    console.log('Applying filter:', filter);
    activeFilter = filter;
    filterPreorders(filter, document.querySelector(`label[for="btnradio-${filter}-top"]`).innerText);
}

function filterPreorders(filter, title) {
    console.log('Filtering preorders:', filter, title);
    document.getElementById('preorderTitle').innerText = title;
    const preorderItems = document.querySelectorAll('.preorder-item');

    preorderItems.forEach(item => {
        if (filter === 'all' || item.classList.contains(filter)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

function addEditIconListeners() {
    const editIcons = document.querySelectorAll('.edit-icon');
    editIcons.forEach(icon => {
        icon.addEventListener('click', function () {
            const preorderId = this.getAttribute('data-id');
            openEditModal(preorderId);
        });
    });
}

function openEditModal(preorderId) {
    console.log('Opening edit modal for preorder:', preorderId);
    fetch(`/seller_cabinet/preorder/${preorderId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('preorderId').value = data.id;
            document.getElementById('fullName').value = data.full_name;
            document.getElementById('text').value = data.text;
            document.getElementById('drop').checked = data.drop;
            document.getElementById('ttn').value = data.ttn;
            document.getElementById('status').value = data.status;
            document.getElementById('preorderModalLabel').innerText = 'Редактировать предзаказ';
            const preorderModal = new bootstrap.Modal(document.getElementById('preorderModal'));
            preorderModal.show();
        })
        .catch(error => console.error('Error fetching preorder data:', error));
}

function getCookie(name) {
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
