=============
OSC Namespace
=============


All arguments are required unless marked as optional.


/slot<n>/...
============

Address patterns pertaining to a specific slot witin the SunVox DLL
playback engine.

*<n>* must be in the range ``0..3``.


Messages received by SunVOSC
============================


/slot<n>/inform/start,si
------------------------

Add an endpoint to send informational OSC messages to.

``address(s)``
    The string-formatted hostname or IP address to inform.

``port(i)``
    The port to inform.


/slot<n>/inform/stop,si
-----------------------

Remove an endpoint so it no longer receives informational OSC messages.

``address(s)``
    The string-formatted hostname or IP address to stop informing.

``port(i)``
    The port to stop informing.


/slot<n>/init,iisb
------------------

Stops slot playback, initializes with an empty or specified project,
resets playback state, resets virtual row counter to ``-1``.

``patterns(i)``
    Number of playback patterns to create. Must be at least 1 if initializing
    an empty project, or at least the maximum number of overlapping patterns
    in the timeline of the loaded project.

``pattern_length(i)``
    Length of playback pattern(s). Must be within the range ``4..4096``.

``project_filename(s)`` (optional)
    Filename of existing SunVox project to initialize with.
    Must be UTF-8 encoded.

``project_data(b)`` (optional)
    Content of existing SunVox project to initialize with.


/slot<n>/start
--------------

Starts playback.


/slot<n>/stop
-------------

Stops playback. Does not reset module state.


/slot<n>/reset
--------------

Resets module state.


/slot<n>/volume,i
-----------------

Sets master volume of slot.

``volume(i)``
    The volume to set. Must be within the range ``0..???TODO???``.


/slot<n>/queue,iiiiiiiii
------------------------

Queues a command for playback.

``row(i)``
    The virtual row to queue into. Must be greater than the row currently
    being played.

``pattern(i)``
    The pattern to queue into. Must be within the range ``0..x`` where *x*
    must be less than the number of playback patterns the slot was
    initialized with.

``track(i)``
    The track to queue into. Must be within the range ``0..15``.

``note_cmd(i)``
    The note or note command to queue, or ``-1`` if not applicable.

``velocity(i)``
    The velocity of the note. Must be within the range ``0..128``,
    or ``-1`` if not applicable.

``module(i)``
    The module to trigger. Must be within the range ``1..255``,
    or ``-1`` if not triggering a module.

``controller(i)``
    The controller to set a value for. Must be within the range ``1..32``,
    or ``-1`` if not adjusting a controller.

``effect(i)``
    The note effect to apply. Must be a valid SunVox effect number,
    or ``-1`` if not applying an effect. Must not be ``0x30``, which
    stops playback; instead use the `/slot<n>/stop`_ command to do so.

``parameter(i)``
    The 32-bit "XXYY" encoded parameter for controller or effect,
    or ``-1`` if not setting a parameter. Effects that require
    separate "XX" and "YY" parameters must be encoded to "XXYY" form
    by the sender.


/slot<n>/play,iiiiiii
---------------------

Plays a note immediately using the SunVox DLL internal pattern.

``track(i)``
    The track to send the note to. Must be within the range ``0..15``.

``note_cmd(i)``
    The note or note command to queue, or ``-1`` if not applicable.
    Must not be an "FX to previous track" command.

``velocity(i)``
    The velocity of the note. Must be within the range ``0..128``,
    or ``-1`` if not applicable.

``module(i)``
    The module to trigger. Must be within the range ``1..255``,
    or ``-1`` if not triggering a module.

``controller(i)``
    The controller to set a value for. Must be within the range ``1..32``,
    or ``-1`` if not adjusting a controller.

``effect(i)``
    The note effect to apply. Must be a valid SunVox effect number,
    or ``-1`` if not applying an effect. Must not be ``0x30``, which
    stops playback; instead use the `/slot<n>/stop`_ command to do so.

``parameter(i)``
    The 32-bit "XXYY" encoded parameter for controller or effect,
    or ``-1`` if not setting a parameter. Effects that require
    separate "XX" and "YY" parameters must be encoded to "XXYY" form
    by the sender.


Messages sent by SunVOSC
========================


/slot<n>/played,i
-----------------

This is sent one to each listener registered using `/slot<n>/inform/start,si`_
immediately after SunVOSC detects that a new row is being played by
SunVox DLL.

``row(i)``
    The virtual row that began playback.
