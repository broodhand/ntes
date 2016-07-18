# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""
import logging; logging.basicConfig(level=logging.DEBUG)
from collections import Iterator


def cut_seq(items, slices):
    """
    To slice sequence by var slices
    :param items: Input list,tuple or Generator.
    :param slices: slices number
    :return: Generator which yield slices tuple.
    """
    if isinstance(items, (list, tuple)):
        if len(items) < slices:
            yield tuple(items,)
        else:
            for index in range(0, len(items), slices):
                yield tuple(items[index:index + slices])

    elif isinstance(items, Iterator):
        itemlist = list()
        for item in items:
            itemlist.append(item)
            if len(itemlist) == slices:
                yield tuple(itemlist)
                itemlist = list()
        if len(itemlist) > 0:
            yield tuple(itemlist)

    else:
        raise TypeError('Must input list tuple or Generator')


def merge(x, y):
    """
    To use for updating dict y's key to dict x's key include sub dict's key.
    :param x: must be dict. To be updating.
    :param y: must be dict. update y's key to x.
    :return: return new dict x which is updated by y.
    """
    for k, v in y.items():
        if not isinstance(v, dict):
            x[k] = v
        else:
            if k in x.keys():
                merge(x[k], v)
            else:
                x[k] = v
    return x
