import logging
import threading

import begin
import sunvox
from pythonosc import osc_server

from sunvosc.dispatcher import SunVoscDispatcher


@begin.start
@begin.logging
def main(
    interface: 'Interface to listen on' = 'localhost',
    port: 'Port to listen to' = 9000,
    freq: 'Audio output frequency (frames/sec)' = 44100,
    channels: 'Audio channels (1 or 2)' = 2,
):
    """
    Bidirectional OSC bridge for SunVox DLL.
    """
    process = sunvox.dll
    process.init(None, freq, channels, 0)
    dispatcher = SunVoscDispatcher(process)
    watch_thread = threading.Thread(target=dispatcher.watch_playback)
    watch_thread.start()
    server = osc_server.ThreadingOSCUDPServer((interface, port), dispatcher)
    logging.info('Serving on %s:%s', *server.server_address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        logging.info('Exiting')
        process.deinit()
        return 0
