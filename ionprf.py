#!/usr/bin/env python
# coding:utf-8
"""Plot ionprf."""


import argparse
from datetime import datetime
from ionsao import SAO, SAORecordParser
from iondata import IonPrf
from ionplot import IonGraph


def ionprf_sao(ionfile, output, t, all=False, show=False):
    sao = SAO(ionfile)
    iongraph = IonGraph()
    if all:
        for record in sao:
            parser = SAORecordParser(record)
            datetime = parser.get_time()
            true_height = parser.get_true_height()
            elec_dens = parser.get_elec_dens()
            location = parser.get_location()
            ionprf = IonPrf(location[0], location[1], true_height, elec_dens,
                            datetime)
            iongraph.plot_ionprf(ionprf, output, show)
    elif t:
        pass


def ionprf(ionfile, output, t, format, all=False, show=False):
    if format == 'SAO':
        ionprf_sao(ionfile, output, t, all, show)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('ionprf')
    parser.add_argument('-i', '--input', type=str, help='ion profile')
    parser.add_argument('-o', '--output', type=str, help='output directory')
    parser.add_argument('-t', '--time', type=lambda x:
                        datetime.strftime('%Y%m%dT%H:%M:%S', x),
                        help='time')
    parser.add_argument('-f', '--format', type=str, choices=['SAO'],
                        help='format')
    parser.add_argument('-a', '--all', action='store_true', help='all time')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    args = parser.parse_args()
    ionprf(args.input, args.output, args.time,
           args.format, args.all, args.show)
