#!/usr/bin/env python 
'''linereg.py takes input from an html gui in the form of user-generated
data points. These points are sent through ajax over a local server
to linereg.py for trendline fitting. The learning rate is automatically
selected and the cost is minimized by gradient descent. The resulting 
slope and intercept parameters are sent back to linereg.html and 
overlaid on the original data. '''
import cgi,json,sys,copy,time
from decimal import Decimal
from operator import itemgetter
print

def main():
	start=time.time()
	global x
	global y
	
	data = cgi.FieldStorage()['package'].value
	data = json.loads(data)
	points = data[0]
	prec = float(data[1])
	if not points or len(points) == 1:
		print 'insufficient data'
		sys.exit()
	
	#first guess of th0/th1
	x_sort = sorted(points)
	y_sort = sorted(points,key=itemgetter(1))
	if abs(x_sort[-1][0]-x_sort[0][0]) > abs(y_sort[-1][1]-y_sort[0][1]):
		th1=(x_sort[-1][1]-x_sort[0][1])/(x_sort[-1][0]-x_sort[0][0])
		th0=x_sort[0][1] - th1*x_sort[0][0]
	else:
		th1=(y_sort[-1][1]-y_sort[0][1])/(y_sort[-1][0]-y_sort[0][0])
		th0=y_sort[0][1] - th1*y_sort[0][0]
	
	x=[float(x_[0]) for x_ in points]
	y=[float(y_[1]) for y_ in points]
	
	def th0_sum(th0,th1):
		return sum([th0+th1*x[i]-y[i] for i in range(len(x))])
		
	def th1_sum(th0,th1):
		return sum([( th0+th1*x[i]-y[i] )*x[i] for i in range(len(x))])
		
	def cost_sum(th0,th1):
		return sum([ (th0+th1*x[i]-y[i])**2 for i in range(len(x))])
	
	def compute(alpha,th0,th1,prec):
		#initialize some parameters
		#th0=0.; th1=0.; 
		th0_tmp=0.
		m=len(x)
		cost_new=0.; cost_old=0.
		th0s=[];th1s=[];J=[];diffs=[]
		
		while 1:	
			#new theta parameters
			th0_tmp=th0-alpha/m*th0_sum(th0,th1)		
			th1=th1-alpha/m*th1_sum(th0,th1)
			th0=th0_tmp
			#new cost
			cost_old=cost_new
			cost_new=1./(2*m)*cost_sum(th0,th1)
			if cost_new > (cost_old+1000000):	#cost explosion; alpha too high
				return 'high'
			diff=cost_new-cost_old
		
			th0s.append(th0)
			th1s.append(th1)
			J.append(cost_new)
			diffs.append(diff)
		
			if abs(diff) < prec:	#cost minimized
				return th0,th1,th0s,th1s

	alpha=.1	#initial alpha
	alpha_iter = 1
	while 1:	#auto-generate alpha value by trial
		result=compute(alpha,th0,th1,prec)	
		if result == 'high':
			alpha=alpha*9./10	#new alpha
			alpha_iter+=1
		else:
			th0=result[0]
			th1=result[1]
			th0s=result[2]
			th1s=result[3]
			break
	iterations = len(th0s)
	th0s = [th0s[x] for x in range(0,len(th0s),20)]
	th1s = [th1s[x] for x in range(0,len(th1s),20)]
	elapsed = int(10*(time.time()-start))/10.	
	package = [th0,th1,elapsed,'%.2E' % Decimal(str(alpha)),alpha_iter,iterations]
	print json.dumps(package)
	
if __name__ == '__main__':
	main()