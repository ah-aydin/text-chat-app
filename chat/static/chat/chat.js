const chat_body = document.getElementById('chat-body');
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user_username = JSON.parse(document.getElementById('user_username').textContent);
// const messageInputDom = document.querySelector('#input');
const form = document.querySelector("#form");
const sendButton = document.querySelector("#send");
const redirect_url = `http://${window.location.host}/chat/`;

/**
 * Creates a message
 */
function createMessage(owner, content, time_created) {
    var classes = '';
    if (owner === user_username) {
        classes = "chat__message chat__reciever";
    } else {
        classes = "chat__message";
    }
    const p = `<p class="${classes}">
                    <span class="chat__name">${owner}</span>
                    ${content}
                </p>`;
    return p;
}

// load messages from api
async function fetchMessages() {
    try {
        let res = await fetch(`http://${window.location.host}/chat/api/messages/${roomName}/`,{
            headers: {
                'X-USERNAME': user_username
            }
        });
        if (res.status === 200) {
            let data = await res.json();
            let results = await data['results'];
            for (let i in results) {
                var row = results[i];
                chat_body.innerHTML += createMessage(row.owner_name, row.content, row.time_created);
            }
        }
    } catch (e) {
        console.log(e);
    }
    scrollBottom();
}
fetchMessages();

// create socket connection
const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.type === 'owner_left') {
        window.location.replace(redirect_url); 
    }
    chat_body.innerHTML += createMessage(data.username, data.message, data.time_created);
    scrollBottom();
}

// scroll to bottom of chat
function scrollBottom() {
    chat_body.scrollTop = chat_body.scrollHeight;
}
scrollBottom();

// send message function
function sendMessage(e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    var today = new Date();
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': user_username,
        'time_created': today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()
    }));
    messageInputDom.value = '';
}

form.onsubmit = function (e) { sendMessage(e); };