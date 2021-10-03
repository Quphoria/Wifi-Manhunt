import json
from dataclasses import dataclass, field
from types import resolve_bases
from typing import ClassVar

recal_on_load = True

@dataclass
class Signal:
    essid: str
    rssi: int

@dataclass
class Player:
    mac: str
    nick: str
    joined: bool = True
    rssi_threshold: int = None
    last_signals: list = field(default_factory=list)
    players: ClassVar[dict] = {}
    alive = False
    ident = False
    cal = False

    def is_ready(self):
        return self.rssi_threshold != None

    def do_ident(self):
        i = self.ident
        self.ident = False
        return i

    def __post_init__(self):
        self.__class__.players[self.mac] = self

    @classmethod
    def delete_player(cls, mac):
        # Dont throw exception if doesnt exist
        cls.players.pop(mac, None)

    def save(self):
        return {
            "mac": self.mac,
            "nick": self.nick,
            "rssi_t": self.rssi_threshold
        }

    @classmethod
    def load(cls, data):
        new = cls(data["mac"], data["nick"], joined=False)
        if not recal_on_load:
            new.rssi_threshold = data["rssi_t"]
        return new

def save_players():
    player_data = []
    for player in Player.players:
        player_data.append(player.save())
    with open("playerdb.json", "w") as f:
        json.dump(player_data, f)

def load_players():
    with open("playerdb.json") as f:
        player_data = json.load(f) 
        if player_data and type(player_data) == list:
            for player in player_data:
                Player.load(player)

def get_clients():
    clients = []
    for player in Player.players:
        if player.joined:
            clients.append({
                "mac": player.mac,
                "nick": player.nick,
                "signals": [{"essid": s.essid, "rssi": s.rssi} for s in player.last_signals],
                "cal_rssi_threshold": player.rssi_threshold,
                "alive": player.alive
            })

    return 200, {
        "clients": clients
    }

def set_all_alive(alive = True):
    for player in Player.players:
        if player.is_ready():
            player.alive = alive