import logging
import requests
import json
import time
from multiprocessing import Pool

def pool_worker(id):
	Checker(id).main()

def ip_pooler(checks, threads):
	ids = []
	for _ in range(checks): # number of checks to run
		ids.append(_)
	p = Pool(threads) # number of simultaneous checks
	p.map(pool_worker, ids)

class Checker:
	"""Check your IP addresses and other parameters on https://wtfismyip.com"""

	def __init__(self, name):
		self.name = name
		self.logging_init()

	def logging_init(self):
		"""Start the logging library at level = DEBUG. You can switch to level = ERROR when you're finished with development."""

		logging.basicConfig(filename = "./logging.log", level = logging.DEBUG) 
		self.logger = logging.getLogger()

	def time_start(self):
		self.time_start = time.time()

	def time_end(self):
		time_stop = time.time()
		self.dt = time_stop - self.time_start
		return round(self.dt, 2)

	def check_ip(self):
		try:
			request_data = requests.get('http://wtfismyip.com/json')
		except Exception as e:
			self.logger.error(e)
			raise
		json_data = json.loads(request_data.text)

		ip = json_data['YourFuckingIPAddress']
		hostname = json_data['YourFuckingHostname']
		location = json_data['YourFuckingLocation']
		isp = json_data['YourFuckingISP']

		return (
			f"Checker id: {self.name}\n"
			f"IP: {ip}\n"
			f"Hostname: {hostname}\n"
			f"Location: {location}\n"
			f"ISP: {isp}"
		)

	def main(self):
		self.time_start()
		print(self.check_ip())
		time_end = {self.time_end()}
		print(f"It took {time_end} seconds to look up this data.\n")
		self.logger.info(f"Process: {self.name}. {time_end} seconds runtime.")

if __name__ == "__main__": 
	"""This will run if this script is executed directly and NOT imported into another script"""

	print("Welcome to the IP checker!\n")

	Checker(666).main()

	#ip_pooler(checks=10, threads=2) # uncomment this to try multithreading