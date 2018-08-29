#!/usr/bin/env python
# codint:utf-8
"""Read SAO(Standard Archiving Output) format."""

import os
import re
import math
import fortranformat as ff
from datetime import datetime
from collections import defaultdict


SAOFORMAT = ['16F7.3', 'A120', '120A1', '15F8.3', '60I2', '16F7.3', '15F8.3',
             '15F8.3', '40I3', '120I1', '15F8.3', '15F8.3', '15F8.3', '40I3',
             '120I1', '15F8.3', '15F8.3', '15F8.3', '40I3', '120I1', '15F8.3',
             '15F8.3', '40I3', '120I1', '15F8.3', '15F8.3', '40I3', '120I1',
             '15F8.3', '15F8.3', '40I3', '120I1', '15F8.3', '40I3', '40I3',
             '40I3', '10E11.6E1', '10E11.6E1', '10E11.6E1', '6E20.12E2',
             '120I1', '10E11.6E1', '15F8.3', '40I3', '120I1', '15F8.3',
             '15F8.3', '40I3', '120I1', '15F8.3', '15F8.3', '15F8.3',
             '15E8.3E1', '120A1', '120A1', '120I1']


SAOFORMATRE = re.compile('(\d{,3})[AEFI].+')


SAOGROUPMAX = 80


class SAOGroup(object):
    def __init__(self, i, elements):
        assert(isinstance(elements, list))
        self.__dataindex = i
        self.__elements = elements

    def __getitem__(self, i):
        return self.__elements[i]

    @property
    def dataindex(self):
        return self.__dataindex

    @property
    def data(self):
        return tuple((value for value in self.__elements if value))


class SAORecord(object):
    def __init__(self, f):
        assert(isinstance(f, file))
        self.__dataindex = list()
        self.__metadata = defaultdict(SAOGroup)
        self.__read(f)

    def __getitem__(self, i):
        return self.__metadata[i]

    def __len__(self):
        return len(self.__metadata)

    @property
    def groups(self):
        return self.__metadata.keys()

    def __read(self, f):
        self.__read_dataindex(f)
        self.__read_data(f)

    def __read_dataindex(self, f):
        for i in range(2):
            line = f.readline()
            if not line:
                return
            for j in range(40):
                self.__dataindex.append(int(line[3*j:3*(j+1)]))

    def __read_data(self, f):
        if len(self.__dataindex) != SAOGROUPMAX:
            return
        for i in range(len(SAOFORMAT)):
            elements = list()
            record_format = SAOFORMAT[i]
            element_max = self.__parse_format(record_format)
            if self.__dataindex[i] == 0:
                line_cnt = 0
            else:
                line_cnt = int(math.ceil(self.__dataindex[i] /
                                         float(element_max)))
            line_reader = ff.FortranRecordReader(record_format)
            for j in range(line_cnt):
                line = f.readline()
                datums = line_reader.read(line)
                elements.extend(datums)
            self.__metadata[i] = SAOGroup(i, elements)

    def __parse_format(self, record_format):
        element_max = SAOFORMATRE.findall(record_format)[0]
        if element_max:
            return int(element_max)
        else:
            return 1


class SAO(object):
    def __init__(self, filepath):
        self.__records = list()
        self.__read(filepath)

    def __getitem__(self, i):
        return self.__records[i]

    def __read(self, filepath):
        with open(filepath) as f:
            fsize = os.fstat(f.fileno()).st_size
            while f.tell() != fsize:
                record = SAORecord(f)
                self.__records.append(record)


class SAORecordParser(object):
    def __init__(self, record):
        self.__record = record

    def get_time(self):
        group = self.__record[2]
        text = ''.join(group.data)
        year = None
        month = None
        day = None
        hour = None
        minute = None
        second = None
        if text[:2] == 'FF':
            year = int(text[2:6])
            month = int(text[9:11])
            day = int(text[11:13])
            hour = int(text[13:15])
            minute = int(text[15:17])
            second = int(text[17:19])
        return datetime(year, month, day, hour, minute, second)

    def get_true_height(self):
        return self.__record[50].data

    def get_elec_dens(self):
        return self.__record[52].data

    def get_location(self):
        group = self.__record[0]
        return group[2], group[3]


if __name__ == '__main__':
    sao = SAO('E:\data\sao\BP440_20170102(002).SAO')
