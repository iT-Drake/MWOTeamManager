// toast.js

const toastType = {
    success: 'bg-success',
    warning: 'bg-warning',
    error: 'bg-danger'
};

function toastSuccess(title, message, delay = 3000) {
    showToast(toastType.success, title, message, delay);
}

function toastWarning(title, message, delay = 3000) {
    showToast(toastType.warning, title, message, delay);
}

function toastError(title, message, delay = 3000) {
    showToast(toastType.error, title, message, delay);
}

function showToast(type, title, message, delay = 3000) {
    if (type) {
        $(document).Toasts('create', {
            class: type,
            title: title,
            subtitle: 'Close',
            body: message,
            delay: delay,
            autohide: true
        });
    } else {
        console.error('Toast type should be filled in.');
    }
}
