import mysql.connector
from common import db_name

mydb = mysql.connector.connect(
    host      = "localhost"  ,
    user      = "root"       ,
    passwd    = ""           ,
    database  = db_name
)

if mydb.is_connected():
    print("Connected Successfully!")
    cur = mydb.cursor()

create_table = "CREATE TABLE TWEETS (   " \
               "             TW_ID            varchar(255)                          NOT NULL        , " \
               "             AUTHOR           varchar(255)                          NOT NULL        , " \
               "             AUTHOR_TWS       int                                   DEFAULT NULL    , " \
               "             AUTHOR_FLWRS     int                                   DEFAULT NULL    , " \
               "             DT_POSTED        datetime                              DEFAULT NULL    , " \
               "             TEXT             varchar(1000)                         NOT NULL        , " \
               "             NO_RETWS         int                                   DEFAULT NULL    , " \
               "             LONGITUDE        double                                DEFAULT NULL    , " \
               "             LATITUDE         double                                DEFAULT NULL    , " \
               "             HASHTAGS         varchar(255)                          DEFAULT NULL    , " \
               "             POLARITY         decimal(5,2)                          NOT NULL        , " \
               "             SUBJECTIVITY     decimal(5,2)                          NOT NULL        , " \
               "             SENTIMENT        set('POSITIVE','NEUTRAL','NEGATIVE')  NOT NULL        , " \
               "             SRCH_WRD         varchar(11)                           NOT NULL        , " \
               "  PRIMARY KEY ({}))                                                                 ;".format('TW_ID')
cur.execute(create_table)
mydb.commit()
cur.close()

mydb.close()