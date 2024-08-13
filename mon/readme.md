
whisper /tmp/vedio/done.mp4  --language Chinese --model large-v3 --model_dir .cache/whisper


0.like:模糊查询
result0 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.like(&#34;%&#34; &#43; &#34;cp&#34; &#43; &#34;%&#34;)).all()
1.notlike&#xff1a;模糊查询&#xff0c;不在查询范围内
result1 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.notlike(&#34;%&#34; &#43; &#34;cp&#34; &#43; &#34;%&#34;)).all()
2.in_:在某个范围内&#xff0c;参数为元组或者列表类型的数据
result2 = db.session.query(Protocols.protocolName).filter(Protocols.id.in_((1, 2))).all()
3.notin_&#xff1a;和in_相反
result3 = db.session.query(Protocols.protocolName).filter(Protocols.id.notin_((1, 2))).all()
4.is_:是否为null的比较
result4 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.is_(None)).all()
5.isnot:不为null
result5 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.isnot(None)).all()
6.startswith&#xff1a;以某个数据开头
result6 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.startswith(&#34;t&#34;)).all()
7.endswith&#xff1a;以某数据结尾
result7 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.endswith(&#34;t&#34;)).all()
8.contains&#xff1a;数据中包含&#xff0c;和like功能差不多
result8 = db.session.query(Protocols.protocolName).filter(Protocols.protocolName.contains(&#34;cp&#34;)).all()
9.desc&#xff1a;对查询出来的数据进行降序排序
result9 = db.session.query(Protocols.protocolName).order_by(Protocols.id.desc()).all()
10.asc&#xff1a;对查询出来的数据进行升序排序
result10 = db.session.query(Protocols.protocolName).order_by(Protocols.id.asc()).all()
11.between&#xff1a;某个字段的参数在某个范围内
result11 = db.session.query(Protocols.protocolName).filter(Protocols.id.between(1, 3)).all()
12.distinct&#xff1a;对查询出来的数据进行去重
result12 = db.session.query(Protocols.parent_protocol).distinct().all()


### 
pip install speedtest-cli
pip install polars -i https://mirror.baidu.com/pypi/simple/
