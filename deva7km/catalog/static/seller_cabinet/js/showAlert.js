function showAlert(type, message) {
    const alertDiv = type === 'success' ? $('#success-alert') : $('#error-alert');
    const alertMessage = type === 'success' ? $('#success-message') : $('#error-message');
    alertMessage.text(message);
    alertDiv.addClass('show');

    setTimeout(function() {
        alertDiv.removeClass('show');
    }, 2000);
}