from gps3.agps3threaded import AGPS3mechanism
import time
import os
class gpsAntenna:
	def __init__(self):
		self.agps_thread = AGPS3mechanism()
		self.agps_thread.stream_data()
		self.agps_thread.run_thread()

	def getLoc(self):
		"""gets and returns a lat/lon tuple"""
		val = (self.agps_thread.data_stream.lat, self.agps_thread.data_stream.lon)
		while val == ('n/a','n/a'):	#if we can't get a fix, keep trying until we can
			sleep(1)
			val = (self.agps_thread.data_stream.lat, self.agps_thread.data_stream.lon)
		return val

	def checkSKY(self):
		"""returns the satellites the antenna has a fix on"""
		return self.agps_thread.data_stream.satellites

	def countSKY(self)
		return len(checkSKY())