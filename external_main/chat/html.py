html = """
<!DOCTYPE html>
<html>
    <head>
        <title>ws</title>
    </head>
    <body>
        <h1>WebsocketChannelEndpoint</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>group_id: </label><input type="text" id="groupId" autocomplete="off" value="group_1"><br/>
            <label>username: </label><input type="text" id="username" autocomplete="off" value="test_user1"><br/>       
            <label>message: </label><input type="text" id="messageText" autocomplete="off" value="test_message1"><br/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket(`ws://localhost:8000/chat/ws`);
            ws.onmessage = function(event) {
                console.log('Message received %s', event.data)
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var data = JSON.parse(event.data);
                message.innerHTML = `<strong>${data.username} :</strong> ${data.message}`;
                messages.appendChild(message);
            };
            function sendMessage(event) {
                var username = document.getElementById("username");
                var group_id = document.getElementById("groupId");
                var input = document.getElementById("messageText");
                var data = {
                    "group_id": group_id.value, 
                    "username": username.value,
                    "message": input.value,
                };
                console.log('Message send %s', data)
                ws.send(JSON.stringify(data));
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""