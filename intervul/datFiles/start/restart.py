#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Start


class _Restart(_Start):
    def __init__(self, read_by_file=False):
        self.params = [0]

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.params = []
        if len(values) > 0:
            self.params.append(values.popleft())
        else:
            text = ("ERROR: In line " +
                    str(self.reader.lineNum()) +
                    ", the card " + self._mode +
                    " expected at least one value")
            print(text)
            raise Exception(text)

        if len(values) > 0:
            self.params.append(values.popleft())

    def __str__(self):
        text = "RESTART, "
        text += str(self._mode)
        for val in self.params:
            text += ", " + str(val)
        return text


class Continue(_Restart):
    _mode = "CONTIUNE"


class Skip(_Restart):
    _mode = "SKIP"


def select():
    instance = _Restart()
    words = instance.reader.words
    word = words.popleft()

    if word[:5] == 'CONTI':
        instance._should_be(word, 'CONTINUE')
        return Continue(read_by_file=True)

    elif word[:4] == 'SKIP':
        instance._should_be(word, 'SKIP')
        return Skip(read_by_file=True)

    else:
        self._expected(["CONTINUE", "SKIP"],
                       additionalText="after RESTART")
