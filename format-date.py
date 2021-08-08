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

def format_date(string):
	date = string.split(' ')

	day = '%.02d' % int(date[1])
	year = '%.04d' % int(date[2])

	if date[0] == 'Jan':
		month = '%.02d' % 1
	elif date[0] == 'Feb':
		month = '%.02d' % 2
	elif date[0] == 'Mar':
		month = '%.02d' % 3
	elif date[0] == 'Apr':
		month = '%.02d' % 4
	elif date[0] == 'May':
		month = '%.02d' % 5
	elif date[0] == 'Jun':
		month = '%.02d' % 6
	elif date[0] == 'Jul':
		month = '%.02d' % 7
	elif date[0] == 'Aug':
		month = '%.02d' % 8
	elif date[0] == 'Sep':
		month = '%.02d' % 9
	elif date[0] == 'Oct':
		month = '%.02d' % 10
	elif date[0] == 'Nov':
		month = '%.02d' % 11
	elif date[0] == 'Dec':
		month = '%.02d' % 12

	return year + '-' + month + '-' + day

def main():
	file_csv = file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/data/bitcoin.csv')
	df = pd.read_csv(file_csv)

	for i in range(0,len(df.index)):
	#print(df['date'][i])
	#df['date'][i] = format_date(df['date'][i])
		df.loc[i, 'date'] = format_date(df['date'][i])

	print(df['date'])

	# Write to CSV file
	df.to_csv(file_csv, sep=',', encoding='utf-8', index=False ,float_format='%.2f')

if __name__ == '__main__':
	main()