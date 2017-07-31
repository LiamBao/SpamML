# coding: utf-8
import logging


IS_SPAM = 'isspamer'
NUM_WORKERS = 2	#according CPU number
SLEEP = 30

LOG_FILE = './MQspam.log'
LOG_LEVEL = logging.INFO # .INFO, .WARN, .ERROR, .DEBUG
MaxQlen = 10

Fan_queue = {
    'server': 'devfqservice1.iwommaster.com.cn',
    #http://wiki.internal.cicdata.com/confluence/pages/viewpage.action?pageId=17203367
    'works': (
         ('COOP_INNER_SPAMER_%s', 'COOP_INNER_DB_%s'),
         ('COOP_OUTER_SPAMER_%s', 'COOP_OUTER_DB_%s'),
        ),
    'serviceId': 'BIZ06',
    }

Retweet_queue = {
    'server': 'devfqservice1.iwommaster.com.cn',
    'task':{
        'in': 'COOP_OUTER_DISPATCH_BIZ12',
        'out':'COOP_OUTER_DISPATCH_CAL',
        },
    'work':{
        'in': 'COOP_CAL_POST_SERVICES_%s', #serviceId
        'out':'COOP_CAL_ZOMBIE_SERVICES_%s', #serviceId
        },
    'mem_cache':{
        'servers':(
            'xx.xx.xx.xx:11211',
            'xx.xx.xx.xx:11212',
            'xx.xx.xx.xx:11213',
            'xx.xx.xx.xx:11214',
            'xx.xx.xx.xx:11215',
            'xxx.xx.xx.xx:11216',
            'xx.xx.xx.xx:11217',
            ),
        'progress':{
            'key':'COOP_CAL_Post_Progress_%s', #serviceId
            'value': '\x03\x00\x00\x00<' #60
            }
        }
    }

MailInfo = dict(
    From = "xx@xx.com",
    Passwd = "xxx!",
    Server = "xx.xx.com:25",
    Tos = ["liam_bao@163.com",]
)

DBtask_type = {
    'sina':0,
    # 'sina':13,
    'tencent':27
    }

#http://wiki.internal.cicdata.com/confluence/pages/viewpage.action?pageId=20218824
Media_type = {
        'sina':[1,3],
        'tencent':2,
        'weixin':5,
        'bbs':50,
        'news':60,
        'search':70,
        'e-commerce':80,
        }

MQ_URL = 'http://%s/fqservice/service/%s?wsdl'
MQ_SERVICES = {
    'in':  'wsFileMQOutputService',
    'out': 'wsFileMQInputService',
    'del': 'wsFileMQRemoveService',
    'err': 'wsFileMQInputService',
    }

ERROR_SUF = "_ERROR"


USER_ID = 'userId' #str
Features=[
        'beFollowCount',    #bi_followers_count
        'numOfTweets',  
        'numOfFriends',
        'createdAt',    #2010-09-01
        'numOfFans',
        'favouritesCount',
        'verifiedTag',  #replace tag verified for cooperator use
        'verType',
        'gender',   #f:2,
        'description',
        ]

Gender_dic={2:0, 1:1}

mySqlConf = {
    "HOST" : 'xx.xx.xx.xx',
    "USER" : 'xxx',
    "PASS" : 'xx',
    "DB" : 'xx',
    "TABLE" : "xx"
}