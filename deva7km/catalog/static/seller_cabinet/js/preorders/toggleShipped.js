function toggleShipped(preorderId, isChecked) {
    const url = `/api/preorder/${preorderId}/toggle_shipped/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ shipped_to_customer: isChecked })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Failed to toggle shipped:', data.error);
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
