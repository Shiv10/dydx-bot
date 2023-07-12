from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config

# Select Mode
MODE = "DEVELOPMENT"

# Close all open positions and orders
ABORT_ALL_POSITIONS = True

# Find co-integrated pairs
FIND_COINTEGRATED = True

# Place trades
PLACE_TRADES = True

# Resolution
RESOLUTION = "1HOUR"

# Stats window
WINDOW = 21

# Thresholds - Opening
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 50
USD_MIN_COLLATERAL = 1880

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True

# Ethereum address
ETHEREUM_ADDRESS = "0xfB24B53C5517566A6a109E4A21AD2eE4D5cd23c7"

# ENV vars
ETHEREUM_PRIVATE_KEY = config("ETHEREUM_PRIVATE_KEY")
STARK_PRIVATE_KEY = config('STARK_PRIVATE_KEY')
DYDX_API_KEY = config("DYDX_API_KEY")
DYDX_API_SECRET= config("DYDX_API_SECRET")
DYDX_API_PASSPHRASE = config("DYDX_API_PASSPHRASE")
HTTP_PROVIDER = config("HTTP_PROVIDER")

# HOST - Export
HOST = API_HOST_MAINNET if MODE=="PRODUCTION" else API_HOST_GOERLI

# remember to add production keys on deployment