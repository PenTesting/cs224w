# CS224W Project
# David Golub and Liam Kelly
# Stanford University

import json
import snap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

def read_json_file(filename="price_data_raw.json"):
    read_file = open(filename, "r")
    data = json.load(read_file)
    read_file.close()
    return data

def write_json_file(data, filename="price_data.json"):
    write_file = open(filename, "w")
    json.dump(data, write_file, indent=4)
    write_file.close()

def get_sorted_prices(price_dict):
    dates_sorted = [k for v, k in sorted((datetime.strptime(k, '%Y-%m-%d'), k) for k, v in price_dict.iteritems())]
    data_sorted = []
    for i in range(len(dates_sorted)):
        data_sorted.append(price_dict[dates_sorted[i]])
    return dates_sorted, data_sorted

def plot_price_data(price_data, savefile=None, show=True):
    price_dict = price_data['bpi']
    dates, data = get_sorted_prices(price_dict)

    # Need datetimes so that matplotlib can make it pretty
    datetime_objs = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    plt.plot(datetime_objs,data)

    # Use the autofmt so it will pick numbers properly
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%m/%Y')
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title('Bitcoin Price from 11/2016 to 11/2018')

    if savefile:
        plt.savefig(savefile)
    if show:
        plt.show()

def print_summary_price_stats(price_data):
    _, prices = get_sorted_prices(price_data['bpi'])
    mean = np.mean(prices)
    median = np.median(prices)
    std = np.std(prices)
    max_price = np.amax(prices)
    min_price = np.amin(prices)

    print 'mean: %f' % mean
    print 'median: %f' % median
    print 'std_dev: %f' % std
    print 'max_price: %f' % max_price
    print 'min_price: %f' % min_price

def combine_datasets(price_data, results):
    exchanges = list()
    amount_dict = dict()
    prices = list()
    first_pass = True
    for exch, dataset in results.items():
        exchanges.append(exch)
        inds = list()
        amounts = list()
        for datapoint in dataset:
            inds.append(pd.Timestamp(datapoint[0][:10]))
            amounts.append(datapoint[1])
            if first_pass:
                prices.append(price_data['bpi'][datapoint[0][:10]])
        amount_dict[exch] = amounts
        first_pass = False

    amount_dict['price'] = prices
    df = pd.DataFrame.from_dict(amount_dict)
    df['date'] = inds
    df.set_index('date')

    return df, exchanges

def save_dataframe(df, filename):
    df.to_csv(filename)

def load_dataframe(filename):
    df = pd.read_csv(filename, index_col=0)
    return df

def plot_data(df, exchanges, savefile=None, show=True):
    df1 = df.set_index(pd.DatetimeIndex(df['date']))
    ax1 = df1[exchanges].plot()
    plt.legend(loc=2, prop={'size': 6})

    ax2 = ax1.twinx()
    df1['price'].plot(secondary_y=True, linewidth=1.5, style=['r--'])
    plt.legend(loc=1, prop={'size': 6})

    plt.title('Bitcoin assets over time from 2017-01-01 to 2018-11-26')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Amount in assets')
    ax2.set_ylabel('Bitcoin Price in USD')

    if savefile:
        plt.savefig(savefile)
    if show:
        plt.show()

if __name__ == "__main__":
    price_data = read_json_file('price_data_updated_raw.json')
    # write_json_file(price_data)
    addresses = read_json_file('addresses_raw.json')
    # write_json_file(addresses, 'addresses.json')
    results = read_json_file('results_raw.json')
    # write_json_file(results, 'results.json')
    
    # plot_price_data(price_data, savefile='prices.png', show=False)
    # print_summary_price_stats(price_data)

    df, exchanges = combine_datasets(price_data, results)
    save_dataframe(df, 'combined_data.csv')
    df = load_dataframe('combined_data.csv')
    try:
        exchanges
    except NameError:
        exchanges = addresses.keys() 
    plot_data(df, exchanges, savefile='price_asset.png', show=True)
