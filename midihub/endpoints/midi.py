import mido

import midihub.simple_logging as logging


mido_kwargs = {
    0x80: ['note'],
    0x90: ['note', 'velocity'],
    0xB0: ['control', 'value'],
}

class MidiIn(object):
    def __init__(self, emit):
        self.emit = emit
        port_names = mido.get_input_names()
        if not port_names:
            raise IndexError("No MIDI input ports found")
        if len(port_names) == 1:
            idx = 0
            logging.info("Choosing MIDI input port %s", port_names[0])
        else:
            print("MIDI input ports:")
            for (idx, name) in enumerate(port_names):
                print("{}. {}".format(idx, name))
            idx = int(raw_input("Which MIDI input port? "))
            assert 0 <= idx < len(port_names)
        self.midi_in = mido.open_input(port_names[idx])

    def run(self):
        for message in self.midi_in:
            code = mido.messages.get_spec(message.type).status_byte
            kwarg_names = mido_kwargs.get(code)
            if kwarg_names:
                self.emit(code, *[getattr(message, kwarg_name) for kwarg_name in kwarg_names])

class MidiOut(object):
    def __init__(self):
        port_names = mido.get_output_names()
        if not port_names:
            raise IndexError("No MIDI output ports found")
        if len(port_names) == 1:
            idx = 0
            logging.info("Choosing MIDI output port %s", port_names[0])
        else:
            print("MIDI output ports:")
            for (idx, name) in enumerate(port_names):
                print("{}. {}".format(idx, name))
            idx = int(raw_input("Which MIDI output port? "))
            assert 0 <= idx < len(port_names)
        self.midi_out = mido.open_output(port_names[idx])

    def emit(self, code, *args):
        kwarg_names = mido_kwargs.get(code)
        if kwarg_names:
            kwargs = {kwarg_name: args[i] for (i, kwarg_name) in enumerate(kwarg_names)}
            self.midi_out.send(mido.Message(mido.messages.get_spec(code).type, **kwargs))


def run_src(arg, emit):
    MidiIn(emit).run()

def make_dst(arg):
    return MidiOut()
