from func_connections import connect_dydx

if __name__ == "__main__":

    # connect to client
    try:
        client = connect_dydx()
    except Exception as e:
        print(e)
        print("Error connecting to client")
        exit(1)
        