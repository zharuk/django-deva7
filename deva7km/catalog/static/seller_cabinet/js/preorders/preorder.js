document.addEventListener("DOMContentLoaded", function() {
    const preordersContainer = document.getElementById("preorders-container");
    const filterButtons = document.querySelectorAll('.filter-button');
    const searchInput = document.getElementById("search-input");
    const clearSearchButton = document.getElementById("clear-search");
    let activeFilter = 'all';
    let isWebSocketConnected = false;

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            activeFilter = this.getAttribute('data-filter');
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            if (isWebSocketConnected) {
                filterPreorders();
            }
        });
    });

    searchInput.addEventListener('input', function() {
        if (isWebSocketConnected) {
            searchPreorders(this.value);
        }
    });

    clearSearchButton.addEventListener('click', function() {
        searchInput.value = '';
        if (isWebSocketConnected) {
            searchPreorders('');
        }
    });

    function filterPreorders() {
        const wsMessage = JSON.stringify({ filter: activeFilter });
        socket.send(wsMessage);
        console.log(`Sent filter request: ${activeFilter}`);
    }

    function searchPreorders(searchText) {
        const wsMessage = JSON.stringify({ search_text: searchText });
        socket.send(wsMessage);
        console.log(`Sent search request: ${searchText}`);
    }

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/preorders/");

    socket.onopen = function() {
        console.log("WebSocket connection established");
        isWebSocketConnected = true;
        filterPreorders();
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.event) {
            if (data.event === 'preorder_list') {
                preordersContainer.innerHTML = data.html;
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
                sortPreorders();
                console.log("Received and rendered preorder list");
            } else if (data.event === 'preorder_saved' || data.event === 'preorder_updated') {
                const existingCard = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (existingCard) {
                    existingCard.outerHTML = data.html;
                } else {
                    preordersContainer.innerHTML += data.html;
                }
                bindSwitchEvents(preordersContainer);
                bindCopyEvent(preordersContainer);
                sortPreorders();
                console.log(`Received and updated preorder: ${data.preorder_id}`);
            } else if (data.event === 'preorder_deleted') {
                const cardToRemove = preordersContainer.querySelector(`.col-md-4[data-id="${data.preorder_id}"]`);
                if (cardToRemove) {
                    cardToRemove.remove();
                    console.log(`Removed preorder: ${data.preorder_id}`);
                }
            }
        }
    };

    socket.onclose = function() {
        console.log("WebSocket connection closed");
        isWebSocketConnected = false;
    };

    function sortPreorders() {
        const preorders = Array.from(preordersContainer.children);
        preorders.sort((a, b) => new Date(b.dataset.createdAt) - new Date(a.dataset.createdAt));
        preorders.forEach(preorder => preordersContainer.appendChild(preorder));
    }

    function bindSwitchEvents(container) {
        container.querySelectorAll('.receipt-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                console.log(`Toggled receipt switch for preorder ${id}, status: ${status}`);
                updateSwitchStatus('/preorder/toggle_receipt/', id, status, event.target);
            });
        });

        container.querySelectorAll('.shipped-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                console.log(`Toggled shipped switch for preorder ${id}, status: ${status}`);
                updateSwitchStatus('/preorder/toggle_shipped/', id, status, event.target);
            });
        });

        container.querySelectorAll('.payment-switch').forEach(item => {
            item.addEventListener('change', event => {
                const id = event.target.dataset.id;
                const status = event.target.checked;
                console.log(`Toggled payment switch for preorder ${id}, status: ${status}`);
                updateSwitchStatus('/preorder/toggle_payment/', id, status, event.target);
            });
        });
    }

    function updateSwitchStatus(url, id, status, switchElement) {
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
            console.log(`Updated switch status for ${id}: ${status}`);
        })
        .catch((error) => {
            console.error('Error:', error);
            switchElement.checked = !status;
        });
    }

    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; cookies.length > i; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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
                    toast.innerHTML =
                        `<div class="d-flex">
                            <div class="toast-body">
                                Скопировано
                            </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>`;
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

    bindSwitchEvents(document);
    bindCopyEvent(document);
});
