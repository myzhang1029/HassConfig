import sys 
import socket
import random
from homeassistant.helpers import config_validation as cv, entity_platform, service

def comm(msg):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
        client.connect(('192.168.1.112',6666))
        client.send(msg.encode())
        res = b""
        while True:
            st = client.recv(1024)
            if st:
                res += st
            else:
                break
        return res.decode()

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_play(call):
        """Handle the service call."""
        num = call.data.get("queue_position", "0")
        hass.states.set("imac_music.queue_position", num)
        musics = comm("list").split('\n')
        name = musics[int(num)]
        hass.states.set(
            "imac_music.queue_name",
            name.split('/')[-1].split('.')[0]
        )
        hass.states.set("imac_music.status", "Playing")
        comm(name)

    def handle_shuffle(call):
        """Handle the service call."""
        musics = comm("list").split('\n')
        num = random.randrange(len(musics))
        hass.states.set("imac_music.queue_position", num)
        name = musics[int(num)]
        hass.states.set(
            "imac_music.queue_name",
            name.split('/')[-1].split('.')[0]
        )
        hass.states.set("imac_music.status", "Playing")
        comm(name)

    def handle_stop(call):
        """Handle the service call."""
        hass.states.set("imac_music.queue_position", -1)
        hass.states.set("imac_music.queue_name", None)
        hass.states.set("imac_music.status", "Stopped")
        comm("stop")

    hass.services.register("imac_music", "play", handle_play)
    hass.services.register("imac_music", "shuffle", handle_shuffle)
    hass.services.register("imac_music", "stop", handle_stop)
    return True
