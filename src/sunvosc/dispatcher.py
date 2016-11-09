import ctypes
import logging
import os
from io import BytesIO
from tempfile import mkstemp
from threading import RLock
from time import sleep

import rv
import rv.api
import sunvox
from pythonosc import dispatcher
from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder


SLOTS = 4
PLAYBACK_PATTERN_TRACKS = 16


def _slimmed(d, remove=['self', 'args', '_']):
    for key in remove:
        del d[key]
    return d


class PeerDispatcher(dispatcher.Dispatcher):

    def __init__(self):
        super().__init__()
        self.last_played = [None] * SLOTS
        self.ready = [False] * SLOTS
        self.started = [False] * SLOTS
        self.module_numbers = [{} for _ in range(SLOTS)]
        self.module_connections = [set() for _ in range(SLOTS)]
        for slot_number in range(SLOTS):
            self.map_slot(slot_number)

    def map_slot(self, slot_number):
        slot = '/slot{}/'.format(slot_number)
        self.map(slot + 'played', self.on_played, slot_number)
        self.map(slot + 'ready', self.on_ready, slot_number)
        self.map(slot + 'module_created', self.on_module_created, slot_number)
        self.map(slot + 'modules_connected', self.on_modules_connected, slot_number)
        self.map(slot + 'modules_disconnected', self.on_modules_disconnected, slot_number)
        self.map(slot + 'started', self.on_started, slot_number)
        self.map(slot + 'stopped', self.on_stopped, slot_number)

    def on_played(self, _, args, row, frame):
        slot_number, = args
        logging.debug('played %r', _slimmed(locals()))
        self.last_played[slot_number] = row, frame

    def on_ready(self, _, args):
        slot_number, = args
        logging.debug('ready %r', _slimmed(locals()))
        self.ready[slot_number] = True

    def on_module_created(self, _, args, tag, number):
        slot_number, = args
        logging.debug('module_created %r', _slimmed(locals()))
        self.module_numbers[slot_number][tag] = number

    def on_modules_connected(self, _, args, module_from, module_to):
        slot_number, = args
        logging.debug('modules_connected %r', _slimmed(locals()))
        self.module_connections[slot_number].add((module_from, module_to))

    def on_modules_disconnected(self, _, args, module_from, module_to):
        slot_number, = args
        logging.debug('modules_disconnected %r', _slimmed(locals()))
        self.module_connections[slot_number] -= {(module_from, module_to)}

    def on_started(self, _, args):
        slot_number, = args
        logging.debug('started %r', _slimmed(locals()))
        self.started[slot_number] = True

    def on_stopped(self, _, args):
        slot_number, = args
        logging.debug('stopped %r', _slimmed(locals()))
        self.started[slot_number] = False


class SunVoscDispatcher(dispatcher.Dispatcher):

    def __init__(self, process):
        super().__init__()
        self._process = process
        self._clients = {
            # (slot, host, port): udp_client,
        }
        self._slots = [sunvox.Slot(process=process) for x in range(SLOTS)]
        self._slot_locks = [RLock() for x in range(SLOTS)]
        self._last_played = [-1] * SLOTS
        self._last_virtual = [-1] * SLOTS
        for slot_number in range(SLOTS):
            self.map_slot(slot_number)

    def map_slot(self, slot_number):
        slot = '/slot{}/'.format(slot_number)
        self.map(slot + 'inform/start', self.on_inform_start, slot_number)
        self.map(slot + 'inform/stop', self.on_inform_stop, slot_number)
        self.map(slot + 'init', self.on_slot_init, slot_number)
        self.map(slot + 'connect', self.on_connect, slot_number)
        self.map(slot + 'disconnect', self.on_disconnect, slot_number)
        self.map(slot + 'load_module', self.on_load_module, slot_number)
        self.map(slot + 'new_module', self.on_new_module, slot_number)
        self.map(slot + 'play', self.on_play, slot_number)
        self.map(slot + 'queue', self.on_queue, slot_number)
        self.map(slot + 'start', self.on_start, slot_number)
        self.map(slot + 'stop', self.on_stop, slot_number)
        self.map(slot + 'volume', self.on_volume, slot_number)

    def scrub_row(self, slot, virtual_row):
        actual_row = virtual_row % slot.playback_pattern_length
        for pattern in range(0, slot.playback_pattern_count):
            data = slot.get_pattern_data(pattern)
            for track in range(0, PLAYBACK_PATTERN_TRACKS):
                offset = actual_row * PLAYBACK_PATTERN_TRACKS + track
                note = data[offset]
                note.note = 0
                note.vel = 0
                note.module = 0
                note.nothing = 0
                note.ctl = 0
                note.ctl_val = 0

    def watch_playback(self):
        while True:
            try:
                for slot_number, slot in enumerate(self._slots):
                    if slot.end_of_song():
                        continue
                    last = self._last_played[slot_number]
                    current = slot.get_current_line()
                    if 0 <= current != last:
                        self._last_played[slot_number] = current
                        if current < last:
                            current += slot.playback_pattern_length
                        delta = current - last
                        last_virtual = self._last_virtual[slot_number]
                        current_virtual = last_virtual + delta
                        self._last_virtual[slot_number] = current_virtual
                        with self._slot_locks[slot_number]:
                            for row in range(last_virtual, current_virtual):
                                self.scrub_row(slot, row)
                        b = OscMessageBuilder('/slot{}/played'.format(slot_number))
                        b.add_arg(current_virtual, 'i')
                        b.add_arg(0, 'i')   # TODO: implement frame once we have buffered output
                        msg = b.build()
                        for client in self._clients.values():
                            client.send(msg)
                sleep(0)
            except ctypes.ArgumentError:
                # TODO: fix root cause which is caused by threads
                logging.warning('ctypes.ArgumentError')
                raise

    def on_inform_start(self, _, args, host, port):
        slot_number, = args
        logging.debug('inform_start %r', _slimmed(locals()))
        key = (slot_number, host, port)
        if key not in self._clients:
            self._clients[key] = udp_client.UDPClient(host, port)
        client = self._clients[key]
        b = OscMessageBuilder('/slot{}/played'.format(slot_number))
        b.add_arg(False, 'F')
        b.add_arg(False, 'F')
        msg = b.build()
        client.send(msg)

    def on_inform_stop(self, _, args, host, port):
        slot_number, = args
        logging.debug('inform_stop %r', _slimmed(locals()))
        key = (slot_number, host, port)
        if key in self._clients:
            del self._clients[key]

    def on_slot_init(self, _, args, pattern_count, pattern_length, file_or_data=None):
        slot_number, = args
        logging.debug('slot_init %r', _slimmed(locals()))
        if isinstance(file_or_data, bytes):
            project = rv.api.read_sunvox_file(BytesIO(file_or_data))
        elif isinstance(file_or_data, str):
            project = rv.api.read_sunvox_file(file_or_data)
        else:
            project = rv.api.Project()
            project.initial_tpl = 1
        # TODO: displace built-in patterns and set up pattern map.
        # (for now we just blow away the old patterns)
        project.patterns = [
            rv.api.Pattern(tracks=PLAYBACK_PATTERN_TRACKS,
                           lines=pattern_length)
            for _ in range(pattern_count)
        ]
        slot = self._slots[slot_number]
        with self._slot_locks[slot_number]:
            slot.stop()
            with BytesIO() as f:
                project.write_to(f)
                slot.load_file(f)
            slot.rewind(0)
            slot.set_autostop(False)
            slot.playback_pattern_count = pattern_count
            slot.playback_pattern_length = pattern_length
            self._last_played[slot_number] = -1
            self._last_virtual[slot_number] = -1
        b = OscMessageBuilder('/slot{}/ready'.format(slot_number))
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)

    def on_start(self, _, args):
        slot_number, = args
        logging.debug('start %r', _slimmed(locals()))
        with self._slot_locks[slot_number]:
            self._slots[slot_number].play()
        b = OscMessageBuilder('/slot{}/started'.format(slot_number))
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)

    def on_stop(self, _, args):
        slot_number, = args
        logging.debug('stop %r', _slimmed(locals()))
        with self._slot_locks[slot_number]:
            self._slots[slot_number].stop()
        b = OscMessageBuilder('/slot{}/stopped'.format(slot_number))
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)

    def on_volume(self, _, args, volume):
        slot_number, = args
        logging.debug('volume %r', _slimmed(locals()))
        with self._slot_locks[slot_number]:
            self._slots[slot_number].volume(volume)

    def on_queue(self, _, args, row, pattern, track, note_cmd, velocity,
                 module, controller, effect, parameter):
        slot_number, = args
        logging.debug('queue %r', _slimmed(locals()))
        slot = self._slots[slot_number]
        actual_row = row % slot.playback_pattern_length
        offset = actual_row * PLAYBACK_PATTERN_TRACKS + track
        with self._slot_locks[slot_number]:
            note = slot.get_pattern_data(pattern)[offset]
            note.note = note_cmd
            note.vel = 0 if velocity is False else velocity + 1
            note.module = 0 if module is False else module + 1
            note.nothing = 0
            note.ctl = controller << 16 + effect
            note.ctl_val = parameter

    def on_play(self, _, args, track, note_cmd, velocity, module, controller,
                effect, parameter):
        slot_number, = args
        logging.debug('play %r', _slimmed(locals()))
        ctl_val = controller << 16 + effect
        with self._slot_locks[slot_number]:
            self._slots[slot_number].send_event(
                track, note_cmd, velocity, module + 1, ctl_val, parameter)

    def on_load_module(self, _, args, tag, file_or_data, x=512, y=512, z=0):
        slot_number, = args
        logging.debug('load_module %r', _slimmed(locals()))
        if isinstance(file_or_data, str):
            filename = file_or_data.encode(rv.ENCODING)
            with self._slot_locks[slot_number]:
                module_number = self._slots[slot_number].load_module(
                    filename, x, y, z)
        elif isinstance(file_or_data, bytes):
            fd, name = mkstemp('.sunsynth')
            os.write(fd, file_or_data)
            os.close(fd)
            slot = self._slots[slot_number]
            with self._slot_locks[slot_number]:
                module_number = slot.load_module(name.encode('utf8'), x, y, z)
            os.unlink(name)
        else:
            logging.warning('Unrecognized file_or_data')
            return
        b = OscMessageBuilder('/slot{}/module_created'.format(slot_number))
        b.add_arg(tag, 's')
        b.add_arg(module_number, 'i')
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)

    def on_new_module(self, _, args, tag, module_type, name=None,
                      x=512, y=512, z=0):
        slot_number, = args
        module_type = module_type.encode(rv.ENCODING)
        name = name.encode(rv.ENCODING) if name else None
        logging.debug('new_module %r', _slimmed(locals()))
        with self._slot_locks[slot_number]:
            module_number = self._slots[slot_number].new_module(
                module_type, name, x, y, z)
        b = OscMessageBuilder('/slot{}/module_created'.format(slot_number))
        b.add_arg(tag, 's')
        b.add_arg(module_number, 'i')
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)

    def on_connect(self, _, args, module_from, module_to):
        slot_number, = args
        logging.debug('connect %r', _slimmed(locals()))
        with self._slot_locks[slot_number]:
            self._slots[slot_number].connect_module(module_from, module_to)
        b = OscMessageBuilder('/slot{}/modules_connected'.format(slot_number))
        b.add_arg(module_from, 'i')
        b.add_arg(module_to, 'i')
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)

    def on_disconnect(self, _, args, module_from, module_to):
        slot_number, = args
        logging.debug('disconnect %r', _slimmed(locals()))
        with self._slot_locks[slot_number]:
            self._slots[slot_number].disconnect_module(module_from, module_to)
        b = OscMessageBuilder('/slot{}/modules_disconnected'.format(slot_number))
        b.add_arg(module_from, 'i')
        b.add_arg(module_to, 'i')
        msg = b.build()
        for client in self._clients.values():
            client.send(msg)
