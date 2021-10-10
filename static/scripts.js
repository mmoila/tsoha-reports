
function confirmation(form, message) {
    let yes = confirm(message);
    if (yes == true) {
        return true;
    }
    return false;
}

function notification(form, message) {
    sessionStorage.setItem("notification", message);
}
        
$(document).ready(function() {
    message = sessionStorage.getItem("notification")
    if (message) {
        document.getElementById("toast-body").innerHTML = message;
        $("#toast").toast("show");
        sessionStorage.removeItem("notification");
    }
});



