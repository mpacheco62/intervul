#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Start


class _Future_analysis(_Start):
    pass


class Form1(_Future_analysis):
    def __str__(self):
        return "FUTURE_ANALYSIS: FORM1"


class Form2(_Future_analysis):
    def __str__(self):
        return "FUTURE_ANALYSIS: FORM2"


def select():
    instance = _Future_analysis()

    words = instance.reader.words
    word = words.popleft()
    if word == 'FORM1':
        instance._should_be(word, 'FORM1')
        return Form1()

    elif word == 'FORM2':
        instance._should_be(word, 'FORM2')
        return Form2()

    else:
        instance._expected(["FORM1", "FORM2"],
                       additionalText="after FUTURE_ANALYSIS")
