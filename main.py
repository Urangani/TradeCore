from mt5linux import MetaTrader5 
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt





def get_symbols(m):
    
    symbols=m.symbols_total()
    
    if symbols>0:
        print("Total symbols =",symbols)
    else:
        print("symbols not found")
 




try:
    # attempt to create an instance
    mt5 = MetaTrader5()

    get_symbols(mt5)
 
    print("MT5 Connected")
# shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
except ConnectionRefusedError as e:
    print(f"Failed to connect: {e}")
    mt5 = None   # ensure mt5 is defined, but unusable
except Exception as e:
    print(f"Unexpected error: {e}")
    mt5 = None
else:
    # only runs if no exception was raised
    if not mt5.initialize():
        print("initialize() failed",mt5.last_error())
        quit()
        mt5.shutdown()
        mt5 = None
finally:
    print("Disconnected Successfully")




