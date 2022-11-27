from typing import Union,List
from fastapi import Depends, FastAPI, HTTPException, status,Query ,Body
from pydantic import BaseModel
import os
from  mysql.connector import connect ,Error


database = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('DB_HOST')

def make_query(data):
    if   data['minage'] is None and   data['maxage'] is None:
      age_query =""
    elif   data['minage']!=0 and   data['maxage'] is None:
      age_query = "age >= " + str(int(  data['minage'])) 
    elif   data['minage'] is None and   data['maxage']!=0:
      age_query = "age <= " + str(int(  data['maxage'])) 
    else: 
      age_query = "age between " + str(int(  data['minage'])) + " and " + str(int(  data['maxage']))

    if data['mintransfertvalue'] is None and data['maxtransfertvalue'] is None :
      market_value =""
    elif data['mintransfertvalue'] !=0 and data['maxtransfertvalue'] is None :
      market_value = "Market_value >= " + str(int(data['mintransfertvalue'])) 
    elif data['mintransfertvalue'] is None and data['maxtransfertvalue'] !=0:
      market_value = "Market_value <= " + str(int(data['maxtransfertvalue'])) 
    else: 
      market_value = "Market_value between " + str(int(data['mintransfertvalue'])) + " and " + str(int(data['maxtransfertvalue']))

    if data['mintransfertfee'] is None and data['maxtransfertfee'] is None:
      transfert_query =""
    elif data['mintransfertfee']!=0 and data['maxtransfertfee'] is None:
          transfert_query = "and transferfee >= " + str(int(data['mintransfertfee'])) 
    elif data['mintransfertfee'] is None and data['maxtransfertfee']!=0:
          transfert_query = "and transferfee <= " + str(int(data['maxtransfertfee'])) 
    else: 
       transfert_query = "transferfee between " + str(int(data['mintransfertfee'])) + " and " + str(int(data['maxtransfertfee']))
       
    name_query = "" if data['name'] is None  else "name = '"+data['name']+"'"
    dep_team = "" if data['fromTeam'] is None   else "teamFrom = '"+ data['fromTeam'] +"'"
    arr_team = "" if data['toTeam'] is None   else "teamTo = '"+ data['toTeam'] +"'"
    dep_league = "" if data['fromleague'] is None  else "leagueFrom = '"+ data['fromleague'] +"'"
    arr_league = "" if data['toleague']  is None  else "leagueTo = '"+ data['toleague'] +"'"
    transfert_year = "" if data['transfertYear'] is None  else "Season like '%"+ data['transfertYear'] +"%' "

    query_items =  [name_query, dep_team , arr_team , dep_league ,arr_league, transfert_year , transfert_query , market_value , age_query]
    validated_items = [x for x in query_items if x !='']


    return "select * from transferts  where " + ' and '.join(validated_items)

class transfert(BaseModel):
  name : str
  position : str
  age : int
  teamFrom :str
  leagueFrom :str
  teamTo : str
  leagueTo :str 
  Season :str
  Market_Value: int
  transferFee: int

class result(BaseModel):
    data : List[transfert]


app = FastAPI()


@app.post("/addTransfert")
async def post_transfert(Transfert : transfert):
  t_dict = Transfert.dict()
  connection = connect(host=host,user=user,password=password,database=database)

  if not Transfert.transferFee :
      t_dict['transferFee'] = 0
    #insert_one_query
  insert_transferts = """INSERT INTO transferts (name,position,age,teamFrom,leagueFrom, teamTo , leagueTo,Season ,Market_value,transferFee) 
  VALUES ( "%s", %s,"%s","%s","%s","%s","%s","%s",%s,%s ) """  %  tuple(t_dict.values()) 
  try : 
    with connection.cursor() as cursor:
        cursor.execute(insert_transferts)
        connection.commit()
    return True
  except Error as e:
    return e

@app.get("/get")
async def get_data(
    name: Union[str, None] = Query(default=None,max_length=50),
    minage: Union[int, None] = Query(default=None),
    maxage: Union[int, None] = Query(default=None),
    fromTeam: Union[str, None] = Query(default=None,max_length=50),
    toTeam: Union[str, None] = Query(default=None,max_length=50),
    fromleague : Union[str, None] = Query(default=None,max_length=50),
    toleague : Union[str, None] = Query(default=None,max_length=50),
    transfertYear :Union[str, None] = Query(default=None,regex="^20\d{2}$"),
    mintransfertfee :Union[int, None] = Query(default=None),
    maxtransfertfee :Union[int, None] = Query(default=None),
    mintransfertvalue :Union[int, None] = Query(default=None),
    maxtransfertvalue :Union[int, None] = Query(default=None)
    ):
  data = {"name" : name,
    "minage" : minage,
    "maxage" : maxage, 
    "fromTeam" : fromTeam,
    "toTeam" : toTeam,
    "fromleague" : fromleague,
    "toleague" : toleague,
    "transfertYear" : transfertYear,
    "mintransfertfee" :  mintransfertfee,
    "maxtransfertfee" : maxtransfertfee,
    "mintransfertvalue" : mintransfertvalue,
    "maxtransfertvalue" : maxtransfertvalue}
  query = make_query(data)
  connection = connect(host=host,user='tiboo91',password='projet3-de',database='p3db')
  with connection.cursor(buffered=True) as cursor:
        cursor.execute(query)
        q_result = cursor.fetchall()
        connection.close()
  return {"data" : q_result}
