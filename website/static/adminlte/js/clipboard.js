// Requires additional import of toast.js';

// Extract value of data-code attribute of the element and copies it to a clipboard.
//
// @param {HTMLElement} element - The HTML element that triggers the copy action. It should have data-code attribute.
// @returns {void}
function copyCodeToClipboard(element) {
    const buildCode = element.dataset.code;

    if (buildCode) {
        const toastHeader = 'Data copied to a clipboard';
        const toastMessage = 'You build code have been copied to a clipboard';

        copyToClipboard(buildCode, toastHeader, toastMessage);
    }
}

// Function to copy text to a clipboard
//
// @param {text} string - data that should be copied to a clipboard
// @param {toastHeader} string - header of a popup window after successful operation
// @param {toastMessage} string - body of a popup window after successful operation
// @returns {void}
function copyToClipboard(text, toastHeader = '', toastMessage = '') {
    if (!toastHeader) {
        toastHeader = 'Success';
    }
    if (!toastMessage) {
        toastMessage = 'Data copied to a clipboard';
    }

    if (text) {
        var textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);

        toastSuccess(toastHeader, toastMessage);
    }
}
