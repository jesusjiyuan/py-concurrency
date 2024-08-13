# coding: utf-8
class LinkMonResult():
    def __init__(self,id=None,pUrl=None,url=None,picPath=None,batchNo=None,ocrStr=None
                 ,ocrRaw=None,status=None,createTime=None,matchPicPath=None,delFlag=None
                 ,kwords=None,linkId=None,updateTime=None):
        self.id = id
        self.pUrl = pUrl
        self.url = url
        self.picPath = picPath
        self.batchNo = batchNo
        self.ocrStr = ocrStr
        self.ocrRaw = ocrRaw
        self.status = status
        self.createTime = createTime
        self.updateTime = updateTime
        self.matchPicPath = matchPicPath
        self.delFlag = delFlag
        self.kwords = kwords
        self.linkId = linkId

class MonVideoResult():
    def __init__(self,id=None,vedioUrl=None,name=None,status=None,createTime=None,raw=None,delFlag=None,vedioDuration=0,endTime=None):
        self.id = id
        self.vedioUrl = vedioUrl
        self.name = name
        self.status = status
        self.createTime = createTime
        self.raw = raw
        self.delFlag = delFlag
        self.vedioDuration = vedioDuration
        self.endTime = endTime

class MonVideoResultExt():
    def __init__(self,id=None,vId=None,start=None,end=None,vSlicePath=None,kwords=None):
        self.id = id
        self.vId = vId
        self.starts = start
        self.ends = end
        self.vSlicePath = vSlicePath
        self.kwords = kwords

class MonKeyword():
    def __init__(self,id=None,name=None):
        self.id = id
        self.name = name

class MonLink():
    def __init__(self,id=None,name=None,url=None,typea=None,createTime=None,updateTime=None,business=None):
        self.id = id
        self.name = name
        self.url = url
        self.typea = typea
        self.createTime = createTime
        self.updateTime = updateTime
        #self.delFlag = delFlag
        self.business = business

class MonLinkBatch():
    def __init__(self,id=None,batchNo=None,linkId=None,linkUrl=None,status=None,createTime=None,endTime=None,goodSum=None):
        self.id = id
        self.batchNo = batchNo
        self.linkId = linkId
        self.linkUrl = linkUrl
        self.status = status
        self.createTime = createTime
        self.endTime = endTime
        #self.delFlag = delFlag
        self.goodSum = goodSum
class MonTask():
    def __init__(self,id=None,name=None,batchNo=None,createTime=None,updateTime=None,targetIds=None,kwIds=None,typea=None,endTime=None,status=None):
        self.id = id
        self.name = name
        self.batchNo = batchNo
        self.createTime = createTime
        self.updateTime = updateTime
        #self.delFlag = delFlag
        self.targetIds = targetIds
        self.kwIds = kwIds
        self.typea = typea
        self.endTime = endTime
        self.status = status