# -*- coding: utf-8 -*-
from mingus.containers import Note

from .utils import random_pick

# all available notes in an octave
NOTE_NAME_LIST = [
    'C', 'C#', 'D', 'D#',
    'E', 'E#', 'F', 'G',
    'G#', 'A', 'A#', 'B'
]

# all available interval qualities
INTERVAL_QUALITY_NAME_DICT = {
    'P': 'perfect',
    'm': 'minor',
    'M': 'major',
    'd': 'diminished',
    'A': 'augmented'
}

# all available interval names
INTERVAL_NUMBER_NAME_DICT = {
    1: 'unison',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'octave'
}


def _next_note(start_note, semitones):
    """get next note by adding semitones to the start_note"""
    return Note().from_int(int(start_note) + semitones)


def _P1_d2(start_note):
    """Perfect unison & Diminished second"""
    return start_note, start_note


def _m2_A1(start_note):
    """Minor second & Augmented unison"""
    return start_note, _next_note(start_note, 1)


def _M2_d3(start_note):
    """Major second & Diminished third"""
    return start_note, _next_note(start_note, 2)


def _m3_A2(start_note):
    """Minor third & Augmented second"""
    return start_note, _next_note(start_note, 3)


def _M3_d4(start_note):
    """Major third & Dimished fourth"""
    return start_note, _next_note(start_note, 4)


def _P4_A3(start_note):
    """Perfect fourth & Augmented third"""
    return start_note, _next_note(start_note, 5)


def _d5_A4(start_note):
    """Diminished fourth & Augmented fourth"""
    return start_note, _next_note(start_note, 6)


def _P5_d6(start_note):
    """Perfect fifth & Diminished sixth"""
    return start_note, _next_note(start_note, 7)


def _m6_A5(start_note):
    """Minor sixth & Augmented fifth"""
    return start_note, _next_note(start_note, 8)


def _M6_d7(start_note):
    """Major sixth & Diminished seventh"""
    return start_note, _next_note(start_note, 9)


def _m7_A6(start_note):
    """Minor seventh & Augmented sixth"""
    return start_note, _next_note(start_note, 10)


def _M7_d8(start_note):
    """Major seventh & Diminished octave"""
    return start_note, _next_note(start_note, 11)


def _P8_A7(start_note):
    """Perfect octave & Augmented seventh"""
    return start_note, _next_note(start_note, 12)


# mappings between interval names and interval functions
INTERVAL_NAME_FUNC_DICT = {
    'P1': _P1_d2, 'd2': _P1_d2, 'm2': _m2_A1, 'A1': _m2_A1,
    'M2': _M2_d3, 'd3': _M2_d3, 'm3': _m3_A2, 'A2': _m3_A2,
    'M3': _M3_d4, 'd4': _M3_d4, 'P4': _P4_A3, 'A3': _P4_A3,
    'd5': _d5_A4, 'A4': _d5_A4, 'P5': _P5_d6, 'd6': _P5_d6,
    'm6': _m6_A5, 'A5': _m6_A5, 'M6': _M6_d7, 'd7': _M6_d7,
    'm7': _m7_A6, 'A6': _m7_A6, 'M7': _M7_d8, 'd8': _M7_d8,
    'P8': _P8_A7, 'A7': _P8_A7
}


def get_interval_name(short_name):
    """build long name based on short name"""
    return '%s %s' % (INTERVAL_QUALITY_NAME_DICT[short_name[0]], INTERVAL_NUMBER_NAME_DICT[int(short_name[1])])


def generate_interval(interval_name, start_note, octave=4, asc=True):
    """build a common interval with two notes"""
    start_note = Note(start_note, octave)
    interval = INTERVAL_NAME_FUNC_DICT[interval_name](start_note)
    return [interval[0], interval[1]] if asc else [interval[1], interval[0]]


def generate_interval_sequence(intervals, asc=True, desc=True, rounds=20):
    """generate a sequence of intervals with a specified number of rounds"""
    interval_names = intervals.split(',')
    sequence = []
    if asc and desc:
        order = [True, False]
    elif desc:
        order = [False, False]
    else:
        order = [True, True]
    for i in range(0, rounds):
        interval_name = random_pick(interval_names)
        interval_index = interval_names.index(interval_name)
        interval_order = random_pick(order)
        interval_start_note = random_pick(NOTE_NAME_LIST)
        options = []
        for j, interval_name in enumerate(interval_names):
            interval = generate_interval(interval_name, interval_start_note, asc=interval_order)
            options.append((j, interval_name, interval))
        sequence.append((i, interval_index, options))
    return sequence
