what it is
----------
Listens on an ALSA MIDI port and send its MIDI messages to a multicast address


preparing
---------
Run:
     pip3 install rtmidi
first.


running
-------
Just invoke:
    ./alsa2im.py

If you need it to transmit to a different multicast group and/or port, then
change alsa2im.py. Look for 'multicast_group' and 'multicast_port' at the top.


(C) 2021 by folkert@vanheusden.com
Licensed under GPL v3.0
