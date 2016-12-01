# import csv
# Get Ticker From System Param.

from datetime import datetime


def get_stock_data(ticker):
    # Static Data
    stock_day_list = []
    samplespath = "../samples/%s.csv" % ticker

    # line_counter = 0
    # with open(csv) as file:
    #     file.readline()  # remove csv header
    #     for line in file:
    #         line_counter += 1
    #         stock_day_list.append(StockDay(line, line_counter))

    # return stock_day_list

    line_counter = 0
    with open(samplespath) as file:
        file.readline()  # remove csv header
        for line in file:
            line_counter += 1
            line = line.strip('\n')
            data = line.split(',')
            # Insert entry and maintain ordering from old to new
            stock_day_list.append({
                'date': datetime.strptime(data[0], '%Y-%m-%d').date(),
                'o': round(float(data[1]), 2),
                'h': round(float(data[2]), 2),
                'l': round(float(data[3]), 2),
                'c': round(float(data[4]), 2),
                'vol': int(data[5])})

    return stock_day_list
