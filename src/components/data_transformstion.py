'''
the file is responsible for data transformation in ml project

Read train and test CSV files

Separate numerical and categorical features


'''
import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.execption import CustomExecption
from src.logger import logging
from src.utils import save_object


@dataclass# this is a configuration class used to hold data that is stores configuration
class DataTransformationConfig:
    preproecessor_obj_file_path=os.path.join('aritifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_trnsformation_config=DataTransformationConfig()# stores the configuration

    def get_data_transformer_object(self):
        try:
            numerical_feature=['writing_score','reading_score']
            categorical_feature=[
                "gender",
                "race_ethnicity",
                "lunch",
                "test_preparation_course",
                "parental_level_of_education"]
            
            num_pipeline=Pipeline(
                steps=[#trying to clean the null data and standardizing it 
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            ) 
            cat_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("one_hot_encoder", OneHotEncoder()),
        ("scaler", StandardScaler(with_mean=False))
    ]
)
            logging.info("categorical column encoding completed")
            logging.info("numerical column STandarized completed")

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_feature),
                    ("cat_pipeline",cat_pipeline,categorical_feature)
                ]
            )
            return preprocessor

        except Exception as e:
            raise CustomExecption(e,sys)
    
    def initiate_data_tranformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info('Read train and test Data completed')
            logging.info('Obtaining preprocessor object')

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_feature=['writing_score','reading_score']

            input_features_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_features_test_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=train_df[target_column_name]

            logging.info(
                f"applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_features_test_df)

            train_arr=np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]

            test_arr=np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]

            logging.info(f"saved prepossing objects")

            save_object(# this will make a new file in the provided path and save
                    file_path=self.data_trnsformation_config.preproecessor_obj_file_path,
                    obj=preprocessing_obj)
                
            return (
                train_arr,
                test_arr,
                self.data_trnsformation_config.preproecessor_obj_file_path,
            )
        except Exception as e:
            raise CustomExecption(e,sys)