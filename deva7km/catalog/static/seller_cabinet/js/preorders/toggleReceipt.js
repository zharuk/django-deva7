function toggleReceipt(preorderId, isChecked) {
    const url = `/api/preorder/${preorderId}/toggle_receipt/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ receipt_issued: isChecked })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Failed to toggle receipt:', data.error);
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
