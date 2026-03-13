
from covariance_kalman_predictor import CovarianceKalmanPredictor
from moving_average_filter import MovingAverageFilter
from vvf_rls_prediction import VFF_RLS_Predictor

import yfinance as yf
import threading
import time

live_registry = {}

def start_streaming():
    def message_handler(data):
        symbol = data.get('symbol')
        
        live_registry[symbol] = {
                'price': data.get('price'),
            }
    ws = yf.WebSocket()
    ws.subscribe("AMZN")
    ws.listen(message_handler)

vrls= VFF_RLS_Predictor()

# 5 min 
hist = 5*60
ma = MovingAverageFilter(hist)
ma_pred = MovingAverageFilter(hist)

stream_thread = threading.Thread(target=start_streaming, daemon=True)
stream_thread.start()

current_value = 0
while True:
    old_value = current_value
    try: 
        current_value=live_registry[None]['price']
    except Exception:
        pass

    print("current_value: ", current_value)
    

    vrls.update(u=old_value,y=current_value)
    x_hat=vrls.predict(u=current_value)
    print("predicted_value: ", x_hat)

    ma.insert_new_value(u=current_value)  # moving average of true data
    ma_pred.insert_new_value(u=x_hat)     # moving average of prediction
    print("moving_avg: ", ma.get_average())
    print("moving_avg_pred: ", ma_pred.get_average())
    print("")

    time.sleep(1)
