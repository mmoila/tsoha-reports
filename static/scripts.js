
function confirmation(form) {
    let yes = confirm("Are you sure you want to delete this report?");
    if (yes == true) {
        return true;
    }
    return false;
}
