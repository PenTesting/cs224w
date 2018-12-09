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

def read_json_file(filename="data/price_data_raw.json"):
    read_file = open(filename, "r")
    data = json.load(read_file)
    read_file.close()
    return data

def write_json_file(data, filename="output/price_data.json"):
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
    plt.clf()

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

    return df, exchanges

def save_dataframe(df, filename):
    df.to_csv(filename)

def load_dataframe(filename):
    df = pd.read_csv(filename, index_col=0)
    return df

def plot_data(df, exchanges, savefile=None, show=True):
    ax1 = df[exchanges].plot()
    plt.legend(loc=2, prop={'size': 6})

    ax2 = ax1.twinx()
    df['price'].plot(secondary_y=True, linewidth=1.5, style=['r--'])
    plt.legend(loc=1, prop={'size': 6})

    plt.title('Bitcoin assets over time from 2017-01-01 to 2018-11-26')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Amount in assets')
    ax2.set_ylabel('Bitcoin Price in USD')

    if savefile:
        plt.savefig(savefile)
    if show:
        plt.show()
    plt.clf()

def diff_rows(df, periods):
    df_diff = df.diff(periods=periods).dropna()
    return df_diff

def plot_diffs(df, exchanges, periods=1, savefile=None, show=True):
    df_diff = diff_rows(df, periods)
    
    ax1 = df_diff[exchanges].plot()
    plt.legend(loc=2, prop={'size': 6})

    ax2 = ax1.twinx()
    df_diff['price'].plot(secondary_y=True, linewidth=1.5, style=['r--'])
    plt.legend(loc=1, prop={'size': 6})

    plt.title('Bitcoin assets diff over period %d days' % periods)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Difference in assets')
    ax2.set_ylabel('Bitcoin Price Difference in USD')

    if savefile:
        plt.savefig(savefile)
    if show:
        plt.show()
    plt.clf()

def correlate_exch_price(df, exchanges):
    correlations = dict()
    for exch in exchanges:
        correlations[exch] = df[exch].corr(df['price'])
    return correlations

def correlate_diff_exch_price(df, exchanges, periods=[1]):
    correlations = dict()
    
    for exch in exchanges:
        corr_list = list()
        for period in periods:
            df_diff = diff_rows(df, period)
            corr_list.append(df_diff[exch].corr(df_diff['price']))
        correlations[exch] = corr_list
    return correlations

if __name__ == "__main__":
    price_data = read_json_file('data/price_data_updated_raw.json')
    write_json_file(price_data, 'output/price_data_updated.json')
    addresses = read_json_file('data/addresses_raw.json')
    addresses.pop('top_address_7')
    write_json_file(addresses, 'output/addresses.json')
    results = read_json_file('data/results_raw.json')
    results.pop('top_address_7')
    write_json_file(results, 'output/results.json')
    
    plot_price_data(price_data, savefile='output/prices.png', show=False)
    print_summary_price_stats(price_data)

    df, exchanges = combine_datasets(price_data, results)
    save_dataframe(df, 'output/combined_data.csv')
    df = load_dataframe('output/combined_data.csv')

    # convert date field to datetime, useful for plotting nicely
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    try:
        exchanges
    except NameError:
        exchanges = addresses.keys() 

    plot_data(df, exchanges, savefile='output/price_asset.png', show=False)

    periods = [1, 7, 14, 30, 120, 180, 365]
    for period in periods:
        savefile = 'output/price_asset_diff_period_%d.png' % period
        plot_diffs(df, exchanges, periods=period, savefile=savefile, show=False)

    print
    corr = correlate_exch_price(df, exchanges)
    print 'Correlations on raw data:'
    for k, v in corr.iteritems():
        print(k),
        if (len(k) < 7):
            print ('\t'),
        print '\t%1.4f' % (v)

    print
    corr = correlate_diff_exch_price(df, exchanges, periods)
    print('Diff Correlations')
    print('Name\t\t\t'),
    print('\t'.join(map(str,periods)))
    for k, v in corr.iteritems():
        print(k),
        if (len(k) < 7):
            print ('\t'),
        print('\t\t'),
        for val in v:
            print('%1.4f\t' % val),
        print

