import numpy as np
class CovarianceKalmanPredictor:
    def __init__(self, **kwargs):
        self.lamda = kwargs.get('lamda', 0.99)
        self.K = kwargs.get('K', 1)
        self.x_pred = kwargs.get('x_pred', 1)
         
    def update(self,u,y):
        g_num = (1/np.sqrt(self.lamda)*self.K*u)
        g_den = u*self.K*u + 1
        g = g_num/g_den
        alpha= y-(u*self.x_pred)
        self.x_pred=1/np.sqrt(self.lamda)*self.x_pred+(g*alpha)
        self.K = (1/self.lamda*self.K) - (1/np.sqrt(self.lamda))*g*u*self.K
        
    
    def predict(self,u):
        y_prediction = u*self.x_pred
        return y_prediction




# Simple test
#measurements = [2.5, 2.8, 3.1, 2.7, 3.2]
#
#kf = CovarianceKalmanPredictor(lamda=0.9) 
#
#for i in range(len(measurements) - 1):
#    u = measurements[i]          
#    y_true = measurements[i+1]
#
#    y_prediction = kf.predict(u)
#    
#    kf.update(u, y_true)
#
#    print(f"Step {i+1}:")
#    print(f"  Input (u):      {u}")
#    print(f"  Predicted (y):  {y_prediction:.2f}")
#    print(f"  Actual (y):     {y_true}")
#    print(f"  Error:          {abs(y_true - y_prediction):.2f}\n")