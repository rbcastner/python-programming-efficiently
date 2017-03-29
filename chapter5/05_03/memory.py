
import numpy as np

@profile
def allocate():
    vector_list = [float(i) for i in range(100000)]
    vector_np = np.arange(0,100000,dtype='d')
    
allocate()