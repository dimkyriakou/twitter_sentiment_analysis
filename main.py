import mysql.connector
from credentials import *
from twstreamer import *
from common import db_name, words


mydb = mysql.connector.connect(
    host      = "localhost"  ,
    user      = "root"       ,
    passwd    = ""           ,
    database  = db_name
)

if mydb.is_connected():
    print("Connected Successfully!")
    cur = mydb.cursor()

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth)

myStreamListener = MyStreamListener()
myStream = tw.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(languages=["en"], track=words)

mydb.close()