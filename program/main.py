from func_connections import connect_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message

if __name__ == "__main__":

    send_message("Bot has started")

    # connect to client
    try:
        print("Connecting to client")
        client = connect_dydx()
    except Exception as e:
        print(e)
        print("Error connecting to client")
        send_message("Failed to connect to client")
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
            send_message(f"Failed to close all positions\n{e}")
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
            send_message(f"Failed to fetch market prices\n{e}")
            exit(1)
        

        # store cointegration pairs
        try:
            print("storing cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                send_message("Failed to save cointegrated pairs")
                exit(1)
        except Exception as e:
            print(e)
            print("Error saving cointegrated pairs")
            send_message(f"Failed to save cointegrated pairs\n{e}")
            exit(1)

    while True:
        if MANAGE_EXITS:
            try:
                print("Managing exits..")
                manage_trade_exits(client)
            except Exception as e:
                print(e)
                print("Error managing positions")
                send_message(f"Error managing exits\n{e}")
                exit(1)

        if PLACE_TRADES:
            try:
                print("Findind trading opportunities..")
                open_positions(client)
            except Exception as e:
                print(e.with_traceback())
                print("Error placing trades")
                send_message(f"Error placing trades\n{e}")
                exit(1)