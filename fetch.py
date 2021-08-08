#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name      : CoinMarketCap Currency Price History
# Purpose   : Download provided cryptocurrency's price history in CSV format.
# Author   	: SirDavalos
# Created   : 15 Feb 2018
# Copyright : (c) https://github.com/sirdavalos
# Licence   : MIT
#-------------------------------------------------------------------------------

import sys,re,csv,os
import argparse,datetime
import urllib2

parser = argparse.ArgumentParser()
#parser.add_argument("currency", help="for example, type: bitcoin.", type=str)
#parser.add_argument("start_date", help="2017-10-01", type=str)
#parser.add_argument("end_date", help="yyyy-mm-dd", type=str)

# Extract parameters from command line.
def parse_options(args):
	global currency
	#currency = args.currency.lower()
	#start_date = args.start_date
	#end_date	 = args.end_date
	currency = 'bitcoin'
	start_date = '2013-01-01'
	end_date = '2018-12-01'

	start_date_split = start_date.split('-')
	end_date_split	 = end_date.split('-')

	start_year = int(start_date_split[0])
	end_year = int(end_date_split[0])

	# String validation
	'''
	pattern	= re.compile('[2][0][1][0-9]-[0-1][0-9]-[0-3][0-9]')
	if not re.match(pattern, start_date):
		raise ValueError('Invalid format for the start_date: ' + start_date + ". Should be of the form: yyyy-mm-dd.")
	if not re.match(pattern, end_date):
		raise ValueError('Invalid format for the end_date: '	 + end_date	 + ". Should be of the form: yyyy-mm-dd.")
		'''
	# Datetime validation for the correctness of the date. Will throw a ValueError if not valid
	datetime.datetime(start_year,int(start_date_split[1]),int(start_date_split[2]))
	datetime.datetime(end_year,	int(end_date_split[1]),	int(end_date_split[2]))

	# CoinMarketCap's price data (at least for Bitcoin, presuambly for all others) only goes back to 2013
	invalid_args = start_year < 2013
	invalid_args = invalid_args or end_year	 < 2013
	invalid_args = invalid_args or end_year	 < start_year

	if invalid_args:
		print('Usage: ' + __file__ + ' <currency> <start_date> <end_date> --dataframe')
		sys.exit(1)

	start_date = start_date_split[0]+ start_date_split[1] + start_date_split[2]
	end_date	 = end_date_split[0]	+ end_date_split[1]	 + end_date_split[2]

	return currency, start_date, end_date

# Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.
def download_data(currency, start_date, end_date):
	url = 'https://coinmarketcap.com/currencies/' + currency + '/historical-data/' + '?start=' + start_date + '&end=' + end_date
	try:
		page = urllib2.urlopen(url,timeout=10)
		if page.getcode() != 200:
			raise Exception('Failed to load page')
		html = page.read()
		page.close()

	except Exception as e:
		print('Error fetching price data from ' + url)
		print('Currency not valid\nIt should be entered exactly as displayed on CoinMarketCap.com (case-insensitive), with dashes in place of spaces.')

		if hasattr(e, 'message'):
			print("Error message: " + e.message)
		else:
			print(e)
			sys.exit(1)

	return html

# calculate average value
def append_average(row):
	high = float(row[header.index('High')])
	low = float(row[header.index('Low')])
	average = (high + low) / 2
	row.append( '{:.2f}'.format(average) )
	return row

def reverse_list(list_rows):
	list_rows = list(reversed(list_rows))
	return list_rows

def extract_data(html):
	global header
	global rows
	"""
	Extract the price history from the HTML.

	The CoinMarketCap historical data page has just one HTML table.	This table contains the data we want.
	It's got one header row with the column names.
	"""
	head = re.search(r'<thead>(.*)</thead>', html, re.DOTALL).group(1)
	header = re.findall(r'<th .*>([\w ]+)</th>', head)
	header.append('average')

	body = re.search(r'<tbody>(.*)</tbody>', html, re.DOTALL).group(1)
	raw_rows = re.findall(r'<tr[^>]*>' + r'\s*<td[^>]*>([^<]+)</td>'*7 + r'\s*</tr>', body)

	# strip commas
	rows = []
	for row in raw_rows:
		row = [ field.translate(None, ',') for field in row ]
		rows.append(row)

	rows = [ append_average(row) for row in rows ]

	# lowercase the header
	header = [x.lower() for x in header]

	# reverse the list
	rows = reverse_list(rows)

	return header, rows

# Render data in CSV format
def render_csv_data(header, rows_list):
	pass
	#print(','.join(header))
	#for row in rows:
		#print(','.join(row))

def create_csv_file():
	global header
	global rows
	global currency
	file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/data/', currency + '.csv')
	with open(file, 'w',) as f:
		f.write(','.join(header) + '\n'.encode('utf-8'))
		for row in rows:
			f.write(','.join(row) + '\n'.encode('utf-8'))

def main(args=None):
	# assert that args is a list
	if(args is not None):
		args = parser.parse_args(args)
	else:
		args = parser.parse_args()

	currency, start_date, end_date = parse_options(args)
	html = download_data(currency, start_date, end_date)
	header, rows = extract_data(html)

	render_csv_data(header, rows)
	create_csv_file()


if __name__ == '__main__':
	main()
