# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:27:34 2017
@author: Thautwarm
"""
from classDefine import class_info, class_type_map
from copy import deepcopy


def type_of(key_name):
    """judge the type of SQL columns """
    for type_map_key in class_type_map:
        for sign in class_type_map[type_map_key]:
            if sign in key_name.lower():
                return type_map_key
    return "varchar(255)"


class Entity:
    def __init__(self, init, name=None):
        if name:
            self.table = name
        if type(init) in (tuple, list):  # 定义一个Entity
            self.type_map = dict()
            for i in init:
                setattr(self, i, None)
                # self.__setattr__(i,None)
                self.type_map[i] = type_of(i)
            self.attrs = set(init)
        else:
            raise TypeError("`init` is a list or tuple.")

    def to_map(self):
        maps = dict()
        for attr in self.attrs:
            value = self[attr]
            if value:
                maps[attr] = value
        return maps

    def __call__(self, **attr_values):
        if attr_values:
            ret = deepcopy(self)
            ret.__init__(attr_values)
            return ret

        return deepcopy(self)

    def get(self, key):
        return getattr(self, key)

    def set(self, key, value):
        if key in self.attrs:
            setattr(self, key, value)
            # self.__setattr__(key,value)

    def __getitem__(self, key):
        return getattr(self, key)


Entities = [Entity(config_i['attrs'], name=config_i['class']) for config_i in class_info]
