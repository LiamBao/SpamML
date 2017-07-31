# -*- coding: utf-8 -*-
##__author__=='Liam'#
import pymysql as mySqlSvrdb
import logging

class mysqlSvrClient(object):

    def __init__(self, host=None, user=None, passwd=None, port=3306, db=None):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__port = port
        self.__db = db

    def execute_data(self, sql):
        try:
            conn = mySqlSvrdb.connect(host=self.__host,
                                port=self.__port,
                                user=self.__user,
                                passwd=self.__passwd,
                                db=self.__db,
                                charset='utf8')
            cursor = conn.cursor()
            print sql
            cursor.execute(sql)
            conn.commit()
            conn.close()

        except Exception as err:
            print 'Error msg: %s ' %err

    def select_data(self, sql):
        try:
            conn = mySqlSvrdb.connect(host=self.__host,
                                port=self.__port,
                                user=self.__user,
                                passwd=self.__passwd,
                                db=self.__db,
                                charset='utf8'
                                       )
            cursor = conn.cursor()
            cursor.execute(sql)
            alldata = cursor.fetchall()
            # print('  ' + sql + '\n amount of data:  %d' % (len(alldata)))
            cursor.close()
            conn.close()
            return alldata
        except Exception as err:
            print 'Error msg: %s ' %err
