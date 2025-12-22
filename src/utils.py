# common functionalities fro the entire project
import os
import pickle
import pandas as pd
import numpy as np
import sys
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import dill 
from src.execption import CustomExecption
from src.logger import logging

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb')as file_obj:
            dill.dump(obj,file_obj)

    except Exception as eL:
        raise CustomExecption(eL,sys) 
def evaluate_models(X_train, y_train, X_test, y_test, models, param=None):
    try:
        report = {}

        for model_name, model in models.items():
            logging.info(f"Training model: {model_name}")

            # SAFE handling when param is None
            params = param[model_name] if param and model_name in param else {}

            gs = GridSearchCV(
                estimator=model,
                param_grid=params,
                cv=3,
                n_jobs=-1
            )

            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

            logging.info(f"{model_name} R2 score: {test_model_score}")

        return report

    except Exception as e:
        raise CustomExecption(e, sys)
    
def load_object(file_path):
    """
    Loads a pickled object from disk.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomExecption(e, sys)
