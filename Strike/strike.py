#!/usr/bin/python
from logging import exception
import requests
import json
import argparse,sys
import csv

def shodaninternetdb(ip):
	'''shodaninternetdb function to scan target IP'''
	response = requests.get("https://internetdb.shodan.io/%s" %(ip))
	try:
		if response.status_code == 200:
			dicionary = response.json()
			data = json.dumps(dicionary,indent=4)
			print(data)
	except Exception as e:
		print(e)


def shodaninternetexcel(iplist,output):
	'''shodaninternetexcel function to scan list of IP's & store into CSV format'''
	file = open("%s" %(iplist))
	content = file.read()
	path = content.splitlines()
	for ips in path:
		response = requests.get("https://internetdb.shodan.io/%s" %(ips))
		header = ['IP','Hostname','Ports','Tags','Vulns']
		try:
			if response.status_code == 200:
				dictionary = response.json()
				new_dict = {
							'IP':dictionary['ip'], 
							'Hostname':dictionary['hostnames'],
							'Ports':dictionary['ports'], 
							'Tags':dictionary['tags'], 
							'Vulns':dictionary['vulns']}
							
				with open("%s" %(output), 'a', newline='') as csvfile:
					writer = csv.DictWriter(csvfile, fieldnames = header)
					writer.writerow(new_dict)
		except Exception as e:
			print(e)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip',help='ip of the target')
	parser.add_argument('--iplist',help='list of target ips')
	parser.add_argument('--output',help='excel output filename')
	args = parser.parse_args()

	if args.ip:
		shodaninternetdb(args.ip)
		sys.exit()

	if args.iplist:
		shodaninternetexcel(args.iplist,args.output)
		sys.exit()
