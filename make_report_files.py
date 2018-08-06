import argparse
import json
import csv
import os
import sys
from collections import OrderedDict as od
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal


def check_arg(args=None):
    ''' This function reads command line options.'''
    parser = argparse.ArgumentParser(description='Script which generates CSV/XLSX and PNG files from JSON data')
    parser.add_argument('-e', '--excel', action="store_true",
                        help='Generate Excel XLSX file', default=None,)
    parser.add_argument('-i', '--input_file', required=True,
                        help='Input JSON file name, -i rts.json')
    parser.add_argument('-d', '--results_dir', default='/tmp',
                        help='Results directory, -d /tmp)')
    parser.add_argument('-c', '--csv', default=None, action="store_true",
                        help='Generate CSV file')
    parser.add_argument('-p', '--png', default=None, action="store_true",
                        help='Generate PNG file')
    parser.add_argument('--html', default=None, action="store_true",
                        help='Generate HTML file')
    arguments = parser.parse_args(args)
    return (arguments.excel, arguments.input_file,
            arguments.results_dir, arguments.csv,
            arguments.png, arguments.html)


def main():
    print(input_file)
    file_name = input_file.split('.')[1]
    file_name = file_name.strip('\\')
    print(file_name)
    with open(input_file) as json_file:
        data = json.load(json_file, parse_int=Decimal, parse_float=Decimal)
    df = pd.DataFrame(data)
    if csv:
        df.to_csv(file_name + '.csv', sep=',', index=False)
    if html:
        df.to_html(file_name + '.html')
    if png:
        ax = plt.gca()
        df = df.astype(float)
        df.plot(kind='line', x='Timestamp', y='appTxFrameDataRate', ax=ax,
                markevery=10, marker='o', markerfacecolor='black', grid=True)
        df.plot(kind='line', x='Timestamp', y='appTxFrameDataRate', color='red', ax=ax,
                markevery=10, marker='o', markerfacecolor='black', grid=True)
        df.plot(kind='line', x='Timestamp', y='appFlowRate', color='brown', ax=ax,
                markevery=10, marker='o', markerfacecolor='black', grid=True)
        # plt.show()
        plt.savefig(file_name + '.png')
    if excel:
        writer = pd.ExcelWriter(file_name + '.xlsx')
        df.to_excel(writer, file_name, index=False)
        writer.save()

if __name__ == '__main__':
    excel, input_file, results_dir, csv, png, html = check_arg(sys.argv[1:])
    os.makedirs(results_dir, exist_ok=True)
    main()
