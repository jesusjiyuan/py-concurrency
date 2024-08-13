# coding: utf-8
from collections.abc import Generator

from sqlalchemy import and_,text,insert,update,delete,select
from sqlalchemy.orm import Session

from db_mg import DatabaseManagement
from article import article
from cluster import cluster
from articleclusterref import articleclusterref
from tmp_result import result

db = DatabaseManagement()
def get_sesssion():
    with  DatabaseManagement().session as session:
        yield session
    #try:
    #    session = DatabaseManagement().session
    #    return session
    #finally:
    #    session.close()

#sql_cluster = "select * from z_tmp_Cluster where Channel = 'BLR'"
#sql_article = "select * from z_tmp_article"
sql_cluster_c3 = '''select sum(OTB) from z_tmp_Cluster
where Channel = '{}'
group by Channel
'''

sql_cluster_c2 = '''select Account,sum(OTB) from z_tmp_Cluster
where Channel = '{}'
group by Account 
'''

def get_class3(channel:str):
    return db.session.execute(text(sql_cluster_c3.format(channel))).fetchone()


def get_class2(channel: str):
    #db.session.bulk_insert_mappings()
    return db.session.execute(text(sql_cluster_c2.format(channel))).fetchall()



def get_article_all():
    return db.query_all(article)


def get_cluster_all(channel: str):
    return db.query_list(cluster,cluster.Channel== channel)

def query_cluster(channel,account):
    return db.query_list(cluster,and_(cluster.Channel==channel,cluster.Account==account))

#sql_total_pty = 'select rf.ClusterID, a.ID, a.MaxQty, a.MinQty  from z_tmp_assortment rf ' \
#           'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
#           'where a.ID in {0}'
#def get_total_qty(articleIds):
#    try:
#        return db.session.execute(text(sql_total_pty.format(tuple(articleIds)))).fetchall()
#    except:
#        db.session.rollback()
#        db.session.close()

sql_pty = '''
    select isnull(sum(MaxQty),0), isnull(SUM(MinQty),0), ID  from z_tmp_article
    group by ID 
    '''
def get_total_qty():
    return db.session.execute(text(sql_pty)).fetchall()


sql_pty1 = 'select rf.ClusterID, rf.ROS, rf.MinQty,a.ID  from z_tmp_assortment rf ' \
           'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
           'where a.ID = {0}'
def get_cluster_ids(articleId :int):
    return db.session.execute(text(sql_pty1.format(articleId))).fetchall()


sql_pty2 = 'select rf.ClusterID, rf.ROS, rf.MinQty, a.ID, rf.SourceQty,rf.MaxQty  from z_tmp_assortment rf ' \
           'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
           'where a.ID in {0}'
def get_maxmin_qty(articleIds: list):
    return db.session.execute(text(sql_pty2.format(tuple(articleIds)))).fetchall()

update_pty_old = 'update z_tmp_assortment set qty = {} ' \
             'where id  = ( ' \
             '    select rf.ID  from z_tmp_assortment rf ' \
             'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
             'where a.ID = {} ' \
             'and rf.ClusterID = {} ' \
             ')'
def update_pty(articlId,clusterId,val):
    try:
        db.session.execute(text(update_pty_old.format(val,articlId,clusterId)))
        db.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

def update_pty():
    update_pty = "update rf set rf.Qty = r.pty from  z_tmp_assortment rf " \
                 "inner join z_tmp_result r on rf.ArticleID = r.articleId and rf.ClusterID = r.clusterId  "
    try:
        db.session.execute(text(update_pty))
        db.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
def insert_tmp_result(mappers:list):
    sql_delete="delete from z_tmp_result"
    try:
        db.session.execute(text(sql_delete))
        db.session.bulk_insert_mappings(result,mappers)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()


############################################

def get_cluster_column_count():
    sql = """
    select c.ID ,SUM(rf.SourceQty) as total  from z_tmp_Cluster c
    left join z_tmp_assortment rf on c.ID = rf.ClusterID 
    group by c.ID 
    """
    return db.session.execute(text(sql)).fetchall()

def get_article_row_count():
    sql = """
    select a.ID ,SUM(rf.SourceQty) as total  from z_tmp_article a 
    left join z_tmp_assortment rf on a.ID  = rf.ArticleID  
    group by a.ID 
    """
    return db.session.execute(text(sql)).fetchall()

def query_cluster_all():
    return db.session.query(cluster).all()

def query_article_all():
    sql = "SELECT ID, ArticleNo, ProductType, RP, isnull(MaxQty,0) MaxQty, isnull(MinQty,0) MinQty FROM z_tmp_article"
    with DatabaseManagement().session as session:
        return session.execute(text(sql)).fetchall()

def get_xy_data(cluster_seq):
    #([1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20]))
    sql = "select * from ( " \
          "select * from  (select a.ID, rf.ClusterID,rf.Qty,a.ArticleNo from z_tmp_assortment rf " \
          "inner join z_tmp_article a on a.ArticleNo = rf.Article " \
          "left join z_tmp_Cluster c on rf.ClusterID = c.ID " \
          "where c.Channel = 'BLR' ) tmp pivot(sum(tmp.Qty) for tmp.ClusterID in {0}) as P " \
          ") t order by t.ID "
    with DatabaseManagement().session as session:
        return session.execute(text(sql.format(cluster_seq))).fetchall()

def get_qty_by_cluId_and_artId(articleId,clusterId):
    sql = """
    select Qty from z_tmp_assortment
    where ClusterID = {} and ArticleID = {}
    """
    with DatabaseManagement().session as session:
        return session.execute(text(sql.format(clusterId,articleId))).fetchone()
def get_articleclusterref_all():
    with DatabaseManagement().session as session:
        return session.query(articleclusterref).all()