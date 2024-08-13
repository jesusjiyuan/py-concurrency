# coding:utf-8
from person import Person
from db_mg import DatabaseManagement
from sqlalchemy import and_,text
from article import article


if __name__=="__main__":
    db = DatabaseManagement()
    sql = 'select * from z_tmp_article;'
    results = db.session.execute(text(sql)).fetchall()
    for a in results:
        print(a.ID ,a.ArticleNo)

    articles = db.query_all(article)
    for a in articles:
      print(a.ID ,a.ArticleNo)

    tmps = db.session.query(article).filter(article.ID==1).first()
    print(tmps.ID ,tmps.ArticleNo)
