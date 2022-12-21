import sqlalchemy as db
import os

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

engine = db.create_engine('mysql+mysqldb://{db_user}:{db_pass}@127.0.0.1/dbname', echo=True)
conn = engine.connect()

selectQuery = db.select('dbtable')
print(selectQuery)