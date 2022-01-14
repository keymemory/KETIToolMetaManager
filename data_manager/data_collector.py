import sys
import os
sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

from KETIToolMetaManager.manual_data_insert import wiz_mongo_meta_api as wiz
from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as ins
from KETIPreDataIngestion.data_influx import influx_Client
from KETIPrePartialDataPreprocessing import data_preprocessing

# packcage : InputSourceController
# class : Collector
refine_param = {
            "removeDuplication":{"flag":True},
            "staticFrequency":{"flag":True, "frequency":None}
        }
        
outlier_param  = {
    "certainErrorToNaN":{"flag":True},
    "unCertainErrorToNaN":{
        "flag":False,
        "param":{"neighbor":[0.5,0.6]}
    },
    "data_type":"air"
}

imputation_param = {
    "serialImputation":{
        "flag":True,
        "imputation_method":[{"min":0,"max":20,"method":"linear" , "parameter":{}}],
        "totalNonNanRatio":70
    }
}
process_param = {'refine_param':refine_param, 'outlier_param':outlier_param, 'imputation_param':imputation_param}

class Collector(): # GetInputSource / InputSourceCollector
    def __init__(self, database, tablename):
        self.db = database
        self.tablename = tablename
    
    def get_database_meta(self):
        domain = self.db.split("_", maxsplit=1)[0]
        sub_domain = self.db.split("_", maxsplit=1)[1]
        mongodb_con = wiz.WizApiMongoMeta(domain, sub_domain, "db_information")
        base_meta = mongodb_con.get_database_collection_document()
        
        return base_meta
    
    def get_dataframe(self):
        data_nopreprocessing = influx_Client.influxClient(ins.CLUSTDataServer).get_data(self.db, self.tablename)
        # preprocessing
        
        
        partialP = data_preprocessing.packagedPartialProcessing(process_param)
        dataframe = partialP.allPartialProcessing(data_nopreprocessing)["imputed_data"]

        return dataframe