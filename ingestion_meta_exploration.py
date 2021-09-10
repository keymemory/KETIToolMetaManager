import sys, os
import pandas as pd
from pymongo import collection
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from KETIToolMetaManager.mongo_management.mongo_crud import MongoCRUD

def get_meta_table(db_info):
    main_domian_list =  ['air', 'farm', 'factory', 'bio', 'life', 'energy',\
         'weather', 'city', 'traffic', 'culture', 'economy']
    mydb = MongoCRUD(db_info)
    db_list = mydb.getDBList()
    print(db_list)
    exploration_df = pd.DataFrame()

    for db_name in db_list :
        if db_name in main_domian_list:
            mydb.switchDB(db_name)
            colls = mydb.getCollList()
            print(colls)
            for coll in colls:
                items = mydb.getManyData(coll)
                for item in items:
                    influx_db_name = item['domain']+"_"+item["sub_domain"]
                    measurement_name = item['table_name']
                    start_time = item['start_time']
                    end_time = item['end_time']
                    frequency = item['frequency']
                    number_of_columns = item['number_of_columns']
                    
                    exploration_df = exploration_df.append([[influx_db_name, measurement_name, start_time, end_time, frequency, number_of_columns]])
    
    exploration_df.columns = ['db_name', 'measurement_name', 'start_time', 'end_time', 'frequency', 'number_of_columns']
    exploration_df.reset_index(drop=True, inplace = True)
    exploration_js = exploration_df.to_json(orient = 'records')
    
    return exploration_js

def get_meta_some_tables(db_info,db_ms_names):
    '''{
        db_name : {collection : [ms_names]}
    }'''
    mydb = MongoCRUD(db_info)
    db_list = mydb.getDBList()
    result = {}
    for db in db_ms_names.keys():
        if db not in db_list:
            continue
        mydb.switchDB(db)
        result[db]={}
        for coll in db_ms_names[db].keys():
            result[db][coll]={}
            for ms in db_ms_names[db][coll]:
                data = mydb.getOneData(coll,{"table_name":ms})
                data = {"start_time":data["start_time"],"end_time":data["end_time"]}
                result[db][coll][ms]=data
    return result
                

if __name__=="__main__":
    import json
    # with open('KETIPreDataIngestion/KETI_setting/config.json', 'r') as f:
    #     config = json.load(f)
    from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as isk
    
    # exploration_df = get_meta_table(isk.DB_INFO)
    # print(exploration_df)
    #print(exploration_df.columns)
    get_meta_some_tables(isk.DB_INFO,{"air":{"indoor_경로당":['ICL1L2000234','ICL1L2000235']}})