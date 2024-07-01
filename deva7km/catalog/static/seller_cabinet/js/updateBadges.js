function updateBadges(preorderElement, isShipped, isReceipted) {
    const badgeContainer = preorderElement.querySelector('.badge-container');
    badgeContainer.innerHTML = '';

    if (isShipped && isReceipted) {
        const badgeBoth = document.createElement('span');
        badgeBoth.className = 'badge bg-success mb-2';
        badgeBoth.innerText = 'Отправлен и пробит';
        badgeContainer.appendChild(badgeBoth);
    } else {
        if (!isShipped) {
            const badgeShipped = document.createElement('span');
            badgeShipped.className = 'badge bg-warning text-dark mb-2';
            badgeShipped.innerText = 'Не отправлено';
            badgeContainer.appendChild(badgeShipped);
        }

        if (!isReceipted) {
            const badgeReceipted = document.createElement('span');
            badgeReceipted.className = 'badge bg-danger text-white mb-2';
            badgeReceipted.innerText = 'Не пробит чек';
            badgeContainer.appendChild(badgeReceipted);
        }
    }
}
