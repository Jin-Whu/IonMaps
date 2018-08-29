#!/usr/bin/env python
# coding:utf-8


class IonData(object):
    def __init__(self, lat, lon, altitude, ied, time):
        self._lat = lat
        self._lon = lon
        self._altitude = altitude
        self._ied = ied
        self._time = time


class IonPrf(IonData):
    def __init__(self, lat, lon, altitude, ied, time):
        super(IonPrf, self).__init__(lat, lon, altitude, ied, time)

    @property
    def lat(self):
        return self._lat

    @property
    def lon(self):
        return self._lon

    @property
    def altitude(self):
        return self._altitude

    @property
    def ied(self):
        return tuple(self._ied)

    @property
    def time(self):
        return self.__time


class IonMap(IonData):
    pass
