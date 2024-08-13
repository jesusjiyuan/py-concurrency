# coding: utf-8
import time

import dbhepler
from entity import LinkMonResult, MonVideoResultExt, MonVideoResult, MonKeyword, MonTask, MonLink, MonLinkBatch
from datetime import datetime

class LinkMonResultMapper:
    @classmethod
    def insert(cls,link: LinkMonResult):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        #"values ('"+link.id+"','"+link.pUrl+"','"+link.url+"','"+link.picPath+"','"+str(datetime.now())+"','"+str(link.batchNo)+"')"
        sql = "insert into mon_link_result(id, purl, url, picPath,createTime,batchNo,linkId) " \
        "values ('{id}','{purl}','{url}','{picPath}','{createTime}','{batchNo}','{linkId}')"\
            .format(id=link.id,purl=link.pUrl,url=link.url,picPath=link.picPath,createTime=str(datetime.now()),batchNo=str(link.batchNo),linkId=link.linkId)
        print(sql)
        cursor.execute(sql)
        dbhepler.close(conn)
    @staticmethod
    def list(link: LinkMonResult) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,purl,url,picPath,linkId,status,createTime,updateTime,delFlag,matchPicPath,batchNo,ocrStr,ocrRaw from mon_link_result where delFlag = '0'"
        sql = (sql + " and status = '0' ") if (link.status is None or link.status == '') else (sql + " and status = '{}' ".format(link.status))
        if link.id is not None:
            sql = sql + " and id = '{id}'".format(id=link.id)
        if link.batchNo is not None:
            sql = sql + " and batchNo = '{}'".format(link.batchNo)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            linktmp = LinkMonResult(id=r[0],pUrl=r[1],url=r[2],picPath=r[3],linkId=r[4])
            result.append(linktmp)
        dbhepler.close(conn)
        return result

    @classmethod
    def update(cls,link: LinkMonResult):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        setsql = []
        wheresql = ["where delFlag='0' "]
        # set
        if link.ocrStr is not None:
            setsql.append(" ocrStr='{}'".format(link.ocrStr))
        if link.status is not None:
            setsql.append(" status='{}'".format(link.status))
        if link.picPath is not None:
            setsql.append(" picPath='{}'".format(link.picPath))
        if link.updateTime is not None:
            setsql.append(" updateTime='{}'".format(time.strftime("%Y-%m-%d %H:%M:%S",link.updateTime)))
        # where
        if link.linkId is not None:
            wheresql.append(" linkId='{}'".format(link.linkId))
        if link.pUrl is not None:
            wheresql.append(" pUrl='{}'".format(link.pUrl))
        if link.url is not None:
            wheresql.append(" url='{}'".format(link.url))
        if link.batchNo is not None:
            wheresql.append(" batchNo='{}'".format(link.batchNo))
        sql = "update mon_link_result set "+" , ".join(setsql) + " and ".join(wheresql)
        print(sql)
        cursor.execute(sql)
        dbhepler.close(conn)
    @classmethod
    def updateMatch(cls,link: LinkMonResult):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "update mon_link_result set ocrStr='{ocrStr}',matchPicPath='{matchPicPath}',status='{status}',kwords='{kwords}' where id = '{id}'" \
            .format(id=link.id,ocrStr=link.ocrStr,matchPicPath=link.matchPicPath,status=link.status,kwords=link.kwords)
        print(sql)
        cursor.execute(sql)
        dbhepler.close(conn)
    @staticmethod
    def count(link: LinkMonResult):
        "select id,purl,url,picPath,status,createTime,updateTime,delFlag,matchPicPath,batchNo,ocrStr,ocrRaw from mon_link_result where delFlag = '0'"
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "select count(1) from mon_link_result where delFlag = '0' "
        if link.linkId is not None:
            sql = sql + " and linkId='{}'".format(link.linkId)
        if link.pUrl is not None:
            sql = sql + " and pUrl='{}'".format(link.pUrl)
        if link.url is not None:
            sql = sql + " and url='{}'".format(link.url)
        if link.batchNo is not None:
            sql = sql + " and batchNo='{}'".format(link.batchNo)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchone()
        result = res[0]
        dbhepler.close(conn)
        return result


class MonVideoResultMapper:
    "insert into CC_MZH.mon_video_result(id, vedioUrl, name, status, createTime, delFlag, raw, endTime) "
    @staticmethod
    def list(ved: MonVideoResult =MonVideoResult()) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,vedioUrl,name,status,createTime,delFlag,raw,endTime from mon_video_result where status = '0' and delFlag = '0'"
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            linktmp = MonVideoResult(r[0],r[1],r[2])
            result.append(linktmp)
        dbhepler.close(conn)
        return result
    @staticmethod
    def list_by_ids(ids:list) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,vedioUrl,name,status,createTime,delFlag,raw,endTime from mon_video_result where status = '0' and delFlag = '0'"
        if len(ids) > 0:
            ids = ["'"+str(id)+"'" for id in ids]
            sql = sql + " and id in ({})".format(",".join(ids))
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            linktmp = MonVideoResult(r[0],r[1],r[2])
            result.append(linktmp)
        dbhepler.close(conn)
        return result

    @classmethod
    def update(cls,ved: MonVideoResult):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "update mon_video_result set raw='{raw}',status='{status}',vedioDuration='{vedioDuration}',endTime='{endTime}' where id = '{id}'" \
            .format(id=ved.id,raw=ved.raw,status=ved.status,vedioDuration=ved.vedioDuration,endTime=time.strftime("%Y-%m-%d %H:%M:%S",ved.endTime))
        #print(sql)
        print("MonVideoResultMapper update",ved.id,ved.status)
        cursor.execute(sql)
        dbhepler.close(conn)

class MonVideoResultExtMapper:
    "select id,vId,starts,ends,vSlicePath,kwords from CC_MZH.mon_video_result_ext"
    @classmethod
    def insert(cls,vedio: MonVideoResultExt):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        #"values ('"+link.id+"','"+link.pUrl+"','"+link.url+"','"+link.picPath+"','"+str(datetime.now())+"','"+str(link.batchNo)+"')"
        sql = "insert into mon_video_result_ext(vId, starts, ends, vSlicePath,kwords) " \
              "values ('{vId}','{starts}','{ends}','{vSlicePath}','{kwords}')"\
            .format(vId=vedio.vId,starts=vedio.starts,ends=vedio.ends,vSlicePath=vedio.vSlicePath,kwords=vedio.kwords)
        print(sql)
        cursor.execute(sql)
        dbhepler.close(conn)

    @staticmethod
    def count(vedio: MonVideoResultExt):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "select count(1) from mon_video_result_ext where 1=1 "
        if vedio.vId is not None:
            sql = sql + " and vId='{}'".format(vedio.vId)
        if vedio.starts is not None:
            sql = sql + " and starts='{}'".format(vedio.starts)
        if vedio.ends is not None:
            sql = sql + " and ends='{}'".format(vedio.ends)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchone()
        result = res[0]
        dbhepler.close(conn)
        return result
    @staticmethod
    def update(vedio: MonVideoResultExt):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "update mon_video_result_ext set kwords = concat(kwords,',{kwds}') where vId='{vId}' and starts='{starts}' and ends='{ends}'"\
            .format(vId=vedio.vId,starts=vedio.starts,ends=vedio.ends,kwds=vedio.kwords)
        print(sql)
        cursor.execute(sql)
        dbhepler.close(conn)

class MonKeywordMapper:
    "select id,name,createTime,delFlag from CC_MZH.mon_keyword"
    @staticmethod
    def list(key: MonKeyword =MonKeyword()) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,name,createTime,delFlag from mon_keyword where delFlag = '0' "
        if key.id is not None:
            sql = sql + " and id='{}'".format(key.id)
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            keyw = MonKeyword(r[0],r[1])
            result.append(keyw)
        dbhepler.close(conn)
        return result
    @staticmethod
    def list_by_ids(ids) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,name,createTime,delFlag from mon_keyword where delFlag = '0' "
        if len(ids) > 0:
            ids = [str(id) for id in ids]
            sql = sql + " and id in ({})".format(",".join(ids))
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            keyw = MonKeyword(r[0],r[1])
            result.append(keyw)
        dbhepler.close(conn)
        return result
class MonLinkMapper:
    "select id,name,url,typea,createTime,updateTime,delFlag,business from CC_MZH.mon_link"
    @staticmethod
    def list(link: MonLink =MonLink()) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,name,url,typea,createTime,updateTime,delFlag,business from mon_link where delFlag = '0' "
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            keyw = MonKeyword(r[0],r[1])
            result.append(keyw)
        dbhepler.close(conn)
        return result

    @staticmethod
    def list_by_ids(ids:list,typea:str) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,name,url,typea,createTime,updateTime,business from mon_link where delFlag = '0'  "
        if len(ids) > 0:
            ids = [str(id) for id in ids]
            sql = sql + " and id in ({})".format(",".join(ids))
        if typea is not None:
            sql = sql + " and typea='{}'".format(typea)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            lk = MonLink(id=r[0],name=r[1],url=r[2],typea=r[3])
            result.append(lk)
        dbhepler.close(conn)
        return result


class MonLinkBatchMapper:
    "select id,batchNo,linkId,linkUrl,status,createTime,endTime,delFlag,goodSum from CC_MZH.mon_link_batch"
    @classmethod
    def list(linkBatch: MonLinkBatch) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,batchNo,linkId,linkUrl,status,createTime,endTime,delFlag,goodSum from mon_link_batch where delFlag = '0' "
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            keyw = MonLinkBatch(id=r[0],batchNo=r[1],linkId=r[2],linkUrl=r[3])
            result.append(keyw)
        dbhepler.close(conn)
        return result
    @classmethod
    def update(cls,linkBatch: MonLinkBatch):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "update mon_link_batch set goodSum='{goodSum}' where linkId = '{linkId}'" \
            .format(linkId=linkBatch.linkId,goodSum=linkBatch.goodSum)
        print(sql)
        print("MonLinkBatchMapper update",linkBatch.linkId,linkBatch.goodSum)
        cursor.execute(sql)
        dbhepler.close(conn)
    @classmethod
    def updateSatus(cls,linkBatch: MonLinkBatch):
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql = "update mon_link_batch set status='{status}',endTime='{endTime}' " \
              "where delFlag='0' and batchNo = '{batchNo}' and linkId = '{linkId}'" \
              "and not exists( select id from mon_link_result where batchNo = '{batchNo}' and linkId = '{linkId}' and status = '0' ) " \
            .format(linkId=linkBatch.linkId,batchNo=linkBatch.batchNo,status=linkBatch.status,endTime=time.strftime("%Y-%m-%d %H:%M:%S",linkBatch.endTime))
        print(sql)
        print("MonLinkBatchMapper update",linkBatch.status,linkBatch.endTime)
        cursor.execute(sql)
        dbhepler.close(conn)


class MonTaskMapper:
    "select id,name,batchNo,createTime,updateTime,delFlag,targetIds,kwIds,typea,endTime,status from mon_task"
    @classmethod
    def list(cls,task: MonTask) -> list:
        result = [];
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,name,batchNo,targetIds,kwIds,typea,status,endTime,createTime,updateTime from mon_task where delFlag = '0' "
        if task.typea is not None:
            sql = sql + " and typea='{}' ".format(task.typea)
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            montask = MonTask(id=r[0],batchNo=r[2],targetIds=r[3],kwIds=r[4],typea=r[5])
            result.append(montask)
        dbhepler.close(conn)
        return result
    @staticmethod
    def get_by_batchno(batchNo:str) :
        monTask = None
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="select id,name,batchNo,targetIds,kwIds,typea,status,endTime,createTime,updateTime from mon_task where delFlag = '0' and batchNo='{}' ".format(batchNo)
        cursor.execute(sql)
        r = cursor.fetchone()
        if r is not None:
            monTask = MonTask(id=r[0],batchNo=r[2],targetIds=r[3],kwIds=r[4],typea=r[5])
        dbhepler.close(conn)
        return monTask

    @staticmethod
    def update(task: MonTask) :
        monTask = None
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="update mon_task set status='{status}',endTime='{endTime}' " \
            "where delFlag = '0' and batchNo='{batchNo}' ".format(batchNo=task.batchNo,status=task.status,endTime=time.strftime("%Y-%m-%d %H:%M:%S",task.endTime))
        cursor.execute(sql)

        dbhepler.close(conn)
        return monTask

    @staticmethod
    def updateStatus(task: MonTask) :
        monTask = None
        conn = dbhepler.connect()
        cursor = conn.cursor()
        sql="update mon_task set status='{status}',endTime='{endTime}' " \
            "where delFlag = '0' and batchNo='{batchNo}' and " \
            "not exists( select id from mon_link_batch where batchNo='{batchNo}' and status = '0' )"\
            .format(batchNo=task.batchNo,status=task.status,endTime=time.strftime("%Y-%m-%d %H:%M:%S",task.endTime))
        print(sql)
        cursor.execute(sql)
        dbhepler.close(conn)
        return monTask
