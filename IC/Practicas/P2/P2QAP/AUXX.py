##clean 
import os
import time

from Gen_Algorithm import GAs
from standard import Standard

DATA_DIR = os.path.join('src', 'data', 'qap')


def get_data_files( dir ):
    
    def exists(file):
        return os.path.isfile(os.path.join(dir, file))

    return [file for file in os.listdir(dir) if exists(file)]


def execute_algorithm( algorithm, datafile ):
    
    if issubclass(type(algorithm), GAs):
        start_time = time.time()
        algorithm.execute( datafile )
        return time.time() - start_time

    


def check_files( ):

    n_assertion_err = 0
    for file in get_data_files( DATA_DIR ):
        try:
            execute_algorithm( Standard(), file )
        except AssertionError:
            n_assertion_err += 1
    print(n_assertion_err)
