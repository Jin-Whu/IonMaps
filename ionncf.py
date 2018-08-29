#!/usr/bin/env python
# coding:utf-8
"""Read netCDF4 format."""

import datetime
from netCDF4 import Dataset


class IEDMap(Dataset):
    def __init__(self, filepath):
        super(IEDMap, self).__init__(filepath)

    @property
    def msl_alt(self):
        return self.variables['MSL_alt'][:]

    @property
    def geo_lon(self):
        return self.variables['GEO_lon'][:]

    @property
    def geo_lat(self):
        return self.variables['GEO_lat'][:]

    @property
    def elec_dens(self):
        return self.variables['ELEC_dens'][:]

    @property
    def time(self):
        return datetime(self.year, self.month, self.day,
                        self.hour, self.minute, int(self.second))
