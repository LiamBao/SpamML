# coding: utf-8
import logging


IS_SPAM = 'isspamer'
NUM_WORKERS = 8	#according CPU number
SLEEP = 300

LOG_FILE = './MQspam.log'
LOG_LEVEL = logging.WARN # .INFO, .WARN, .ERROR, .DEBUG
MaxQlen = 10

Fan_queue = {
    'server': 'xxx.xx.xx.xxx:8780',
    #http://wiki.internal.cicdata.com/confluence/pages/viewpage.action?pageId=17203367
    'works': (
         ('COOP_INNER_SPAMER_%s', 'COOP_INNER_DB_%s'),
         ('COOP_OUTER_SPAMER_%s', 'COOP_OUTER_DB_%s'),
        ),
    'serviceId': 'BIZ06',
    }

Retweet_queue = {
    'server': 'xxx.xx.xx.xxx:8480',
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
            'xxx.xx.xx.xxx:11214',
            'xxx.xx.xx.xxx:11215',
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
    Tos = ["xxx@xx.com",]
)
DBtask_type = {
    'sina':13,
    'tencent':27
    }

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

