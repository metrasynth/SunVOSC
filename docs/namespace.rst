=============
OSC Namespace
=============


All arguments are required unless marked as optional.


/slotN/...
==========

Address patterns pertaining to a specific slot witin the SunVox DLL
playback engine.

*N* must be in the range ``0..3``.


Messages sent to SunVOSC from peers
===================================


/slotN/inform/start,si
----------------------

Add an endpoint to send informational OSC messages to.

``host(s)``
    The hostname or IP address to inform.

``port(i)``
    The port to inform.


/slotN/inform/stop,si
---------------------

Remove an endpoint so it no longer receives informational OSC messages.

``host(s)``
    The string-formatted hostname or IP address to stop informing.

``port(i)``
    The port to stop informing.


/slotN/init,ii[b|s]
-------------------

Stops slot playback, initializes with an empty or specified project,
resets playback state, resets virtual row counter to ``-1``, and
resets master volume to either 80 for an empty project or the master
volume set by the project being loaded.

``patterns(i)``
    Number of playback patterns to create. Must be at least 1 if initializing
    an empty project, or at least the maximum number of overlapping patterns
    in the timeline of the loaded project.

``pattern_length(i)``
    Length of playback pattern(s). Must be within the range ``4..4096``.

The third argument may be one of these options:

``project_data(b)`` (optional)
    Content of existing SunVox project to initialize with.

``project_filename(s)`` (optional)
    Filename of existing SunVox project to initialize with.
    Must be UTF-8 encoded.


/slotN/start
------------

Starts playback.


/slotN/stop
-----------

Stops playback. Does not reset module state.


/slotN/volume,i
---------------

Sets master volume of slot.

``volume(i)``
    The volume to set.


/slotN/queue,iii(i|F)(i|F)(i|s|F)(i|F)(i|F)(i|F)
------------------------------------------------

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

``note_cmd(i|F)``
    The note or note command to queue, or ``False`` if not applicable.

``velocity(i|F)``
    The velocity of the note. Must be within the range ``0..128``,
    or ``False`` if not applicable.

``module(i|s|F)``
    The module to trigger. ``False`` if not triggering a module.
    If an actual module number, must be within the range ``1..255``.
    May be a module tag instead, if actual module number is not known.

``controller(i|F)``
    The controller to set a value for. Must be within the range ``1..32``,
    or ``False`` if not adjusting a controller.

``effect(i|F)``
    The note effect to apply. Must be a valid SunVox effect number,
    or ``False`` if not applying an effect. Must not be ``0x30``, which
    stops playback; instead use the `/slotN/stop`_ command to do so.

``parameter(i|F)``
    The 32-bit "XXYY" encoded parameter for controller or effect,
    or ``False`` if not setting a parameter. Effects that require
    separate "XX" and "YY" parameters must be encoded to "XXYY" form
    by the sender.


/slotN/play,i(i|F)(i|F)(i|s|F)(i|F)(i|F)(i|F)
---------------------------------------------

Plays a note immediately using the SunVox DLL internal pattern.

``track(i)``
    The track to send the note to. Must be within the range ``0..15``.

``note_cmd(i|F)``
    The note or note command to queue, or ``False`` if not applicable.
    Must not be an "FX to previous track" command.

``velocity(i|F)``
    The velocity of the note. Must be within the range ``0..128``,
    or ``False`` if not applicable.

``module(i|s|F)``
    The module to trigger. ``False`` if not triggering a module.
    If an actual module number, must be within the range ``1..255``.
    May be a module tag instead, if actual module number is not known.

``controller(i|F)``
    The controller to set a value for. Must be within the range ``1..32``,
    or ``False`` if not adjusting a controller.

``effect(i|F)``
    The note effect to apply. Must be a valid SunVox effect number,
    or ``False`` if not applying an effect. Must not be ``0x30``, which
    stops playback; instead use the `/slotN/stop`_ command to do so.

``parameter(i|F)``
    The 32-bit "XXYY" encoded parameter for controller or effect,
    or ``False`` if not setting a parameter. Effects that require
    separate "XX" and "YY" parameters must be encoded to "XXYY" form
    by the sender.


/slotN/new_module,ss[iii]
-------------------------

``tag(s)``
    A UUID representing the module that will be loaded.
    SunVOSC will use this tag when sending a message containing
    the actual module number.

``module_type``
    The type of the module, exactly as it appears in SunVox.
    (e.g. ``Generator``)

``name`` (default: same as ``module_type``)
    The name of the new module.

``x`` (default: 512)
    X position of the module.

``y`` (default: 512)
    Y position of the module.

``z`` (default: 0)
    Z position (layer) of the module.


/slotN/load_module,s(b|s)[iii]
------------------------------

``tag(s)``
    A UUID representing the module that will be loaded.
    SunVOSC will use this tag when sending a message containing
    the actual module number.

The second argument must be **one** of the following:

``synth_data(b)``
    Content of existing SunVox project to initialize with.

``synth_filename(s)``
    Filename of existing SunVox project to initialize with.
    Must be UTF-8 encoded.

Optional to specify module position:

``x`` (default: 512)
    X position of the module.

``y`` (default: 512)
    Y position of the module.

``z`` (default: 0)
    Z position (layer) of the module.


/slotN/connect,(i|s)(i|s)
-------------------------

``module_from(i|s)``
    Tag or module number of connection's source.

``module_to(i|s)``
    Tag or module number of of connection's destination.


/slotN/disconnect,(i|s)(i|s)
----------------------------

``module_from(i|s)``
    Tag or module number of connection's source.

``module_to(i|s)``
    Tag or module number of of connection's destination.


Messages sent by SunVOSC to peers
=================================

These messages are broadcast to all listeners registered to be informed.


/slotN/ready
------------

(No arguments.)

Sent to indicate that the slot has been initialized.


/slotN/module_created,s(i|F)
----------------------------

``tag(s)``
    The tag sent when loading or creating a module.

``number(i|F)``
    The module number of the module that was loaded or created;
    or ``False`` if the module couldn't be loaded or created.


/slotN/modules_connected,ii
---------------------------

``module_from(i)``
    Tag or module number of connection's source.

``module_to(i)``
    Tag or module number of of connection's destination.


/slotN/modules_disconnected,ii
------------------------------

``module_from(i)``
    Tag or module number of connection's source.

``module_to(i)``
    Tag or module number of of connection's destination.


/slotN/started
--------------

(No arguments.)


/slotN/stopped
--------------

(No arguments.)


/slotN/played,(i|F)(i|F)
------------------------

``row(i|F)``
    The virtual row that began playback;
    ``False``if playback hasn't started.

``frame(i|F)``
    The audio frame number where the row began, relative to the beginning of
    slot playback; ``False``if playback hasn't started.

This is sent once to each listener registered using `/slotN/inform/start,si`_
immediately after SunVOSC detects that a new row is being played by
SunVox DLL.

This is also sent to a new listener immediately after it's registered
to be informed.
