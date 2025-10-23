import json 
import yaml 
import pandas as pd 
import utils.printer as pr 
from utils.exceptions import ConfigException 
from os import walk, listdir, getenv as env 
from os.path import join 
from pathlib import  Path 
from io import StringIO

LOCAL_PATHS = {
    'mappings': 'local/mappings/',
    'inputs': 'local/inputs/',
    'errors': 'local/outputs/errors/',
    'outputs': 'local/outputs/',
    'secrets': 'local/credentials.json',
}


class Singleton(type): 
    """ Singleton Class """
    _instances = { }
    def __call__(self, *args, **kwargs)
        if self not in self._instances: 
            instance = super().__call__(*args, **kwargs)
            self._instances[self] = instance 

        return self._instances[self]
    
class Canonical(metaclass=Singleton):
    def __init__(self) -> None:
        self.PATHS = self._get_paths()
        self.SECRETS = self._get_secrets()
        self. = self._get_()
        self. = self._get_()