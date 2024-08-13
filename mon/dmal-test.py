# coding: utf-8
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from spider.Product import Product
from urllib import parse



def main():
    passwd = parse.quote_plus("MONITOR@123.net")
    #dialect 是SQLAlchemy用来与各种类型的DBAPI和数据库通信的系统。
    #conn_url = 'dm+dmPython://SYSDBA: SYSDBA123@192.168.201.118:5236'
    conn_url = 'dm+dmPython://MONITOR:{passwd}@101.227.55.53:15236'.format(passwd=passwd)
    #创建Engine对象
    engine = create_engine(conn_url)
    #创建DBSession对象
    DBSession = sessionmaker(bind=engine)

    fun_select_all(DBSession)
    fun_insert(DBSession)
    # 插入
    fun_select_all(DBSession)
    # 更新
    fun_update(DBSession)
    fun_select_all(DBSession)
    # 删除
    #fun_delete(DBSession)
    fun_select_all(DBSession)

def fun_select_all(DBSession):
    # 创建Session
    session = DBSession()
    # 查询所有的
    list_product = session.query(Product).all()
    print('查询所有结果：')
    for product in list_product:
        print(product.NAME, product.AUTHOR, product.PUBLISHER )
    print('')
    session.close()

def fun_insert(DBSession):
    # 创建Session
    session = DBSession()
    new_product = Product()
    new_product.PRODUCTID='2'
    new_product.NAME = '水浒传'
    new_product.AUTHOR = '施耐庵，罗贯中'
    new_product.PUBLISHER = '中华书局'
    new_product.PUBLISHTIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    new_product.PRODUCTNO = '97871010461371'
    new_product.SATETYSTOCKLEVEL = '10'
    new_product.ORIGINALPRICE = '19'
    new_product.NOWPRICE = '14.3'
    new_product.DISCOUNT = '7.5'
    new_product.DESCRIPTION = '''  《水浒传》是宋江起义故事在民间长期流传基础上产生出来的，吸收了民间文学的营养。'''
    new_product.PHOTO = ''
    new_product.TYPE = '16'
    new_product.PAPERTOTAL = '922'
    new_product.WORDTOTAL = '912000'
    new_product.SELLSTARTTIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    new_product.SELLENDTIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    session.add(new_product)
    session.commit()
    print('插入成功')
    session.close()

def fun_update(DBSession):
    # 创建Session
    session = DBSession()
    product = session.query(Product).filter(Product.NAME == '水浒传').one()
    product.NAME = '水浒'
    session.commit()
    print('更新成功')
    session.close()

def fun_delete(DBSession):
    # 创建Session
    session = DBSession()
    session.query(Product).filter(Product.NAME == '水浒').delete()
    session.commit()
    print('删除成功')
    session.close()

if __name__ == '__main__':
    main()
