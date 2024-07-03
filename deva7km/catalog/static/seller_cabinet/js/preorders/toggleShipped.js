function toggleShipped(id, isChecked) {
    fetch(`/api/preorder/${id}/toggle_shipped/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ shipped_to_customer: isChecked })
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
            const shippedInput = preorderElement.querySelector(`#shipped_to_customer_${id}`);
            if (isChecked) {
                preorderElement.classList.remove('not-shipped');
                shippedInput.classList.remove('bg-warning');
                shippedInput.classList.add('bg-success');
            } else {
                preorderElement.classList.add('not-shipped');
                shippedInput.classList.remove('bg-success');
                shippedInput.classList.add('bg-warning');
            }
            // Update badges
            updateBadges(preorderElement, isChecked, preorderElement.querySelector(`#receipt_issued_${id}`).checked);
            // Update the display based on current filter
            filterPreorders(activeFilter, document.querySelector('.btn-group .btn-check:checked + .btn').innerText);
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
