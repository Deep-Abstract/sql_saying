# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:08:10 2017
@author: Thautwarm

Updated on Oct 28 2017
@author: Thautwarm

DONE:
    - To meet PEP8 demands.
    - To make it totally scripted as to make it easier to be integrated in your project.
"""

import pymysql

from entity import Entity
from pymysql.cursors import DictCursor
from daoDetails import dbargs

dbargs['charset'] = "utf8"

dbargs['use_unicode'] = True

getDataBase = lambda: pymysql.connect(**dbargs)




class deploy:
    """
    you can easily create a table associated with an entity in this way:
        (if I write a class named "user" in "config.json")
        
        from dao import deploy
        from entity import entities
        user=entities.user
        deploy(user).create_table()
        # now the table named user is established.
    
    also you can destroy a table named "user" in this way:
        from dao import deploy
        from entity import entities
        user=entities.user
        deploy(user).dropTable()
    
    and you can create all the tables associated with "config.json" in this way:
        from sql_say import entity,deploy
        entities=entity.entities
        for entity_i in entities.attrs:
            dao.deploy(entities.get(entity_i)).createTable()

    """

    def __init__(self, entity):
        if isinstance(entity, Entity):
            self.entity = entity
            self.table = entity.table
        elif isinstance(entity, str):
            self.entity = None
            self.table = entity
        else:
            raise ValueError("Invalid argument type.")

    def create_table(self):
        entity = self.entity
        db = getDataBase()

        sql = "create table if not exists %s(%s)ENGINE=MyISAM DEFAULT CHARSET=UTF8;;"
        type_map = entity.type_map

        if 'id' not in type_map:
            # `id` field's type should be `int`
            type_map.update({'id': 'int'})

        attrs = ''.join(
            "{} {} {}".format(key,
                              type_map[key],
                              'primary key auto_increment,' if key == 'id' else ',') for key in type_map)

        with db:
            cur = db.cursor()
            cur.execute(sql % (entity.table, attrs[:-1]))
            cur.close()
        db.close()

    def drop_table(self):
        sql = 'drop table {};'.format(self.table)
        db = getDataBase()
        print(sql)
        with db:
            cur = db.cursor()
            cur.execute(sql)
            cur.close()
        db.close()


# explain: the abstraction of some trivial SQL operations.
# explain: SQL操作抽象函数
def send_execute(conn, sql, mode='void'):
    """
    execute SQL statements and return a corresponding reuslt decided by the param "mode".
    """
    with conn:
        cur = conn.cursor(DictCursor)
        if mode == 'void':
            ret = cur.execute(sql)
            cur.close()
            return ret
        elif mode == 'count':
            ret = cur.execute(sql)
            cur.close()
        elif mode == 'df':
            cur.execute(sql)
            ret = cur.fetchall()
            cur.close()
        else:
            ret = None
            cur.close()
    return ret


def make_attr_arr(table, **maps):
    """
    each SQL operations will be done with passing the params like this way:
        userdao.delete(username='saber',password='123456')
    and this function is to dealing with the params to convert them into two lists, \
    first of which is a list of Keys, the other a list of Values (converted to string form) correspond with the Keys.

    for instance,
    function "makeAttrArr({'a':1,'b':2})" will return "(['a','b'],['1','2'])"
    """
    entity = maps.get(table)
    if entity:
        maps = entity.toMap()
    if not maps:
        return

    key_arr = []
    value_arr = []
    for key in maps:
        key_arr.append(key)
        value = maps[key]
        value_arr.append("'{}'".format(value))
    return key_arr, value_arr


# end explain

def make_multi_attr_arr(table, maps_iterator):
    return [make_attr_arr(table, **maps) for maps in maps_iterator]


class baseDao:
    def __init__(self, table_name):
        self.table = table_name
        self.conn = getDataBase()

    def add(self, **maps):
        """add record.
        configurations = dict(filed0 = value0)
        add(field1 = value1, field2 = value2, **configurations)

        增加记录（不判断重复）
        """
        attr_arr = make_attr_arr(self.table, **maps)
        if not attr_arr:
            return

        key_arr, value_arr = attr_arr

        sql = "insert into {} ({}) values ({});".format(self.table,
                                                        ','.join(key_arr),
                                                        ','.join(value_arr))
        conn = self.conn
        return send_execute(conn, sql)

    def add_multiple(self, key_arr, values):
        """add records.
        add_multiple([column1, ...], [[value1_1, ...],
                                      [value2_1, ...],
                                      ...
                                      ])
        增加多条记录（不判断重复）
        """

        def make_unit(value_arr):
            return '({})'.format(','.join(map(lambda v: "'{}'".format(v), value_arr)))

        if not values:
            return

        sql = 'insert into {} ({}) values {};'.format(self.table,
                                                      ','.join(key_arr),
                                                      ','.join(map(make_unit, values)))
        conn = self.conn
        return send_execute(conn, sql)

    def delete(self, **maps):
        """delete records.
        删除记录（不判断重复）
        """
        attr_arr = make_attr_arr(self.table, **maps)
        if not attr_arr:
            return

        key_arr, value_attr = attr_arr

        sql = 'delete from {} where {};'.format(self.table,
                                                ' and '.join('='.join(key_pair)
                                                             for key_pair in zip(key_arr, value_attr)))
        conn = self.conn
        return send_execute(conn, sql)

    def check(self, **maps):

        """check how many records matched with the key-value pairs in the database.
        """
        attr_arr = make_attr_arr(self.table, **maps)
        if not attr_arr:
            return

        key_arr, value_arr = attr_arr

        sql = "select * from {} where {} limit 1;".format(
            self.table,
            ' and '.join('='.join(key_pair)
                         for key_pair in zip(key_arr, value_arr)))

        conn = self.conn
        return send_execute(conn, sql, mode='count')

    def select(self, **maps):
        """select the records matched with the key-value pairs in the database,
        which return a list of dict object like this way:

        print(userdao.select(username='archer'))
        >>>[{'id':5,'username':'archer','password':'emiya','access':4,...},
            {'id':6,'username':'archer','password':'gilgamesh','access':1,...},
            ...
            ]
        """
        attr_arr = make_attr_arr(self.table, **maps)
        if not attr_arr:
            return

        key_arr, value_arr = attr_arr

        conn = self.conn
        sql = "select * from {} where {};".format(self.table,
                                                  ' and '.join('='.join(key_pair)
                                                               for key_pair in zip(key_arr, value_arr)))
        return send_execute(conn, sql, mode='df')

    def select_all(self):
        """return the results of SQL statements "SELECT * FROM %s;"%tableName
        """
        conn = self.conn
        sql = "select * from {}".format(self.table)
        return send_execute(conn, sql, mode='df')

    def change(self, **maps):
        """
        change the information of selected records.
        
        match the records by passing key-value pairs.
        and change the value of specific field by passing _key-value pairs, \
        like this way:
        
        userdao.change(username='caster',_username="rider")
        #you change usernames of all the records whose username are 'caster' to 'rider'. 
        """
        attr_arr = make_attr_arr(self.table, **maps)
        if not attr_arr:
            return

        key_arr = []
        value_arr = []
        to_key_arr = []  # names of the fields which will be updated.
        to_value_arr = []  # values of the fields which will be updated.

        for key, value in zip(*attr_arr):
            if key[0] == '_':
                to_key_arr.append(key[1:])
                to_value_arr.append(value)
            else:
                key_arr.append(key)
                value_arr.append(value)

        conn = self.conn

        sql = "UPDATE {} SET {} WHERE {};".format(
            self.table,

            ','.join('='.join(to_key_pair)
                     for to_key_pair in zip(to_key_arr, to_value_arr)),

            ' and '.join('='.join(key_pair)
                         for key_pair in zip(key_arr, value_arr)))

        return send_execute(conn, sql)

    def __del__(self):
        self.conn.close()
