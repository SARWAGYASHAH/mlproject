# common functionalities fro the entire project
import os
import pandas as pd
import numpy as np
import sys

import dill 
from src.execption import CustomExecption

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb')as file_obj:
            dill.dump(obj,file_obj)

    except Exception as eL:
        raise CustomExecption(eL,sys) 