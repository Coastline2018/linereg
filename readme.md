`linereg` is an simple experiment in linear regression plotting of user-generated data, written in python 2.7. 

The program is invoked from the command line with the command `python start.py`, 
which starts a localhost server (`server.py`), serving on port 8000. 

`linereg.html` is read from file `linereg` and opened in the default browser. 

The simple interface allows points to be drawn in a 400x400 pixel area. 

The 'regression' button sends the point data to `linereg.py` for processing via jquery/ajax. 

Linear regression is performed in python by minimizing the cost function through gradient descent. 

The output (theta values) is returned to `linereg.html` for plotting, where a trendline is drawn over the data. 

![alt tag](https://github.com/markedwinharvey/linereg/blob/master/media/before.trendline.png)
