from music21 import converter, instrument, note, chord
import glob
import pickle
import pandas as pd
import multiprocessing


def embedding(year):
    notes = []
    log = []
    folder_name = 'data/' + str(year) + '/*'
    n = len(glob.glob(folder_name))
    counter = 0
    for file in glob.glob(folder_name):
        midi = converter.parse(file)

        print("Parsing %s" % file)
        print(str(year) + ' : ' + str(counter) + '/' + str(n))

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

        with open('data/notes_' + str(year), 'wb') as filepath:
            pickle.dump(notes, filepath)

        with open('data/log_' + str(year), 'wb') as filepath:
            pickle.dump(log, filepath)

        counter += 1


year_list = [2002, 2004, 2006, 2008, 2009, 2011, 2013, 2014, 2015, 2017, 2018]

processes = [ ]
for y in year_list:
    t = multiprocessing.Process(target=embedding, args=(y,))
    processes.append(t)
    t.start()

for one_process in processes:
    one_process.join()

print("Done!")
