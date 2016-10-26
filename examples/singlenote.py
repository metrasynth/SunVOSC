import logging
import os
import threading
from time import sleep
from uuid import uuid4

import begin
from pythonosc import osc_server, udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
import sunvox


from sunvosc.dispatcher import PeerDispatcher


@begin.start
@begin.logging
def main(
    interface: 'Interface to listen on' = 'localhost',
    port: 'Port to listen to' = 9001,
    sunvosc_host: 'Host to connect to' = 'localhost',
    sunvosc_port: '' = 9000,
):
    """Connect to SunVOSC server and play a single note for 1 line."""

    client = udp_client.UDPClient(sunvosc_host, sunvosc_port)

    dispatcher = PeerDispatcher()
    server = osc_server.ThreadingOSCUDPServer((interface, port), dispatcher)
    logging.info('Peer serving on %s:%s', *server.server_address)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    b = OscMessageBuilder('/slot0/inform/start')
    b.add_arg(interface, 's')
    b.add_arg(port, 'i')
    msg = b.build()
    client.send(msg)

    logging.debug('Waiting for `played` response.')
    while dispatcher.last_played[0] is None:
        sleep(0.1)

    b = OscMessageBuilder('/slot0/init')
    b.add_arg(1, 'i')
    b.add_arg(4, 'i')
    msg = b.build()
    client.send(msg)

    logging.debug('Waiting for `ready` response.')
    while not dispatcher.ready[0]:
        sleep(0.1)

    b = OscMessageBuilder('/slot0/new_module')
    fm_tag = uuid4().hex
    b.add_arg(fm_tag, 's')
    b.add_arg('FM', 's')
    msg = b.build()
    client.send(msg)

    logging.debug('Waiting for `module_created` response.')
    while fm_tag not in dispatcher.module_numbers[0]:
        sleep(0.1)
    fm_id = dispatcher.module_numbers[0][fm_tag]

    b = OscMessageBuilder('/slot0/connect')
    b.add_arg(fm_id, 'i')
    b.add_arg(0, 'i')
    msg = b.build()
    client.send(msg)

    logging.debug('Waiting for `modules_connected` response.')
    while (fm_id, 0) not in dispatcher.module_connections[0]:
        sleep(0.1)

    b = OscMessageBuilder('/slot0/queue')
    b.add_arg(0, 'i')
    b.add_arg(0, 'i')
    b.add_arg(0, 'i')
    b.add_arg(sunvox.NOTECMD.C4, 'i')
    b.add_arg(64, 'i')
    b.add_arg(fm_id, 'i')
    b.add_arg(False, 'F')
    b.add_arg(False, 'F')
    b.add_arg(False, 'F')
    msg = b.build()
    client.send(msg)

    b = OscMessageBuilder('/slot0/queue')
    b.add_arg(1, 'i')
    b.add_arg(0, 'i')
    b.add_arg(0, 'i')
    b.add_arg(sunvox.NOTECMD.NOTE_OFF, 'i')
    b.add_arg(False, 'F')
    b.add_arg(fm_id, 'i')
    b.add_arg(False, 'F')
    b.add_arg(False, 'F')
    b.add_arg(False, 'F')
    msg = b.build()
    client.send(msg)

    b = OscMessageBuilder('/slot0/play')
    b.add_arg(1, 'i')
    b.add_arg(sunvox.NOTECMD.G4, 'i')
    b.add_arg(128, 'i')
    b.add_arg(fm_id, 'i')
    b.add_arg(False, 'F')
    b.add_arg(False, 'F')
    b.add_arg(False, 'F')
    msg = b.build()
    client.send(msg)

    b = OscMessageBuilder('/slot0/play')
    b.add_arg(1, 'i')
    b.add_arg(sunvox.NOTECMD.NOTE_OFF, 'i')
    b.add_arg(False, 'F')
    b.add_arg(fm_id, 'i')
    b.add_arg(False, 'i')
    b.add_arg(False, 'i')
    b.add_arg(False, 'i')
    msg = b.build()
    client.send(msg)

    b = OscMessageBuilder('/slot0/start')
    msg = b.build()
    client.send(msg)

    logging.debug('Waiting for `started` response.')
    while not dispatcher.started[0]:
        sleep(0.1)

    b = OscMessageBuilder('/slot0/inform/stop')
    b.add_arg(interface, 's')
    b.add_arg(port, 'i')
    msg = b.build()
    client.send(msg)

    os._exit(0)
