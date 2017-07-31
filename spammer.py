# coding: utf-8
import sys
import time
import datetime
import json
import copy
import logging
import multiprocessing
from suds.client import Client
import memcache
from service import gSpamersimple
import mailer
from conf import *
from utils import *
from fqMonitor import fqMonitor


#@benchmark
def task_fans():
    serviceId = Fan_queue['serviceId']
    server = Fan_queue['server']
    dealers=create_dealers(server)
    remains = True 
    while remains:
        remains = False
        for work_i in Fan_queue['works']:
            workq = dict(zip(('in','out'), work_i))
            qnames = (workq['in'] %serviceId, workq['out'] %serviceId )
            logging.info('task_fans, server:%s, qnames: %s' %(server, repr(qnames)))
            ndone = process_safe(dealers, qnames, parse_work, 'fans')
            if ndone<0:
                dealers=create_dealers(server)
            if ndone != 0:
                remains = True
 
#@benchmark
def task_retweet():
    taskq = Retweet_queue
    server = taskq['server']
    dealers = create_dealers(server)
    qnames = (taskq['task']['in'], taskq['task']['out'])
    logging.info('task_retweet server:%s, qnames: %s' %(server, repr(qnames)))
    ndone = -1
    while ndone != 0:
        ndone = process_safe(dealers, qnames, parse_task, 'retweet', maxSize = 1)
        if ndone<0:
            dealers = create_dealers(server)


def reflect(s, *args):
    logging.info('reflect')
    return s

#@benchmark
def process_retweet(serviceId, to_work=True):
    taskq = Retweet_queue
    server = taskq['server']
    dealers = create_dealers(server)
    workq = taskq['work']
    qnames = (workq['in'] %serviceId, workq['out'] %serviceId )
    logging.info('process_retweet, qnames: %s' %repr(qnames))
    ndone = -1
    while ndone != 0:
        ndone = process_safe(dealers, qnames, to_work and parse_work or reflect, 'retweet')
        if ndone<0:
            dealers = create_dealers(server)
    """
    update fqMonitordb status
    """
    fqMonitor.update(serviceId)
           
#@benchmark 
def process_safe(dealers, qnames, parse_fn, taskType, maxSize = MaxQlen ):
    log_pre = 'pid:%d, queue names: %s, ' %(current_pid(), qnames) 
    ndone = -1
    try:
        ndone = do_work(dealers, qnames, parse_fn, taskType, maxSize)
        if ndone>0:   
            logging.info('%s processed %d msgs' %(log_pre, ndone))
    except Exception, e:
        notify('%s exception:%s\n traceback: %s' %(log_pre, e, traceback.format_exc()))
    return ndone 

 
#@benchmark
def create_dealers(server_addr):
    dealers={}
    for t in MQ_SERVICES:
        dealers[t] = {}
        dealers[t]['cli'] = cli = Client(MQ_URL %(server_addr, MQ_SERVICES[t]))
        obj_name = (t== 'in') and 'ns0:wsQueryFileMqRQ' or 'ns0:wsFileMqRQ'
        dealers[t]['obj'] = dealers[t]['cli'].factory.create(obj_name)
    return dealers

def parse_task(s, taskType):
    o = json.loads(s)
    logging.info('task object: %s' %o)
    serviceId = o['serviceId']
    """
    ip:10.203.4.203 db:iwmdata
    查询channelID并创建db记录
    """
    fqMonitor.create(serviceId)
    # process_retweet(serviceId, o.get('type') == DBtask_type['sina'])
    process_retweet(serviceId, True)
    update_memcache(serviceId)
    return s

def update_memcache(serviceId):
    minfo = Retweet_queue['mem_cache']
    dic = minfo['progress']
    for serv in minfo['servers']:
        try:
            mc = memcache.Client([serv])
            k, v = dic['key'] %serviceId, dic['value']
            logging.info('update_memcache to %s: %s' %(k,v))
            assert mc.set(k,v)
            break #any success is OK
        except Exception, e:
            notify('update memcache error! server:%s, exception: %s\n traceback: %s' %(serv, e, traceback.format_exc()))
     

def do_work(dealers, qnames, parse_fn, taskType, maxSize):
    logging.info('do_work, qnames: %s, taskType: %s, maxSize: %d' %( qnames, taskType, maxSize))
    o_in = dealers['in']['obj']
    o_in.maxSize = maxSize 
    o_in.queueName = qnames[0]   
    res = dealers['in']['cli'].service.queryFileMQ(o_in)
    assert res.success
    if 'fileNames' not in dir(res) or not res.fileNames or len(res.fileNames)<1:
        """db查询taskq为空, 但任务未完成的状态"""
        if 'COOP_OUTER_DISPATCH_BIZ12' in str(qnames):
            srvIdList = fqMonitor.checkTask()
            if srvIdList:
                gen_svr = '{"serviceId": %d}' %int(str(srvIdList[1]))
                parse_task(gen_svr, 'retweet')
                fq_out = dealers['out']['obj']
                fq_out.messages = []
                fq_out.messages.append(gen_svr)
                fq_out.queueName = qnames[1]
                res = dealers['out']['cli'].service.createFileMQ(fq_out)
                assert res.success
            return 0
        else:
            return 0    #no remain
    fnames = res.fileNames
    logging.info('do work, fnames:%s' %repr(fnames))
    o_out = dealers['out']['obj']
    o_out.messages = []
    o_out.queueName = qnames[1]   
    obj_err = dealers['err']['obj']
    obj_err.messages = []
    obj_err.queueName = qnames[0] + ERROR_SUF
    for fq in res.results:
        logging.warn('in msg num: %d' %len(fq.messages))
        for msg in fq.messages:
            msgout = parse_fn(msg, taskType)
            if msgout:
                o_out.messages.append(msgout)
            else:
                obj_err.messages.append(msg)
    logging.warn('out msg num: %d' %len(o_out.messages))            
    res = dealers['out']['cli'].service.createFileMQ(o_out)            
    assert res.success
    if len(obj_err.messages) > 0:
        logging.info(u'err num: %d' %len(obj_err.messages))
        res = dealers['err']['cli'].service.createFileMQ(obj_err)
        assert res.success
    o_del = dealers['del']['obj']
    o_del.messages = fnames
    o_del.queueName = qnames[0]
    res = dealers['del']['cli'].service.removeFileMQ(o_del)
    assert res.success
    return len(fnames)


def parse_work(s, taskType):
    """if business type not match, return orignal s,
    else modify json object and return dumps
    """
    try:
        o = json.loads(s)
    except Exception, e:
        logging.error(e)
        return None
    if taskType == 'retweet':
        user = o['tweetBean']['tweet']['user']
        proc_user(user)
    elif taskType == 'fans':
        mediatype = o.get('mediaType',-1) 
        logging.info('mediaType: %s' %mediatype)
        if mediatype not in (Media_type['sina']):
            return s
        users = o.get('users',[])
        logging.info('users len: %d' %len(users))
        for user in users:
            proc_user(user)
    else:
        logging.info('unkown taskType: %s' %taskType)
        return s
    return json.dumps(o) 


def proc_user(user):
    fs = []
    for f in Features:
        fs.append(user.get(f,-1))
    fs[3] = get_timestamp(fs[3])
    fs[8] = Gender_dic.get(fs[8], -1)
    fs[9] = len(fs[9])
    user[IS_SPAM]= is_spam(fs, user.get(USER_ID, 0))


def is_spam(row, uid):
    gSpamersimple.add(row, 0, uid)
    judge = gSpamersimple.judge() and 1 or 0
    logging.info('uid:%s, row:%s, %s: %s' %(uid, row, IS_SPAM, judge))
    return judge


def notify(txt):
    logging.warn('notify txt: %s' %txt)
    try:
        info = copy.deepcopy(MailInfo)
        info['Subject'] = u"[SPAMMER]@%s warning" %now_str() 
        info['Txt'] = u'local ip: %s\ntime: %s\n%s' %(local_ip(), now_str(), txt)
        mailer.send(**info)
    except Exception, e:
        logging.error('notify exception: %s' %e)


def main(taskType):
    logging.basicConfig(
            level=LOG_LEVEL,
            filename=LOG_FILE,
            format = '[%(asctime)s] [%(levelname)s]%(message)s')

    pool = multiprocessing.Pool(NUM_WORKERS)   
    args = ((i, taskType) for i in xrange(NUM_WORKERS))
    r = pool.map_async(worker, args)
    r.wait()
    if not r.successful():
        logging.error('worker not completed')


def worker(arg):
    logging.info(arg)
    i, taskType = arg
    while True:
        if taskType == 'retweet':
            task_retweet()
        else:
            task_fans()
        time.sleep(SLEEP)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("""
Usage:
    %s fans/retweet""" %sys.argv[0])
    taskType = sys.argv[1] == 'retweet' and 'retweet' or 'fans'
    main(taskType)
