from constants import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_z_score
from func_private import is_open_positions
from func_bot_agent import BotAgent
import pandas as pd
import json
from pprint import pprint

# open positions
def open_positions(client):

    """
        Manage finding tiggers for trade entry
        Store trades for managing later on exit function
    """

    # load cointegrated pairs
    df = pd.read_csv("cointegrated_pairs.csv")
    
    # get markets for reference
    markets = client.public.get_markets().data

    # init containter for BotAgent results
    bot_agents = []

    # find zScrore triggers
    for index, row in df.iterrows():

        # extract variables
        base_market = row["base_market"]
        quote_market = row["quote_market"]
        hedge_ratio = row["hedge_ratio"]
        half_life = row["half_life"]
        
        # get prcies
        series_1 = get_candles_recent(client, base_market)
        series_2 = get_candles_recent(client, quote_market)

        # get zScore
        if len(series_1) > 0 and len(series_1)==len(series_2):
            spread = series_1 - (hedge_ratio * series_2)
            z_score = calculate_z_score(spread).values.tolist()[-1]
            
            # establish if potential trade
            if abs(z_score) >= ZSCORE_THRESH:

                # enusre like for like not already open (diversify trading)
                is_base_open = is_open_positions(client, base_market)
                is_quote_open = is_open_positions(client, quote_market)

                # place trades
                if not is_base_open and not is_quote_open:

                    # determine side
                    base_side = "BUY" if z_score < 0 else "SELL"
                    quote_side = "BUY" if z_score > 0 else "SELL"

                    # get acceptable price in string format with correct number of decimals
                    base_price = series_1[-1]
                    quote_price = series_2[-1]
                    accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
                    accept_quote_price = float(quote_price) * 1.01 if z_score > 0 else float(quote_price) * 0.99
                    failsafe_base_price = float(base_price) * 0.05 if z_score < 0 else float(quote_price) * 1.7
                    base_tick_size = markets["markets"][base_market]["tickSize"]
                    quote_tick_size = markets["markets"][quote_market]["tickSize"]

                    # format prices 
                    accept_base_price = format_number(accept_base_price, base_tick_size)
                    accept_quote_price = format_number(accept_quote_price, quote_tick_size)
                    accept_failsafe_base_price = format_number(failsafe_base_price, base_tick_size)\
                    
                    # get size
                    base_quantity = 1 / base_price * USD_PER_TRADE
                    quote_quantity = 1 / quote_price * USD_PER_TRADE
                    base_step_size = markets["markets"][base_market]["stepSize"]
                    quote_step_size = markets["markets"][quote_market]["stepSize"]

                    # format size
                    base_size = format_number(base_quantity, base_step_size)
                    quote_size = format_number(quote_quantity, quote_step_size)

                    # ensure size
                    base_min_order_size = markets["markets"][base_market]["minOrderSize"]
                    quote_min_order_size = markets["markets"][quote_market]["minOrderSize"]
                    check_base = float(base_quantity) > float(base_min_order_size)
                    check_quote = float(quote_quantity) > float(quote_min_order_size)

                    if check_base and check_quote:

                        # check account balance
                        account = client.private.get_account()
                        free_collateral = float(account.data["account"]["freeCollateral"])
                        print(f"Balance: {free_collateral} and minimum at {USD_MIN_COLLATERAL}")

                        # guard ensure collateral
                        if free_collateral < USD_MIN_COLLATERAL:
                            break

                        # create Bot Agent
                        bot_agent = BotAgent(
                            client,
                            market_1=base_market,
                            market_2=quote_market,
                            base_side=base_side,
                            base_size=base_size,
                            base_price=accept_base_price,
                            quote_side=quote_side,
                            quote_size=quote_size,
                            quote_price=accept_quote_price,
                            accept_failsafe_base_price=accept_failsafe_base_price,
                            z_score=z_score,
                            half_life=half_life,
                            hedge_ratio=hedge_ratio
                        )

                        # call open trades
                        bot_open_dict = bot_agent.open_trades()

                        # handle success in opening trades
                        if bot_open_dict["pair_status"] == "LIVE":

                            bot_agents.append(bot_open_dict)
                            del bot_open_dict

                            # confirm live status
                            print("trade status: live")
                            print("---")
    
    # save agents
    print(f"Success: {len(bot_agents)} New Pairs LIVE")
    if len(bot_agents) > 0:
        with open("bot_agents_json", "w") as f:
            json.dump(bot_agents, f)
