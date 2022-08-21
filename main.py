import requests, json, time, websocket

token = "token"
message_id = "message id"
channel_id = "channel id"
guild_id = "guild id"
def get_msg(channel_id, message_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1&around={message_id}"
    headers = { 
        "authorization": token
    }
    request = requests.get(url, headers=headers)
    data = json.loads(request.text)
    return data
def interact(message_id, channel_id, guild_id):
    msg = get_msg(channel_id, message_id)
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    heart = ws.recv()
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "os": "windows",
                "browser": "chrome",
                "device": "pc"
            },
        }
    }
    ws.send(json.dumps(auth))
    res = json.loads(ws.recv())
    payload = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_id": message_id,
        "session_id":  res["d"]["session_id"],
        "application_id": msg[0]["author"]["id"],
        "data": {
                "component_type": msg[0]['components'][0]['components'][0]["type"],
                "custom_id": msg[0]['components'][0]['components'][0]['custom_id']
        },
    }
    req = requests.post('https://discord.com/api/v9/interactions', headers={"authorization": token}, json=payload)
    print(req.content)
    ws.close()
interact(message_id, channel_id, guild_id)
