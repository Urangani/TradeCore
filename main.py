from mt5linux import MetaTrader5
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

try:
    # attempt to create an instance
    mt5 = MetaTrader5()
except ConnectionRefusedError as e:
    print(f"Failed to connect: {e}")
    mt5 = None   # ensure mt5 is defined, but unusable
except Exception as e:
    print(f"Unexpected error: {e}")
    mt5 = None
else:
    # only runs if no exception was raised
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        mt5 = None

# only proceed if mt5 is valid
if mt5:
    # request 1000 ticks from EURAUD
    euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2020,1,28,13), 1000, mt5.COPY_TICKS_ALL)
    # request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00
    audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,1,27,13), datetime(2020,1,28,13), mt5.COPY_TICKS_ALL)

    # get bars from different symbols
    eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2020,1,28,13), 1000)
    eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
    eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020,1,27,13), datetime(2020,1,28,13))

    # shut down connection
    mt5.shutdown()

    # --- DATA ---
    print('euraud_ticks(', len(euraud_ticks), ')')
    for val in euraud_ticks[:10]: print(val)

    print('audusd_ticks(', len(audusd_ticks), ')')
    for val in audusd_ticks[:10]: print(val)

    print('eurusd_rates(', len(eurusd_rates), ')')
    for val in eurusd_rates[:10]: print(val)

    print('eurgbp_rates(', len(eurgbp_rates), ')')
    for val in eurgbp_rates[:10]: print(val)

    print('eurcad_rates(', len(eurcad_rates), ')')
    for val in eurcad_rates[:10]: print(val)

    # --- PLOT ---
    ticks_frame = pd.DataFrame(euraud_ticks)
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
    plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
    plt.legend(loc='upper left')
    plt.title('EURAUD ticks')
    plt.show()
else:
    print("No valid MT5 connection. Skipping data requests.")
