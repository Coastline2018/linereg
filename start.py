#!/usr/bin/env python
import subprocess,time
def main():
	try:
		subprocess.Popen(['python server.py &'],shell=True)
		time.sleep(.5)
		#open in default browser
		subprocess.Popen(['open http://localhost:8000/linereg'],shell=True)
	except:
		time.sleep(.5)
		print 'Cannot start server; is server.py present?'
if __name__ == '__main__':
	main()

