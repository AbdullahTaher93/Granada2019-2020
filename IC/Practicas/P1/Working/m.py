import numpy as np
import matplotlib
import matplotlib.pyplot as ptl
import os
import urllib.request
def load_file():
    print("1")
    def download(filename,source="http://yann.lecun.com/exdb/mnist/"):
        print("downloding",filename)
        import urllib
        urllib.request.urlretrieve(source+filename,filename)

    import gzip
    def load_minst_images(filename):
        if not (os.path.exists(filename)):
            download(filename)
        

        with gzip.open(filename,"rb") as f:
            data=np.frombuffer(f.read(),np.uint8,offset=16)
            data=data.reshape(-1,1,28,28)

            return data/np.float32(255)
            

    def load_minst_lables(filename):
        print("1")
        if not (os.path.exists(filename)):
            download(filename)

        with gzip.open(filename,"rb") as f:
            data=np.frombuffer(f.read(),np.uint8,offset=8)
            

            return data

    x_train= load_minst_images("train-images-idx3-ubyte.gz")
    y_train= load_minst_lables("train-labels-idx1-ubyte.gz")

    x_test= load_minst_images("t10k-images-idx3-ubyte.gz")
    y_test= load_minst_lables("t10k-labels-idx1-ubyte.gz")

    matplotlib.use("TkAgg")
    ptl.show(ptl.imshow(x_train[2][0]))

load_file()
            