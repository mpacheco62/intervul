#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from collections import deque
import os
import io


class _dataListen8(deque):
    def __init__(self, default):
        self.default = default
        super().__init__()

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except IndexError:
            return self.default

    def popleft(self):
        try:
            return super().popleft()
        except IndexError:
            return self.default


def _strToCorrectType(text):

    try:
        value = int(text)
        isNum = True
    except ValueError:
        try:
            value = float(text)
            isNum = True
        except ValueError:
            value = text
            isNum = False
    return isNum, value


class Base_dat:
    reader = None

    def _should_be(self, word, should):
        if word != should:
            print("WARNING: in line ",
                  self.reader.lineNum(),
                  " the card is ",
                  word,
                  " and should be ",
                  should
                  )

    def _expected(self, words, additionalText=None):
        text = "ERROR: in line "
        text += str(self.reader.lineNum())
        text += " expected one of the following cards:["
        for word in words:
            text += word
            text += ", "
        text = text[:-2] + ']'

        if additionalText is not None:
            text += " " + additionalText
        print(text)
        raise Exception(text)

    def _expected_value(self, textError):
        text = "ERROR: in line "
        text += str(self.reader.lineNum())
        text += " expected value: "
        text += textError
        print(text)
        raise Exception(text)

    def _init_by_reader(self, words, values, **kwargs):
        raise NotImplementedError("Please Implement this method")


class _Reader:
    def __init__(self, filename):
        basename = os.path.basename(filename)
        self.filename = filename
        self.dirname = os.path.dirname(filename)
        self.caseName = os.path.splitext(basename)[0]
        self.f = io.open(filename, 'r', encoding="utf-8")
        self._iline = 0
        self.lastLine = " "

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self._iline += 1
            line = self.f.readline()
            if not line:
                raise StopIteration
            # print(str(self._iline) + ": " + line.strip())
            line = line.strip()

            # Para saltarse los comentarios
            if line.startswith('$') or line.startswith('!'):
                return self.__next__()
            line = line.split('!')[0].strip()
            line = line.split('$')[0].strip()

            # Para las continuaciones de linea
            if '\\' in line or '/' in line:
                line = line.split('\\')[0].strip()
                line = line.split('/')[0].strip()
                secondLine = self.__next__()
                line = line + " " + secondLine
            self.lastLine = line
        except StopIteration:
            raise
        except Exception:
            print("Error in line: " + str(self._iline))
            raise
        return line
    next = __next__

    def readLikeVulcan(self):
        # Trata de hacer lo mismo que listen8.f
        equivalentCharacters = ('=', ':', ',')
        line = self.lastLine

        # words = deque()
        # values = deque()
        words = _dataListen8(" ")
        values = _dataListen8(0)
        # Cambia los caracteres por espacios que son equivalentes
        for char in equivalentCharacters:
            line = line.replace(char, ' ')

        for param in line.split():
            param = param.strip()
            isNum, value = _strToCorrectType(param)
            if isNum:
                values.append(value)
            else:
                words.append(value)
        if len(words) > 0 and words[0] == 'ECHO':
            self.next()
            words, values = self.readLikeVulcan()

        self.words = words
        self.values = values
        return words, values

    def lineNum(self):
        return self._iline
