# coding: utf-8
#__author__= liam
import sys
import json
import copy
import logging
from sqlClient import *
from conf import *
import utils as utils

"""
fq监测优化
"""
class fqMonitor(object):

    __host = mySqlConf['HOST']
    __user = mySqlConf['USER']
    __passwd = mySqlConf['PASS']
    __db = mySqlConf['DB']
    __table = mySqlConf['TABLE']

    @classmethod
    def create(cls, serviceID=None):
        self = cls()

        try:
            createSql = "INSERT INTO {}.{} "\
                        " (CHANNEL_ID , MEDIA_TYPES, STEP, STATUS, DATA_STATUS, TASK_FQ_CONTENT, " \
                        " CREATE_TIME, UPDATE_TIME, CREATE_USER, UPDATE_USER, DELETE_FLAG )" \
                        " SELECT DISTINCT {}, 1, 5, 0 , 0, null, '{}', null, 'system', null, 0 " \
                        " FROM {}.{} " \
                        " WHERE EXISTS ( " \
                        " SELECT * FROM {}.{} " \
                        " WHERE CHANNEL_ID =  {} AND STEP = 4 AND STATUS = 2)" \
                        " AND NOT EXISTS (  " \
                        " SELECT * FROM {}.{} " \
                        " WHERE CHANNEL_ID =  {} AND STEP = 5 )".format( self.__db, self.__table,
                                                                         serviceID,
                                                                         utils.now_str(),
                                                                         self.__db, self.__table,
                                                                         self.__db, self.__table,
                                                                         serviceID,
                                                                         self.__db, self.__table,
                                                                         serviceID)

            mysqlSvrClient(host=self.__host,
                           user=self.__user,
                           passwd=self.__passwd,
                           port=3306,
                           db=self.__db).execute_data(createSql)
        except Exception, e:
            logging.error(e)


    @classmethod
    def update(cls, serviceId=None):
        self = cls()

        try:
            createSql = "UPDATE {}.{}" \
                        " SET STATUS=2 " \
                        " WHERE CHANNEL_ID = {} AND STEP = 5 ".format(self.__db, self.__table,
                                                                      serviceId)

            mysqlSvrClient(host=self.__host,
                           user=self.__user,
                           passwd=self.__passwd,
                           port=3306,
                           db=self.__db).execute_data(createSql)
        except Exception, e:
            logging.error(e)


    @classmethod
    def checkTask(cls):
        self = cls()

        try:
            selectSql = " SELECT * FROM {}.{}" \
                        " WHERE STEP = 5 AND STATUS != 2 ".format(self.__db, self.__table)

            fetchall = mysqlSvrClient(host=self.__host,
                           user=self.__user,
                           passwd=self.__passwd,
                           port=3306,
                           db=self.__db).select_data(selectSql)
            """每次取到一个ServiceList"""
            return fetchall[0] if fetchall else None

        except Exception, e:
            logging.error(e)

# if __name__=='__main__':
#     print str(fqMonitor.checkTask()[1])