
function confirmation(form, message) {
    let yes = confirm(message);
    if (yes == true) {
        return true;
    }
    return false;
}
