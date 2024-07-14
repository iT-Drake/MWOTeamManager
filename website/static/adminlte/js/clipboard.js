// Function to copy text to the clipboard
//
// @param {HTMLElement} element - The HTML element that triggers the copy action. It should have data-code attribute.
// @returns {void}
function copyToClipboard(element) {
    const buildCode = element.dataset.code;

    if (buildCode) {
        var textarea = document.createElement("textarea");
        textarea.value = buildCode;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);

        $(document).Toasts('create', {
            class: 'bg-success',
            title: 'Data copied to clipboard',
            subtitle: 'Close',
            body: 'You build code have been copied to a clipboard',
            delay: 3000,
            autohide: true
        })
    }
}
