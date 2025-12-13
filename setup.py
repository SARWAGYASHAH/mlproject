from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''this function will return a list of requirements'''
    requirements=[]
    with open(file_path) as fileojb:
        requirements=fileojb.readlines() 
        requirements=[req.replace('\n',"") for req in requirements]

        if '-e .' in requirements:# this is in the requirements.txt to automatically track the packages
            requirements.remove('-e .')
    return requirements ## a list would be returned containing all the packages required

setup(### this function usese the setup tool to describe your project as a python package
    # META DATA KIND OF THING
    name='mlproject',
    version='0.0.1',
    author='Sarwagya Shah',
    author_email='sarwagyashahonline@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)