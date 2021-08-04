var notificationsElement = document.getElementById('notifications');
var socket = new WebSocket('ws://127.0.0.1:8000/consumers/notifications');

socket.onmessage = function (event) {
    notify(event.data);
}

function notify(message, type='danger') {
    var notification = document.createElement('div');
    notification.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible m-2" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
    notificationsElement.append(notification);
}
