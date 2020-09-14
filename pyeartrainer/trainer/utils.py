# -*- coding: utf-8 -*-
import random


def random_pick(data):
    if not isinstance(data, list):
        raise ValueError
    _len = len(data)
    return data[random.randint(0, _len - 1)]
