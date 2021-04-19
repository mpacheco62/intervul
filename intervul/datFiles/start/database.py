#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Start


class _Database(_Start):
    pass


class In_core(_Database):
    def __str__(self):
        return "DATABASE:IN_CORE"


class Out_of_core(_Database):
    def __str__(self):
        return "DATABASE:OUT_OF_CORE"


def select():
    instance = _Database()
    words = instance.reader.words
    word = words.popleft()
    if word[:5] == 'OUT_O':
        instance._should_be(word, 'OUT_OF_CORE')
        return Out_of_core()

    elif word[:5] == 'IN_CO':
        instance._should_be(word, 'IN_CORE')
        return In_core()

    else:
        instance._expected(["OUT_OF_CORE", "IN_CORE"],
                       additionalText=" after DATABASE")
