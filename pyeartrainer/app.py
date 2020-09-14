# -*- coding: utf-8 -*-
import curses
import curses.panel
from curses import wrapper

import yaml
from mingus.containers import Bar
from mingus.midi import fluidsynth

import resources
from trainer import interval
from tui import input

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

soundfont_path = '/usr/share/soundfonts/default.sf2'
audio_driver = 'alsa'


def init(sf, driver):
    global soundfont_path
    global audio_driver
    if sf is not None:
        soundfont_path = sf
    if driver is not None:
        audio_driver = driver
    fluidsynth.init(soundfont_path, audio_driver)


def run(args):
    init(args.get('f'), args.get('d'))
    wrapper(curses_main)


def read_level():
    level_config_str = pkg_resources.read_text(resources, 'level.json')
    level_config = yaml.load(level_config_str, Loader=yaml.FullLoader)
    return level_config


def create_panel(h, l, y, x, str):
    win = curses.newwin(h, l, y, x)
    win.erase()
    win.box()
    win.addstr(2, 2, str)
    panel = curses.panel.new_panel(win)
    return win, panel


def curses_main(stdscr):
    stdscr.border(0, 0, 0, 0, 0, 0, 0, 0)

    stdscr.clear()
    stdscr.addstr("press SPACE to start...")
    stdscr.refresh()
    input.wait_key(stdscr, stdscr.getch(), [input.KEY_CODE_SPACE])

    level_config = read_level()[0]['levels'][0]
    interval_trainer = interval.IntervalTrainer(level_config)
    sequence = interval_trainer.generate_sequence()

    for index, interval_index, options in sequence:
        notes = list(filter(lambda x: x[0] == interval_index, options))[0][2]
        bar = create_bar(notes)
        stdscr.clear()
        stdscr.addstr("now hearing the interval")
        stdscr.refresh()
        fluidsynth.play_Bar(bar, bpm=80)
        stdscr.clear()
        key_lst, option_lst = generate_options(options)
        prompt = 'what interval you just heard?\n' + ' '.join(option_lst)
        stdscr.addstr(prompt)
        stdscr.refresh()
        user_input_key = input.wait_key(stdscr, stdscr.getch(), key_lst)
        if user_input_key == ord(str(interval_index + 1)):
            stdscr.addstr(2, 2, 'correct!\n')
        else:
            stdscr.addstr(2, 2, 'not correct!\n')
        stdscr.refresh()
        stdscr.addstr("press SPACE to continue...")
        input.wait_key(stdscr, stdscr.getch(), [input.KEY_CODE_SPACE])
        stdscr.clear()

    stdscr.refresh()
    stdscr.getkey()


def generate_options(option_data):
    option_lst = [str(t[0] + 1) + '. ' + interval.get_interval_name(t[1]) for t in option_data]
    key_lst = [ord(str(i + 1)) for i in range(len(option_data))]
    return key_lst, option_lst


def create_bar(notes):
    bar = Bar(meter=(2, 4))
    bar.place_notes(notes[0], 4)
    bar.place_notes(notes[1], 4)
    return bar


if __name__ == '__main__':
    run({})
