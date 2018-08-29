#!/usr/bin/env python
# coding:utf-8
"""Ion plot (including IONEX Map, NETCDF4 Map, IED Profile)."""


import os
import numpy as np
import matplotlib
if os.name != 'nt':
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from ionex import IONEXMap
from iondata import IonPrf, IonMap


class IonGraph(object):
    def __init__(self, area=None):
        self.__area = area

    def plot_map(self, ionmap, figdir, format, colorbar=None, show=False):
        assert(isinstance(ionmap, IONEXMap))
        if self.__area:
            m = Basemap(
                llcrnrlat=self.__area[0],
                urcrnrlat=self.__area[1],
                llcrnrlon=self.__area[2],
                urcrnrlon=self.__area[3])
            m.drawparallels(np.linspace(self.__area[0], self.__area[1], 6),
                            labels=[1, 0, 0, 0], linewidth=0.)
            m.drawmeridians(np.linspace(self.__area[2], self.__area[3], 6),
                            labels=[0, 0, 0, 1], linewidth=0.)
        else:
            m = Basemap(
                llcrnrlon=min(ionmap.lon[0]),
                urcrnrlon=max(ionmap.lon[0]),
                llcrnrlat=min(ionmap.lat[:, 0]),
                urcrnrlat=max(ionmap.lat[:, 0]))
            lat_size = len(ionmap.lat)
            lon_size = len(ionmap.lon[0])
            m.drawparallels(ionmap.lat[:, 0][0:lat_size:int(lat_size / 5)],
                            labels=[1, 0, 0, 0],
                            linewidth=0.)
            m.drawmeridians(ionmap.lon[0][0:lon_size:int(lon_size / 6)],
                            labels=[0, 0, 0, 1],
                            linewidth=0.)
        m.drawcoastlines()
        m.drawcountries()
        if colorbar:
            m.pcolormesh(ionmap.lon, ionmap.lat, ionmap.data, latlon=True,
                         shading='gouraud', vmin=colorbar[0], vmax=colorbar[1])
        else:
            m.pcolormesh(ionmap.lon, ionmap.lat, ionmap.data, latlon=True,
                         shading='gouraud')
        plt.title('%s %s' % (format, ionmap.time), size=25)
        m.colorbar()

        if show:
            plt.show()
        else:
            figname = '%s-%s.png' % (format,
                                     ionmap.time.strftime('%Y%m%d%H%M%S'))
            plt.savefig(os.path.join(figdir, figname), bbox_inches='tight')
        plt.clf()
        plt.close()

    def plot_3dmap(self, ionmap, figdir):
        pass

    def plot_ionprf(self, ionprf, figdir, show=False):
        assert(isinstance(ionprf, IonPrf))
        plt.plot(ionprf.ied, ionprf.altitude)
        if show:
            plt.show()
        plt.clf()
        plt.close()
