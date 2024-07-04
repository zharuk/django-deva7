// preorders.js

document.addEventListener('DOMContentLoaded', function() {
    const preorderForm = document.getElementById('preorderForm');

    preorderForm.addEventListener('submit', handleFormSubmit);

    // Добавим обработчики для иконок редактирования сразу после загрузки страницы
    addEditIconListeners();
});

function handleFormSubmit(event) {
    event.preventDefault();

    const submitButton = event.target.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    const preorderId = document.getElementById('preorderId').value;
    const formData = new FormData(event.target);

    // Получаем текущий текст описания
    let currentDescription = formData.get('text');

    // Проверка и удаление лишних "Инфо"
    if (currentDescription) {
        const infoPattern = /(?:Инфо: )+/g;
        currentDescription = currentDescription.replace(infoPattern, 'Инфо: ').trim();
        formData.set('text', currentDescription);
    }

    let url = '/api/preorder/create/';
    if (preorderId) {
        url = `/api/preorder/${preorderId}/update/`;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            $('#preorderModal').modal('hide');
            fetchPreorders();
        } else {
            console.error('Failed to save preorder:', data.error);
        }
        submitButton.disabled = false;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        submitButton.disabled = false;
    });
}

function openAddModal() {
    document.getElementById('preorderForm').reset();
    document.getElementById('preorderId').value = '';
    document.getElementById('preorderModalLabel').textContent = 'Добавить предзаказ';
    $('#preorderModal').modal('show');
}

function openEditModal(id) {
    const preorderElement = document.getElementById(`preorder-${id}`);
    if (preorderElement) {
        const fullName = preorderElement.querySelector('.card-title');
        const infoBlock = preorderElement.querySelector('.info-text');
        const drop = preorderElement.querySelector('.fa-check-circle');
        const ttn = preorderElement.querySelector('.ttn-badge');
        const status = preorderElement.querySelector('.status-text');

        document.getElementById('preorderId').value = id;
        document.getElementById('fullName').value = fullName ? fullName.textContent.trim() : '';

        // Извлечение текста из HTML и замена <br> на '\n', удаление пустых строк
        let textContent = infoBlock ? infoBlock.innerHTML.replace(/<br\s*\/?>/g, '\n').trim() : '';
        textContent = textContent.split('\n').filter(line => line.trim() !== '').join('\n');
        document.getElementById('text').value = textContent;

        document.getElementById('drop').checked = drop ? true : false;
        document.getElementById('ttn').value = ttn ? ttn.textContent.trim() : '';

        let statusContent = status ? status.textContent.trim() : '';
        document.getElementById('status').value = statusContent;

        document.getElementById('preorderModalLabel').textContent = 'Редактировать предзаказ';
        $('#preorderModal').modal('show');
    } else {
        console.error('Preorder element not found for ID:', id);
    }
}

function addEditIconListeners() {
    const editIcons = document.querySelectorAll('.edit-icon');
    editIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            openEditModal(id);
        });
    });
}