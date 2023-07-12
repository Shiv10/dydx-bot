from func_connections import connect_dydx
from constants import ABORT_ALL_POSITIONS
from func_private import abort_all_positions

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

        