function toggleReceipt(id, isChecked) {
    fetch(`/api/preorder/${id}/toggle_receipt/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ receipt_issued: isChecked })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const preorderElement = document.getElementById(`preorder-${id}`);
            const receiptInput = preorderElement.querySelector(`#receipt_issued_${id}`);
            if (isChecked) {
                preorderElement.classList.remove('not-receipted');
                receiptInput.classList.remove('bg-danger');
                receiptInput.classList.add('bg-success');
            } else {
                preorderElement.classList.add('not-receipted');
                receiptInput.classList.remove('bg-success');
                receiptInput.classList.add('bg-danger');
            }
            // Update badges
            updateBadges(preorderElement, preorderElement.querySelector(`#shipped_to_customer_${id}`).checked, isChecked);
            // Update the display based on current filter
            filterPreorders(activeFilter, document.querySelector('.btn-group .btn-check:checked + .btn').innerText);
            console.log(`Preorder ${id} receipt_issued updated to ${isChecked}`);
        } else {
            console.error('Failed to update receipt_issued');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
