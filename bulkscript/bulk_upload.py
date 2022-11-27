#python file to populate database if not populated
from  mysql.connector import connect,Error
import pandas as pd
import os

database = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('DB_HOST')
# connection à la base de données 

connection = connect(host=host,user=user,password=password,database=database)

## créer la table si pas créée
create_transferts_table = """
    CREATE TABLE IF NOT EXISTS transferts (
    name varchar(50),
    position VARCHAR(50), 
    age INT, 
    teamFrom VARCHAR(50), 
    leagueFrom VARCHAR(50), 
    teamTo VARCHAR(50), 
    leagueTo VARCHAR(50),
    Season VARCHAR(9),
    Market_value INT NULL DEFAULT 0,
    transferFee INT,
    CONSTRAINT unicity UNIQUE (name,age,teamFrom,teamTo,Season)
    )
    """
with connection.cursor() as cursor:
        cursor.execute(create_transferts_table)
        connection.commit()

# check if table is there and propperly populated
populate = False
contenu_table = "select count(*) from transferts"
with connection.cursor() as cursor:
     cursor.execute(contenu_table)
     result = cursor.fetchone()
     if result[0] ==0:
        populate=True

if populate:
    # insert data if not populated 
    insert_transferts = """
    INSERT INTO transferts
    (name,position,age,teamFrom,leagueFrom, teamTo , leagueTo,Season ,Market_value,transferFee)
    VALUES ( %s, %s,%s,%s,%s,%s,%s,%s,%s,%s )
    """ 
    transferts_records = list(pd.read_csv("top250-00-19.csv",sep=",",encoding='utf-8').itertuples(index=False,name=None))
    with connection.cursor() as cursor:
        cursor.executemany(insert_transferts, transferts_records)
        connection.commit()

connection.close()
