import numpy as np

class MovingAverageFilter:
    def __init__(self, window_size, **kwargs):
        self.window = []
        self.window_size = window_size
        self.weigths = kwargs.get('weigths', np.ones(window_size))

    def insert_new_value(self, u):
        if len(self.window) < self.window_size:
            self.window.append(u)
        else:
            self.window.pop(0)
            self.window.append(u)
    
    def get_average(self):
        return np.sum(self.window)/len(self.window)
    
    def get_weigthed_average(self):
        return np.convolve(self.window,self.weigths)
    

# Simple tests
#measurements = [3,5,6,1,2,2,5,7,9,2,3,5,7,2,1,4,3]
#
#MA = MovingAverageFilter(5)
#s = 0 
#r = 0
#for i in measurements:
#    MA.insert_new_value(i)
#    print(MA.get_average())
#    s = i+s
#    r+=1;
#    a = s/r;
#    print("true avg: ", a)