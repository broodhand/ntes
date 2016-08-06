# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.4'
Stock lib
"""
from .code import Generator, Convert
from .error import CodeError
from .data import get_data


class Base(object):
    def __init__(self, codes_type, scheme='default', timeout=1, retry_session=3, semaphore=20, retry_failure=True):
        if codes_type in Generator.all:
            self.__generator = Generator.function[codes_type]
        else:
            raise CodeError('<ntesDS.stock.Base> Please select OF,SZ or SH')

        self.kwargs = dict()
        self.kwargs['codes_type'] = codes_type
        self.kwargs['scheme'] = scheme
        self.kwargs['timeout'] = timeout
        self.kwargs['retry_session'] = retry_session
        self.kwargs['semaphore'] = semaphore
        self.kwargs['retry_failure'] = retry_failure

        self.__init = False

        self.__data_tuple = None
        self.__data = None
        self.__report = None
        self.__num = None
        self.__codes = None
        self.__content = None

    def init(self):
        if self.__init:
            raise CodeError('<ntesDS.stock.Base> Already init')

        self.__data_tuple = get_data(self.__generator(), scheme=self.kwargs['scheme'], timeout=self.kwargs['timeout'],
                                     retry_session=self.kwargs['retry_session'], semaphore=self.kwargs['semaphore'],
                                     retry_failure=self.kwargs['retry_failure'])
        if self.__data_tuple:
            self.__data = self.__data_tuple[0]
            self.__report = self.__data_tuple[1]
            self.__num = len(self.__data)
            self.__codes = set(self.__data.keys())
            self.__content = list(self.__data.values())

        self.__init = True

    def refresh(self):
        if not self.__init:
            raise CodeError('<ntesDS.stock.Base> Need init first')

        self.__data_tuple = get_data(sorted(self.__codes), scheme=self.kwargs['scheme'], timeout=self.kwargs['timeout'],
                                     retry_session=self.kwargs['retry_session'], semaphore=self.kwargs['semaphore'],
                                     retry_failure=self.kwargs['retry_failure'])
        if self.__data_tuple:
            self.__data = self.__data_tuple[0]
            self.__report = self.__data_tuple[1]
            self.__num = len(self.__data)
            self.__codes = set(self.__data.keys())
            self.__content = list(self.__data.values())

    @property
    def data(self):
        if self.__init:
            return self.__data
        else:
            raise CodeError('<ntesDS.stock.Base> Need init first')

    @property
    def report(self):
        if self.__init:
            return self.__report
        else:
            raise CodeError('<ntesDS.stock.Base> Need init first')

    @property
    def num(self):
        if self.__init:
            return self.__num
        else:
            raise CodeError('<ntesDS.stock.Base> Need init first')

    def codes(self, type_code='ntes'):
        if self.__init:
            return set(map(Convert.callback[type_code], self.__codes))
        else:
            raise CodeError('<ntesDS.stock.Base> Need init first')

    @property
    def content(self):
        if self.__init:
            return self.__content
        else:
            raise CodeError('<ntesDS.stock.Base> Need init first')


class OF(Base):
    def __init__(self, scheme='default', timeout=1, retry_session=3, semaphore=20, retry_failure=True):
        super(OF, self).__init__('OF', scheme=scheme, timeout=timeout, retry_session=retry_session, semaphore=semaphore,
                                 retry_failure=retry_failure)


class SH(Base):
    def __init__(self, scheme='default', timeout=1, retry_session=3, semaphore=20, retry_failure=True):
        super(SH, self).__init__('SH', scheme=scheme, timeout=timeout, retry_session=retry_session, semaphore=semaphore,
                                 retry_failure=retry_failure)


class SZ(Base):
    def __init__(self, scheme='default', timeout=1, retry_session=3, semaphore=20, retry_failure=True):
        super(SZ, self).__init__('SZ', scheme=scheme, timeout=timeout, retry_session=retry_session, semaphore=semaphore,
                                 retry_failure=retry_failure)

