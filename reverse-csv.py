#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name      : CoinMarketCap Currency Price History
# Purpose   : Change time format of the dataframe column and save to CSV file.
# Author   	: SirDavalos
# Created   : 15 Feb 2018
# Copyright : (c) https://github.com/sirdavalos
# Licence   : MIT
#-------------------------------------------------------------------------------

import os
import pandas as pd

def format_date(data):
	data_reversed = reverse_list(data)

	return data_reversed

def main():
	file_csv = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/data/aapl.csv')
	df = pd.read_csv(file_csv)

	df = df.iloc[::-1]

	# Write to CSV file
	df.to_csv(file_csv, sep=',', encoding='utf-8', index=False ,float_format='%.2f')

if __name__ == '__main__':
	main()