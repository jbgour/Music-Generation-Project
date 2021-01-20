from music21 import converter, instrument, note, chord
import glob
import pickle
import pandas as pd

notes = []
log = []

for file in glob.glob("data/2011/*"):
    midi = converter.parse(file)

    print("Parsing %s" % file)

    notes_to_parse = None

    notesInt = []

    try:  # file has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        i = 0
        notes_to_parse = []
        while len(notes_to_parse) == 0 and i < len(s2.parts):
            notes_to_parse = s2.parts[2].recurse()

    except:  # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notesInt.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notesInt.append('.'.join(str(n.pitch) for n in element.notes))

    notes += notesInt
    log.append(file + ':' + str(len(notesInt)))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    with open('data/log', 'wb') as filepath:
        pickle.dump(log, filepath)
