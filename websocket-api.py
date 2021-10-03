import asyncio, json, threading, websockets
from flask import Flask
from json.decoder import JSONDecodeError
import api_data

cal_essid = "cal" # (game- stripped off by client)
game_status = {
    "running": False,
    "status": "Please start connecting devices"
}

def parse_mac(content) -> str:
    if content and "mac" in content and type(content["mac"]) == str:
        return content["mac"]
    return None

def get_player(mac: str) -> api_data.Player:
    if mac:
        return api_data.Player.players.get(mac, None)
    return None

def get_status(player) -> dict:
    r = "S"
    r += "1" if player.alive else "0"
    r += "1" if game_status["running"] else "0"
    r += "1" if player.is_ready() else "0"
    r += "1" if player.cal else "0"
    r += "1" if player.do_ident() else "0"
    return r

def client_join(content):
    mac = parse_mac(content)
    if mac:
        player = api_data.Player.players.get(mac, None)
        if not player:
            player = api_data.Player(mac, "Player-" + mac)
        player.joined = True
        game_status["status"] = player.nick + " connected."
        return 200, get_status(player)
    return 400, None

def parse_signals(content) -> list:
    if "signals" in content and type(content["signals"]) == list:
        signals = []
        for signal in content["signals"]:
            if type(signal) == dict and "essid" in signal and "rssi" in signal:
                essid = signal["essid"]
                rssi = signal["rssi"]
                if type(essid) == str and type(rssi) == int:
                    signals.append(api_data.Signal(essid, rssi))
                    continue
            return None # Invalid signal
        return signals
    return None 

def client_cal(content):
    player = get_player(parse_mac(content))
    if player:
        signals = parse_signals(content)
        if signals:
            cal_sig = next(s for s in signals if s.essid == cal_essid)
            player.rssi_threshold = cal_sig.rssi
            player.cal = False
            return 200, get_status(player)
    return 400, None

def client_rssi(content):
    player = get_player(parse_mac(content))
    if player:
        signals = parse_signals(content)
        if signals != None:
            player.last_signals = signals

            if game_status["running"] and not player.alive:
                for signal in signals:
                    if signal.rssi > player.rssi_threshold:
                        t_mac = signal.essid
                        t_player = api_data.Player.players.get(t_mac, None)
                        if t_player and t_player.joined and t_player.alive:
                            t_player.alive = False
                        
            return 200, get_status(player)
    return 400, None

def client_status(content):
    player = get_player(parse_mac(content))
    if player:
        return 200, get_status(player)
    return 400, None

api_methods = {
    # Client methods
    "join": client_join,
    "cal": client_cal,
    "rssi": client_rssi,
    "status": client_status
}

def parse_request(message: str) -> str:
    resp = None

    data = None
    try:
        data = json.loads(message)
    except JSONDecodeError:
        print("Invalid request:", message)
    
    if data and "method" in data and "content" in data:
        method = data["method"]
        if method in api_methods:
            try:
                status, resp = api_methods[method](data["content"])
            except Exception as ex:
                print("Unhandled method exception in method", method, ":", str(ex))
        else:
            print("Invalid method:", message)

    return resp

async def api(websocket, path):
    print(f"{path=}")
    if path == "/":
        print("WEBSOCKET CONNECTION")
        async for message in websocket:
            r = parse_request(message)
            if r:
                await websocket.send(r)
            
    elif path == "/ping":
        async for message in websocket:
            await websocket.send(message)

web_api = Flask(__name__)

def gen_resp(status, data):
    response = web_api.response_class(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@web_api.route('/clients', methods=['GET'])
def web_clients():
    status, data = api_data.get_clients()
    return gen_resp(status, data) 

@web_api.route('/nick', methods=['POST'])
def web_nick():
    request_data = request.get_json()
    player = get_player(parse_mac(request_data))
    if player and "nick" in request_data and type(request_data["nick"]) == str:
        player.nick = request_data["nick"]
        return gen_resp(200, None)
    return gen_resp(500, None)

@web_api.route('/startcal', methods=['POST'])
def web_startcal():
    request_data = request.get_json()
    player = get_player(parse_mac(request_data))
    if player:
        player.rssi_threshold = None
        player.cal = True
        return gen_resp(200, None)
    return gen_resp(500, None)

@web_api.route('/ident', methods=['POST'])
def web_ident():
    request_data = request.get_json()
    player = get_player(parse_mac(request_data))
    if player:
        player.ident = True
        return gen_resp(200, None)
    return gen_resp(500, None)

@web_api.route('/start', methods=['POST'])
def web_start():
    request_data = request.get_json()
    if game_status["running"]:
        return gen_resp(500, {"message": "Game already running"})
    imposters = []
    if "imposters" in request_data: 
        for mac in request_data["imposters"]:
            player = get_player(mac)
            if player:
                imposters.append(player)
    api_data.set_all_alive()
    if len(imposters) > 0:
        for player in imposters:
            player.alive = False
        game_status["running"] = True
        return gen_resp(200, None)
    return gen_resp(500, None)

@web_api.route('/stop', methods=['POST'])
def web_stop():
    if not game_status["running"]:
        return gen_resp(500, {"message": "Game not running"})
    game_status["running"] = False

@web_api.route('/state', methods=['GET'])
def web_state():
    return gen_resp(200, {
        "game_running": game_status["running"],
        "clients": len([p for p in api_data.Player.players if p.joined]),
        "status": game_status["status"]
    })

async def main():
    print("Starting websockets server on port 8765")
    async with websockets.serve(api, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    t = threading.Thread(target=lambda: web_api.run(host="0.0.0.0", port="8080", debug=True, use_reloader=False), daemon=True)
    t.start()
    asyncio.run(main())