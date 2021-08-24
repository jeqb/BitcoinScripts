import os
from datetime import datetime
from decimal import *
import requests
from dotenv import load_dotenv; load_dotenv()


"""
Keep a .env file with two environment variables:
    PRINCIPAL=5000
    MY_BITCOIN_AMT=0.0145684
Replace with your own values.
"""


# GLOBALS
PRINCIPAL = float(os.getenv('PRINCIPAL'))
MY_BITCOIN_AMT = float(os.getenv('MY_BITCOIN_AMT'))


def get_BTC_price() -> float:
    """ Get the price of Bitcoin in usd """

    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')

    data = response.json()

    price_string = data['bpi']['USD']['rate']

    price_float = float(price_string.replace(',', ''))

    return round(price_float, 2)


def get_precision(decimal: float) -> int:
    """ returns how many decimal points a float has """

    string_value = str(decimal)

    precision = string_value[::-1].find('.')

    return precision


def validate_btc_value(btc_amount: float):
    """ for the purpose of the script, make sure that the bitcoin value is a float
    and does not have more than 8 decimal places """

    if type(btc_amount) != float:
        raise Exception("MY_BITCOIN_AMT must be a float")
    if get_precision(btc_amount) > 8:
        raise Exception("MY_BITCOIN_AMT cannot be more than 8 decimal places")


def get_btc_value(btc: float) -> float:
    """ given a sum of BTC, return its value in USD """
    
    validate_btc_value(btc)

    price = get_BTC_price() * btc
    
    return round(price, 2)


def calculate_future_valute(btc: float, future_price: float) -> float:
    """ Calculate the future price of bitcoin given some price from the future.
    kind of pointless. """
    
    return round(btc * future_price, 2)


def usd_to_btc(usd: float) -> float:
    """ How much BTC can I get for this USD right now? """
    
    usd = round(usd, 2)

    btc_value = get_BTC_price()

    raw_value = usd / btc_value

    rounded_value = round(raw_value, 8)
    # removes the scientific notation
    decimal_value = Decimal(rounded_value)

    return round(float(decimal_value), 8)


def get_break_even_price(principal: float, current_btc_holding: float) -> float:
    """ Given your principal investment, and the amount of BTC you have from that,
    it returns the price BTC needs to hit for you to break even on your investment. """
    
    return round( ( principal / current_btc_holding ), 2)


def main():
    """ The script does this """

    validate_btc_value(MY_BITCOIN_AMT)
    btc_in_usd = get_btc_value(MY_BITCOIN_AMT)

    hundred_k = calculate_future_valute(MY_BITCOIN_AMT, 100000)
    two_hundred_k = calculate_future_valute(MY_BITCOIN_AMT, 200000)
    three_hundred_k = calculate_future_valute(MY_BITCOIN_AMT, 300000)
    four_hundred_k = calculate_future_valute(MY_BITCOIN_AMT, 400000)
    five_hundred_k = calculate_future_valute(MY_BITCOIN_AMT, 500000)
    one_million = calculate_future_valute(MY_BITCOIN_AMT, 1000000)


    data = [
        datetime.now(),
        get_BTC_price(),
        MY_BITCOIN_AMT,
        btc_in_usd,
        PRINCIPAL,
        ( round(btc_in_usd - PRINCIPAL, 2) ),
        get_break_even_price(PRINCIPAL, MY_BITCOIN_AMT),
        hundred_k,
        two_hundred_k,
        three_hundred_k,
        four_hundred_k,
        five_hundred_k,
        one_million
    ]

    message = """
    As of {0},
    The price of Bitcoin is $ {1}
    You have {2} BTC.
    The value of your Bitcoin in usd is $ {3}
    Your total dollars invested are: $ {4}
    Your current profit is {5}
    You will break even at a BTC price of: {6}
    At $ 100K, it will be worth $ {7}
    At $ 200K, it will be worth $ {8}
    At $ 300K, it will be worth $ {9}
    At $ 400K, it will be worth $ {10}
    At $ 500K, it will be worth $ {11}
    at $ 1Mil, it will be worth $ {12}
    """.format(*data)

    print(message)


if __name__ == '__main__':
    main()