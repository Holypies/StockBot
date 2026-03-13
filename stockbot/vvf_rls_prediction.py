import numpy as np

class VFF_RLS_Predictor:
    def __init__(self, lamda_max=0.99, lamda_min=0.85, gamma=0.01):
        self.lamda_max = lamda_max
        self.lamda_min = lamda_min
        self.lamda = lamda_max  
        
        self.gamma = gamma 
        
        self.K = 1.0
        self.x_pred = 1.0 
         
    def update(self, u, y):
        # Calculate prior error
        alpha = y - (u * self.x_pred)
        
        # square it
        error_sq = alpha ** 2 
        
        # Calculate the new lambda
        self.lamda = self.lamda_min + (self.lamda_max - self.lamda_min) * np.exp(-self.gamma * error_sq)

        # Calculate Gain
        g_num = (1 / np.sqrt(self.lamda)) * self.K * u
        g_den = (u * self.K * u) + 1
        g = g_num / g_den
        
        # Update the Prediction Gain
        self.x_pred = self.x_pred + (g * alpha)
        
        # Update K
        self.K = (1 / self.lamda) * self.K - (1 / np.sqrt(self.lamda)) * g * u * self.K
        
    def predict(self, u):
        return u * self.x_pred
    
    def calculate_optimal_gamma(self, historical_data:list, sigma_multiplier:float=3.0):
        # Convert to numpy array for easy math
        data = np.array(historical_data)
        
        # Calculate step-to-step differences
        differences = np.diff(data)
        
        # Calculate the standard deviation (sigma) of these differences
        sigma = np.std(differences)
        
        # Safety check: if the data never moves, we can't calculate a shock!
        if sigma == 0:
            print("Warning: Data has zero variance. Returning a default gamma.")
            return 0.01 
            
        # Define the shock threshold
        alpha_shock = sigma_multiplier * sigma
        
        # Calculate gamma
        gamma = 3.0 / (alpha_shock ** 2)
        
        return gamma    