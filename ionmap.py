#!/usr/bin/env python
# coding:utf-8
"""Plot ionex map."""


import argparse
from datetime import datetime
import ionex
import ionplot


def ionmap(ionfile, output, t, format, colorbar=None, area=None, all=False,
           show=False):
    ionexr = ionex.IONEXReader(format)
    iondata = ionexr.read(ionfile)
    iongraph = ionplot.IonGraph(area)
    if not iondata:
        return
    if all:
        for t in sorted(iondata.keys()):
            iongraph.plot_map(iondata[t], output, format, colorbar, show)
    elif t is not None:
        if t in iondata:
            iongraph.plot_map(iondata[t], output, format, colorbar, show)
    else:
        keys = sorted(iondata.keys())
        if len(keys) == 0:
            return
        iongraph.plot_map(iondata[keys[0]], output, format, colorbar)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('ionmap')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='ionex filepath')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='output directory')
    parser.add_argument('-t', '--time',
                        type=lambda s: datetime.strptime(s, '%Y%m%dT%H:%M:%S'),
                        help='time')
    parser.add_argument('-f', '--format', type=str, default='TEC',
                        help='IONEX format')
    parser.add_argument('-c', '--colorbar', type=float, nargs=2,
                        help='min max')
    parser.add_argument('-r', '--region', type=float, nargs=4,
                        help='llcrnrlat urcrnrlat llcrnrlon urcrnrlon')
    parser.add_argument('-a', '--all', action='store_true',
                        help='plot all time')
    parser.add_argument('-s', '--show', action='store_true',
                        help='show picture')
    args = parser.parse_args()
    ionmap(args.input, args.output, args.time, args.format, args.colorbar,
           args.region, args.all, args.show)
