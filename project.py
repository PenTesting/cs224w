# CS224W Project
# David Golub and Liam Kelly
# Stanford University

import json
import snap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

if __name__ == "__main__":
    price_data = read_json_file()
    # write_json_file(price_data)
    # plot_price_data(price_data, savefile='prices.png', show=False)
    print_summary_price_stats(price_data)
