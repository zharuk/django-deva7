document.addEventListener("DOMContentLoaded", function() {
    console.log("Document loaded");

    const preordersContainer = document.getElementById("preorders-container");

    function createPreorderCard(preorder) {
        console.log("Creating card for preorder:", preorder);
        const card = document.createElement("div");
        card.className = "col-md-4 mb-4";
        card.dataset.id = preorder.id;
        card.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${preorder.full_name}</h5>
                    <p class="card-text">${preorder.text}</p>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item"><strong>Дроп:</strong> ${preorder.drop}</li>
                        <li class="list-group-item"><strong>Дата создания:</strong> ${preorder.created_at}</li>
                        <li class="list-group-item"><strong>Дата изменения:</strong> ${preorder.updated_at}</li>
                        <li class="list-group-item"><strong>Чек:</strong> ${preorder.receipt_issued}</li>
                        <li class="list-group-item"><strong>ТТН:</strong> ${preorder.ttn}</li>
                        <li class="list-group-item"><strong>Отправлен:</strong> ${preorder.shipped_to_customer}</li>
                        <li class="list-group-item"><strong>Статус:</strong> ${preorder.status}</li>
                    </ul>
                </div>
            </div>
        `;
        return card;
    }

    function addPreorderToContainer(preorder) {
        console.log("Adding preorder to container:", preorder);
        const card = createPreorderCard(preorder);
        preordersContainer.appendChild(card);
    }

    function updatePreorderInContainer(preorder) {
        console.log("Updating preorder in container:", preorder);
        const existingCard = document.querySelector(`.col-md-4[data-id='${preorder.id}']`);
        if (existingCard) {
            existingCard.querySelector('.card-title').textContent = preorder.full_name;
            existingCard.querySelector('.card-text').textContent = preorder.text;
            existingCard.querySelector('.list-group-item:nth-child(1)').innerHTML = `<strong>Дроп:</strong> ${preorder.drop}`;
            existingCard.querySelector('.list-group-item:nth-child(2)').innerHTML = `<strong>Дата создания:</strong> ${preorder.created_at}`;
            existingCard.querySelector('.list-group-item:nth-child(3)').innerHTML = `<strong>Дата изменения:</strong> ${preorder.updated_at}`;
            existingCard.querySelector('.list-group-item:nth-child(4)').innerHTML = `<strong>Чек:</strong> ${preorder.receipt_issued}`;
            existingCard.querySelector('.list-group-item:nth-child(5)').innerHTML = `<strong>ТТН:</strong> ${preorder.ttn}`;
            existingCard.querySelector('.list-group-item:nth-child(6)').innerHTML = `<strong>Отправлен:</strong> ${preorder.shipped_to_customer}`;
            existingCard.querySelector('.list-group-item:nth-child(7)').innerHTML = `<strong>Статус:</strong> ${preorder.status}`;
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
        } else {
            console.log("Preorder card not found for removal:", preorderId);
        }
    }

    const socket = new WebSocket("ws://" + window.location.host + "/ws/preorders/");

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
        } else {
            console.log("Received message without event type");
        }
    };

    socket.onclose = function() {
        console.log("WebSocket connection closed");
    };
});
