from music21 import converter, instrument, note, chord
import glob

notes = []

counter = 0
for file in glob.glob("data/2002/*.mid"):
    midi = converter.parse(file)

    print("Parsing %s" % file)

    notes_to_parse = None

    try:  # file has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts[0].recurse()
    except:  # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n.pitch) for n in element.notes))


pitchnames = sorted(set(item for item in notes))

# create a dictionary to map pitches to integers
note_to_int = dict((note, number)
                   for number, note in enumerate(pitchnames))


print(note_to_int)
