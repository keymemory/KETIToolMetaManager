import sys, os
import pandas as pd
from pymongo import collection
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from KETIToolMetaManager.data_manager.wizMongoDbApi import WizApiMongoMeta

wiz_c = WizApiMongoMeta()

def get_meta_table():
    main_domian_list =  ['air', 'farm', 'factory', 'bio', 'life', 'energy',\
         'weather', 'city', 'traffic', 'culture', 'economy','INNER','OUTDOOR']
    
    db_list = wiz_c.get_database_list()
    exploration_df = pd.DataFrame()

    for db_name in db_list :
        if db_name in main_domian_list: 
            colls = wiz_c.get_collection_list(db_name)
            for coll in colls:
                print(db_name, coll)
                items = wiz_c.get_database_collection_documents(db_name, coll)
                for item in items:
                    try:
                        influx_db_name = item['domain']+"_"+item["sub_domain"]
                        measurement_name = item['table_name']
                        start_time = item['start_time']
                        end_time = item['end_time']
                        frequency = item['frequency']
                        number_of_columns = item['number_of_columns']
                        exploration_df = exploration_df.append([[influx_db_name, measurement_name, start_time, end_time, frequency, number_of_columns]])
                    except KeyError as e:
                        print("KeyError:", e)
                
    exploration_df.columns = ['db_name', 'measurement_name', 'start_time', 'end_time', 'frequency', 'number_of_columns']
    exploration_df.reset_index(drop=True, inplace = True)
    exploration_js = exploration_df.to_json(orient = 'records')
    
    return exploration_js

def get_meta_some_tables(db_ms_names):
    '''{
        db_name : {collection : [ms_names]}
    }'''
    db_list = wiz_c.get_database_list()
    result = {}
    for db in db_ms_names.keys():
        if db not in db_list: 
            continue
        result[db]={}
        for coll in db_ms_names[db].keys():
            result[db][coll]={}
            for ms in db_ms_names[db][coll]:
                data = wiz_c.get_database_collection_document(db, coll, ms)
                data = {"start_time":data["start_time"],"end_time":data["end_time"]}
                result[db][coll][ms]=data
    return result
                

if __name__=="__main__":
    import json
    from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as isk

    #re = get_meta_some_tables({"air":{"indoor_경로당":['ICL1L2000234','ICL1L2000235']}})                    
    #print(re)
    test_exploration_js = get_meta_table()