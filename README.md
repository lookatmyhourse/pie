####:) 
###Project 'logger'
	I am an Ipython user. I often write code in the interactive session without making a script. This leads to the problem of forgetting what I was doing two weeks ago. Ipython has a logger function

but if you want to add personalized messages, add the something like the following lines to a .py file into the startup folder. 

```python
from time import strftime
iip=get_ipython()
iip.logger.log_write(u"# new sesstion " + strftime('%D %H:%M:%S')+ "====================="+"\n")
```
