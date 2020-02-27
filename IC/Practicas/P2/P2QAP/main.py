from AUXX import *
from standard import Standard

st  = Standard()

if __name__ == '__main__':

    time = execute_algorithm( st, 'tai256c.dat' ) 
    print("executing time Of Standard: {:.3f}s\n".format(time))