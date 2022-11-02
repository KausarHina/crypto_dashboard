import requests
import pandas as pd
import datetime
import json
import numpy as np


#################################################################
#
#
#################################################################
def get_market_chart(coid_id, days):
        
    vs_currency='usd'
    
    if days == '1d' :
        num_of_days=1
    elif days == '7d':
        num_of_days=7
    elif days == '30d':    
        num_of_days=30
    elif days == '90d':    
        num_of_days=90 
    elif days == '1y':    
        num_of_days=365 
    else :   
        num_of_days='max'
        
    url = f"https://api.coingecko.com/api/v3/coins/{coid_id}/market_chart"
    payload={'vs_currency' : vs_currency, 'days' : num_of_days}
    
    response = requests.get(url, params=payload)
    data = response.json()
    
    timestamp_list = []
    price_list = []
    
    for row in data['prices'] :
        timestamp_list.append(datetime.datetime.fromtimestamp(row[0]/1000))
        price_list.append(row[1])
        
    raw_data = {
        'timestamp': timestamp_list,
        'price' : price_list
    }  
    
    df = pd.DataFrame(raw_data, columns=['timestamp','price']) 
    df = df.set_index('timestamp')
    
    title=f"{days}"
    return df, title


#################################################################
#
#
#################################################################
def get_coin_price(coin_id) :
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"
  
    response = requests.get(url)
    data = response.json()
    
    coin_price_df = pd.DataFrame(data)
    coin_price_df = coin_price_df.T   
    pd.options.display.float_format = '{:.2f}'.format
    
    coin_price_df = coin_price_df.reset_index()
    
    coin_price_df = coin_price_df.rename(columns = {'index' : 'id'})
    coin_price_df = coin_price_df.set_index('id')
    
    return coin_price_df

#################################################################
#
#
#################################################################
def get_coin_info(coin_id) :
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    
    coin_all_info_df = pd.DataFrame([data], columns=['id', 'symbol', 'name', 'asset_platform_id', 'platforms',
       'detail_platforms', 'block_time_in_minutes', 'hashing_algorithm',
       'categories', 'public_notice', 'additional_notices', 'description',
       'links', 'image', 'country_origin', 'genesis_date',
       'sentiment_votes_up_percentage', 'sentiment_votes_down_percentage',
       'market_cap_rank', 'coingecko_rank', 'coingecko_score',
       'developer_score', 'community_score', 'liquidity_score',
       'public_interest_score', 'public_interest_stats', 'status_updates',
       'last_updated'])
    
    coin_info_df = coin_all_info_df.loc[:,['id', 'symbol', 'name', 'market_cap_rank' ]]

    coin_info_df = coin_info_df.set_index('id')
    return coin_info_df

#################################################################
#
#
#################################################################
def get_combined_coin_info(coin_id) :
    
    coin_info_df = get_coin_info(coin_id)
    
    coin_price_df = get_coin_price(coin_id)
    
    combined_info_df = pd.merge(coin_info_df, coin_price_df, on='id')
    
    return combined_info_df

#################################################################
#
#
#################################################################