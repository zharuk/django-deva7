document.addEventListener('DOMContentLoaded', () => {
    const ttnElements = document.querySelectorAll('.badge.bg-light.ttn-badge');
    ttnElements.forEach(ttnElement => {
        const ttn = ttnElement.innerText.replace(/\s/g, ''); // Удаление всех пробелов
        const formattedTtn = ttn.replace(/(\d{4})(?=\d)/g, '$1 ').trim(); // Разбивка по 4 цифры
        ttnElement.innerText = formattedTtn;
    });
});
