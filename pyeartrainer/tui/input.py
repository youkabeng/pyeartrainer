# -*- coding: utf-8 -*-

KEY_CODE_ENTER = 10
KEY_CODE_SPACE = 32
KEY_CODE_ESC = 27


def wait_key(scr, user_input, expect):
    while user_input not in expect:
        user_input = scr.getch()
    return user_input
