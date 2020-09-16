# -*- coding: utf-8 -*-
import argparse
import re
import textwrap
from curses import wrapper

import resources
import yaml
from mingus.containers import Bar
from mingus.midi import fluidsynth

from .trainer.interval import IntervalTrainer
from .tui import input

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

soundfont_path = '/usr/share/soundfonts/default.sf2'
audio_driver = 'alsa'


def parse_args():
    parser = argparse.ArgumentParser(
        'Ear Trainer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            This is a very simple ear trainer app with a simple tui.
            Features:
                Interval recognition
                ...
                more to come
        """)
    )
    # basic arguments
    parser.add_argument('-f', '--soundfont', required=True, type=str, help='sound font path')
    parser.add_argument('-r', '--rounds', default=20, type=int, help='how many rounds in a row')
    parser.add_argument('d', '--audio_driver', default='alsa', help='specify an audio driver to use')
    parser.add_argument('t', '--trainer', required=True, type=str, help='specify a trainer')
    args = parser.parse_args()
    if args.trainer == 'interval':
        args = parse_interval_trainer_args(parser)

    return args


def parse_interval_trainer_args(parser: argparse.ArgumentParser):
    parser.add_argument('--level', default='0', type=str, help='custom level config')
    parser.add_argument('--intervals', default='m2,M2', type=str, help='interval names separated by comma')
    parser.add_argument('--melodic', action='store_true', help='make melodic intervals available')
    parser.add_argument('--harmonic', action='store_false', help='make harmonic intervals available')
    parser.add_argument('--ascending', action='store_true', help='make ascending intervals available')
    parser.add_argument('--descending', action='store_false', help='make descending intervals available')
    args = parser.parse_args()
    if args.level:
        if re.match('\\d+', args.level):
            level_config = yaml.load(pkg_resources.read_text(resources, 'level%s.yml' % args.level),
                                     Loader=yaml.FullLoader)
        else:
            with open(args.level, 'r') as config_file:
                level_config = yaml.load('\n'.join(config_file.readlines()))

        if level_config:
            for k, v in level_config.items():
                args.__setattr__(k, v)
    return args


def init(sf, driver):
    global soundfont_path
    global audio_driver
    if sf is not None:
        soundfont_path = sf
    if driver is not None:
        audio_driver = driver
    fluidsynth.init(soundfont_path, audio_driver)


def run():
    args = parse_args()
    init(args.sf, args.audio_driver)

    wrapper(curses_main, trainer=create_trainer(args))


def create_trainer(args):
    if args.trainer == 'interval':
        return IntervalTrainer(args)


# def create_panel(h, l, y, x, str):
#     win = curses.newwin(h, l, y, x)
#     win.erase()
#     win.box()
#     win.addstr(2, 2, str)
#     panel = curses.panel.new_panel(win)
#     return win, panel


def curses_main(stdscr, trainer):
    stdscr.border(0, 0, 0, 0, 0, 0, 0, 0)

    stdscr.clear()
    stdscr.addstr("press SPACE to start...")
    stdscr.refresh()
    input.wait_key(stdscr, stdscr.getch(), [input.KEY_CODE_SPACE])

    level_config = read_level()[0]['levels'][0]
    interval_trainer = interval.IntervalTrainer(level_config)
    sequence = interval_trainer.generate_sequence()

    rounds = len(sequence)
    correct_rounds = 0
    for index, interval_index, options in sequence:
        notes = list(filter(lambda x: x[0] == interval_index, options))[0][2]
        bar = create_bar(notes)
        stdscr.clear()
        stdscr.addstr("now hearing the interval")
        stdscr.refresh()
        fluidsynth.play_Bar(bar, bpm=80)
        stdscr.clear()
        key_lst, option_lst = generate_options(options, interval_trainer)
        prompt = 'what interval you just heard?\n' + ' '.join(option_lst)
        stdscr.addstr(prompt)
        stdscr.refresh()
        user_input_key = input.wait_key(stdscr, stdscr.getch(), key_lst)
        if user_input_key == ord(str(interval_index + 1)):
            correct_rounds += 1
            stdscr.addstr(2, 2, 'correct!\n')
        else:
            correct_answer = option_lst[interval_index]
            stdscr.addstr(2, 2, 'the correct answer is %s\n' % correct_answer)
        stdscr.refresh()
        stdscr.addstr("press SPACE to continue...")
        input.wait_key(stdscr, stdscr.getch(), [input.KEY_CODE_SPACE])
        stdscr.clear()

    stdscr.addstr("your accuracy is %s" % ('{:.2f}'.format(correct_rounds / rounds)))
    stdscr.refresh()
    stdscr.getkey()


def generate_options(option_data, trainer):
    option_lst = [str(t[0] + 1) + '. ' + trainer.get_interval_name(t[1]) for t in option_data]
    key_lst = [ord(str(i + 1)) for i in range(len(option_data))]
    return key_lst, option_lst


def create_bar(notes):
    bar = Bar(meter=(2, 4))
    bar.place_notes(notes[0], 4)
    bar.place_notes(notes[1], 4)
    return bar


if __name__ == '__main__':
    run()
