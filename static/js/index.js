document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/users/')
        .then(response => response.json())
        .then(data => {
            const userList = document.getElementById('user-list');
            data.forEach(user => {
                const li = document.createElement('li');
                li.textContent = `${user.username} - ${user.email}`;
                const button = document.createElement('button');
                button.textContent = 'Send Friend Request';
                button.onclick = () => sendFriendRequest(user.id);
                li.appendChild(button);
                userList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
});

function sendFriendRequest(userId) {
    fetch(`/api/friend-request/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            alert('Friend request sent!');
        } else {
            response.json().then(data => alert(data.detail));
        }
    })
    .catch(error => {
        console.error('Error sending friend request:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*list friend request */
/*document.addEventListener("DOMContentLoaded", function() {
    fetch('friend-requests/', {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const requestList = document.getElementById('friend-request-list');
        data.forEach(request => {
            const li = document.createElement('li');
            li.textContent = `${request.from_user} sent you a friend request`;
            requestList.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Error fetching friend requests:', error);
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}*/