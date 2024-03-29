# coding:utf-8
from sqlalchemy import Column, String, DateTime,Integer,VARCHAR,create_engine,MetaData,Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os
import json
import config
BaseModel = declarative_base()

class Scanner(BaseModel):
    __tablename__ = 'Scanner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15))
    port = Column(Integer,nullable=False)
    flag = Column(String(30)) #这个作用标识每次扫描的结果
    createdatetime = Column(DateTime(), default=datetime.datetime.utcnow)

#sqlite数据库文件位置
DATABASE_PATH = os.path.join(config.BASE_DIR, 'data/data.db')
# 初始化数据库连接:
engine = create_engine('sqlite:///' + DATABASE_PATH, echo=False, connect_args={'check_same_thread': False})
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

class SqlHelper(object):
    params = {'ip': Scanner.ip, 'port': Scanner.port,'flag':Scanner.flag}
    @staticmethod
    def create_db():
        BaseModel.metadata.create_all(engine)

    @staticmethod
    def drop_db():
        BaseModel.metadata.drop_all(engine)

    @staticmethod
    def execute(sql):
        conn = engine.connect()
        conn.execute(sql)
        conn.close()

    @staticmethod
    def deduplication():
        SqlHelper.execute('DELETE FROM Scanner \
WHERE rowid IN \
   (SELECT p.rowid \
    FROM Scanner p \
    INNER JOIN \
         (SELECT ip, port, MIN(rowid) As min_id \
          FROM Proxy_Main \
          GROUP BY ip, port \
          HAVING COUNT(*) > 1) AS agg \
    ON p.ip = agg.ip AND p.port = agg.port \
    AND p.rowid <> agg.min_id);')
    @staticmethod
    def query(sql,count=0):
        conn = engine.connect()
        if count == 0:
            result = conn.execute(sql).fetchall()
        else:
            result = conn.execute(sql).fetchmany(count)
        conn.close()
        fields = []
        for field in Scanner.__dict__:
            if '_' not in field:
                fields.append(field)
        dict_result = []
        for row in result:
            temp = {}
            #例如 ('id',3)
            for column in row.items():
                if(column[0] in SqlHelper.params.keys()):
                    temp[column[0]] = column[1]
            dict_result.append(temp)
        return dict_result

    @staticmethod
    def add(model):
        session = DBSession()
        new_model = Scanner(ip=model["ip"],port=model["port"],flag=model["flag"],createdatetime=model["createdatetime"])
        row_affect = session.add(new_model)
        session.commit()
        return row_affect

    @staticmethod
    def get(count=None,conditions=None):
        session = DBSession()
        conditionlist = []
        if conditions:
            for key in list(conditions.keys()):
                if(SqlHelper.params.get(key,None)):
                    conditionlist.append(SqlHelper.params.get(key) == conditions.get(key))
        query = session.query(Scanner).order_by(Scanner.id.desc())
        for c in conditionlist:
            query = query.filter(c)
        if count:
            return query.limit(count).all()
        else:
            return query.all()

    @staticmethod
    def update(model,conditions):
        session = DBSession()
        conditionlist = []
        for key in list(conditions.keys()):
            if(SqlHelper.params.get(key,None)):
                conditionlist.append(SqlHelper.params.get(key) == conditions.get(key))
        query = session.query(Scanner)
        for c in conditionlist:
            query = query.filter(c)
        updatevalue = {}
        for key in list(model.keys()):
            if SqlHelper.params.get(key, None):
                updatevalue[SqlHelper.params.get(key, None)] = model.get(key)
        row_affect = query.update(model)
        session.commit()
        return row_affect

    @staticmethod
    def delete(conditions):
        session = DBSession()
        conditionlist = []
        for key in list(conditions.keys()):
            if(SqlHelper.params.get(key,None)):
                conditionlist.append(SqlHelper.params.get(key) == conditions.get(key))
        query = session.query(Scanner)
        for c in conditionlist:
            query = query.filter(c)
        row_affect = query.delete()
        session.commit()
        return row_affect


if __name__ == '__main__':
    query = SqlHelper.query('select * from Scanner order by createdatetime',3)
    print(query)