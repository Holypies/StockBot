import yfinance as yf

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



# Simple test
#
#stream_thread = threading.Thread(target=start_streaming, daemon=True)
#stream_thread.start()
#
#print("Waiting for data to hit the dictionary...")
#time.sleep(5)
#
#while True:
#    print(f"\nLatest Registry: ", live_registry)
#    time.sleep(1)