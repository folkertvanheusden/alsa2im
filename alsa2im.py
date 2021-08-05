#! /usr/bin/python3

# (C) 2021 by folkert@vanheusden.com
#
# Run:
#      pip3 install rtmidi
# first.

import rtmidi
import socket

multicast_group = '225.0.0.37'
multicast_port = 21928
multicast_ttl = 2

fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

fd.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast_ttl)

midiin = rtmidi.RtMidiIn()
midiin.openPort(0)

def print_message(midi):
    if midi.isNoteOn():
        print('%2d] ON :' % midi.getChannel(), midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('%2d] OFF:' % midi.getChannel(), midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('%2d] CONTROLLER:' % midi.getChannel(), midi.getControllerNumber(), midi.getControllerValue())

while True:
    m = midiin.getMessage(3600)

    if m:
        buffer = []

        if m.isNoteOn() or m.isNoteOff():
            cmd = 0x90 if m.isNoteOn() else 0x80

            buffer.append(cmd | (m.getChannel() - 1))
            buffer.append(m.getNoteNumber())
            buffer.append(m.getVelocity())

            fd.sendto(bytes(buffer), (multicast_group, multicast_port))

        elif m.isController():
            buffer.append(0xb0 | (m.getChannel() - 1))
            buffer.append(m.getControllerNumber())
            buffer.append(m.getControllerValue())

            fd.sendto(bytes(buffer), (multicast_group, multicast_port))

        elif m.isProgramChange():
            buffer.append(0xc0 | (m.getChannel() - 1))
            buffer.append(m.getProgramChangeNumber())

            fd.sendto(bytes(buffer), (multicast_group, multicast_port))

        else:
            print('Not handled: %s' % m)
