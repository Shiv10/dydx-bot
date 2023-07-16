from func_connections import connect_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions

if __name__ == "__main__":

    # connect to client
    try:
        print("Connecting to client")
        client = connect_dydx()
    except Exception as e:
        print(e)
        print("Error connecting to client")
        exit(1)

    # abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions")
            close_orders = abort_all_positions(client)
            print('All positions closed')
        except Exception as e:
            print(e)
            print("Error closing all positions")
            exit(1)

    # find cointegrated pairs
    if FIND_COINTEGRATED:

        # construct masket prices
        try:
            print("fetching market prices, please allow 3 mins")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print(e)
            print("error fetching market prices")
            exit(1)
        

        # store cointegration pairs
        try:
            print("storing cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print(e)
            print("Error saving cointegrated pairs")
            exit(1)


    if PLACE_TRADES:
        try:
            print("Findind trading opportunities..")
            open_positions(client)
        except Exception as e:
            print(e)
            print("Error placing trades")
            exit(1)