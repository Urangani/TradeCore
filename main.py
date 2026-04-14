from mt5linux import MetaTrader5


try:
    mt5 = MetaTrader5()
    mt5.initialize()
    mt5.terminal_info()
    mt5.shutdown()

except(ConnectionError):
    print("Connection Failed")



