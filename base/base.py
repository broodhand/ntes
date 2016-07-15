# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""
from collections import Iterator
import inspect
import logging
logging.basicConfig(level=logging.DEBUG)


def vaildargs(*args, **kwargs):

    def decorator(func):
        varargs, varargname, kwname = inspect.signature()

        def wrapper(*funcargs, **funckwargs):
            pass
            return func(*funcargs, **funckwargs)

        return wrapper

    pass
    return decorator


# 生成所有可能代码,digit为生成代码位数，输入list生成所有位数代码和,输出为generator
def generate_code(digit=6):
    # 输入参数检测
    def __check_para():
        digittype = (int, list, tuple)  # 输入代码位数类型列表
        if not isinstance(digit, digittype):
            raise TypeError('digit ERROR:digit must be %s' % str(digittype))

    # 根据输入位数生成代码generator
    def __get_code(dit):
        if not isinstance(dit, int):
            raise TypeError("dit ERROR:dit must be int")
        elif dit < 0:
            raise ValueError('dit ERROR:dit must more than 0')
        return (str(x).zfill(dit) for x in range(10 ** dit))

    # 主体程序,输出generator
    def __exec():
        if isinstance(digit, int):
            return __get_code(digit)  # 输入为int直接调用__get_code()生成generator
        elif isinstance(digit, (list, tuple)):
            r = list()
            for l in map(__get_code, digit):
                r += l
            return (x for x in r)  # 输入为list,tuple用map合并结果生成generator

    # Start
    __check_para()
    return __exec()


# 对sequence进行切片,输出为generator
def cut_seq(items, slices=1000):
    # 输入参数检测
    def __check_para():
        itemstype = (list, tuple, Iterator)  # 输入代码类型列表
        if not isinstance(items, itemstype):
            raise TypeError('codes ERROR:codes must be %s' % str(itemstype))

        if not isinstance(slices, int):
            raise TypeError('slices ERROR:slices must be int')
        elif not slices > 0:
            raise ValueError('slices ERROR:slices must more than 0')

    # 主体程序, 输出generator
    def __exec():
        if isinstance(items, (list, tuple)):
            for index in range(0, len(items), slices):
                yield tuple(items[index:index + slices])

        if isinstance(items, Iterator):
            itemlist = list()
            for item in items:
                itemlist.append(item)
                if len(itemlist) == slices:
                    yield tuple(itemlist)
                    itemlist = list()
            yield tuple(itemlist)

    # Start
    __check_para()
    return __exec()


# 可变参数处理,输入tuple,输出为generator
def process_varpara(para):
    def __check_para():
        paratypelist = (tuple,)
        if not isinstance(para,paratypelist):
            raise TypeError('para ERROR:para must be tuple')

    def __check_subpara():
        subparatypelist = (str, int, tuple, list, Iterator)

    def __exec():
        for item in para:
            if isinstance(item, (tuple, list, Iterator)):
                for data in process_varpara(item):
                    yield data
            elif isinstance(item, (int, str)):
                yield item


def merge(x, y):
    """
    merge x and y .
    :param x: must be dict
    :param y: must be dict
    :return: dict
    """
    for k, v in y.items():
        if not isinstance(v, dict):
            x[k] = v
        else:
            if k in x.keys():
                merge(x[k], v)
            else:
                x[k] = v
