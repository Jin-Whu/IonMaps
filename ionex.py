#!/usr/bin/env python
# coding:utf-8
"""Read IONEX(IONosphere map EXchange) format."""

import os
from datetime import datetime
import numpy as np


class IONEXMap(object):
    def __init__(self, dim, nlat, nlon, nheight=1):
        self.num = None
        self.time = None
        self.dim = dim
        self.__lat = np.zeros((nheight, nlat, nlon))
        self.__lon = np.zeros((nheight, nlat, nlon))
        self.__height = np.zeros(nheight)
        self.__data = np.zeros((nheight, nlat, nlon))

    @property
    def lon(self):
        if self.dim == 2:
            return self.__lon[0]
        else:
            return self.__lon

    @property
    def lat(self):
        if self.dim == 2:
            return self.__lat[0]
        else:
            return self.__lat

    @property
    def height(self):
        if self.dim == 2:
            return self.__height[0]
        else:
            return self.__height

    @height.setter
    def height(self, value):
        if self.dim == 2:
            self.__height = value

    @property
    def data(self):
        if self.dim == 2:
            return self.__data[0]
        else:
            return self.__data


class IONEXData(dict):
    def __init__(self):
        super(IONEXData, self).__init__()
        self.dim = 0
        self.exponent = -1
        self.interval = 0
        self.elecutoff = 0.
        self.lat = None
        self.lon = None
        self.height = None


class IONEXReader(object):
    def __init__(self, mark='TEC'):
        self.__mark = mark

    def __readhead(self, f, data):
        valid = False
        cnt = 0
        for line in f:
            line = line.rstrip()
            if cnt == 0:
                if line[60:] != 'IONEX VERSION / TYPE':
                    return valid
                cnt += 1
            elif line[60:] == 'INTERVAL':
                data.interval = int(line[:6])
            elif line[60:] == 'ELEVATION CUTOFF':
                data.elecutoff = float(line[:8])
            elif line[60:] == 'MAP DIMENSION':
                data.dim = int(line[:6])
            elif line[60:] == 'EXPONENT':
                data.exponent = int(line[:6])
            elif line[60:] == 'HGT1 / HGT2 / DHGT':
                hgt1 = float(line[2:8])
                hgt2 = float(line[8:14])
                dhgt = float(line[14:20])
                data.height = np.arange(hgt1, hgt2 + dhgt, dhgt) \
                    if dhgt > 0. else hgt1
            elif line[60:] == 'LAT1 / LAT2 / DLAT':
                lat1 = float(line[2:8])
                lat2 = float(line[8:14])
                dlat = float(line[14:20])
                data.lat = np.arange(lat1, lat2 + dlat, dlat)
            elif line[60:] == 'LON1 / LON2 / DLON':
                lon1 = float(line[2:8])
                lon2 = float(line[8:14])
                dlon = float(line[14:20])
                data.lon = np.arange(lon1, lon2 + dlon, dlon)
            elif line[60:] == 'END OF HEADER':
                valid = True
                return valid
        return valid

    def __readbody(self, f, data):
        ionexmap = None
        ilat = 0
        iheight = 0
        for line in f:
            line = line.rstrip()
            if line[60:] == 'START OF %s MAP' % self.__mark:
                if data.dim == 2:
                    ionexmap = IONEXMap(data.dim, len(data.lat), len(data.lon))
                elif data.dim == 3:
                    ionexmap = IONEXMap(data.dim, len(data.lat), len(data.lon),
                                        len(data.height))
                ionexmap.num = int(line[:6])
            elif line[60:] == 'EPOCH OF CURRENT MAP' and ionexmap:
                ionexmap.time = datetime(
                    int(line[:6]), int(line[6:12]), int(line[12:18]),
                    int(line[18:24]), int(line[24:30]), int(line[30:36]))
            elif line[60:] == 'LAT/LON1/LON2/DLON/H' and ionexmap:
                lat = float(line[2:8])
                lon1 = float(line[8:14])
                lon2 = float(line[14:20])
                dlon = float(line[20:26])
                height = float(line[26:32])
                nlon = int((lon2 - lon1) / dlon + 1)
                values = list()
                for i in range(int(np.ceil(nlon / 16))):
                    line = next(f)
                    values.extend(
                        list(map(lambda x: float(x) * pow(10, data.exponent),
                                 line.split())))
                if data.dim == 2:
                    ionexmap.lat[ilat] = [lat] * nlon
                    ionexmap.lon[ilat] = np.arange(lon1, lon2 + dlon, dlon)
                    ionexmap.data[ilat] = values
                    ilat += 1
                elif data.dim == 3:
                    ionexmap.lat[iheight, ilat] = [lat] * nlon
                    ionexmap.lon[iheight, ilat] = np.arange(lon1, lon2 + dlon,
                                                            dlon)
                    ionexmap.data[iheight, ilat] = values
                    ilat += 1
            elif line[60:] == 'END OF %s MAP' % self.__mark and ionexmap:
                if ionexmap.dim == 2:
                    ionexmap.height = height
                elif ionexmap.dim == 3:
                    ionexmap.height[iheight] = height
                    iheight += 1
                data[ionexmap.time] = ionexmap
                ilat = 0
                if ionexmap.dim == 3:
                    if iheight == len(data.height):
                        iheight = 0
                ionexmap = None
            elif line[60:] == 'START OF RMS MAP':
                break

    def read(self, filepath):
        """Read IONEX file."""
        data = IONEXData()
        if not os.path.isfile(filepath):
            return None
        with open(filepath) as f:
            if not self.__readhead(f, data):
                return None
            self.__readbody(f, data)
        return data
