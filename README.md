####A few Ipython additions  
- {####Extending the 'logging' mode
Ipython has a logger function; enable it by uncommenting the following lines in the `ipythoon_config.py` file 
```python
# The date format used by logging formatters for %(asctime)s
c.TerminalIPythonApp.log_datefmt = '%Y-%m-%d %H:%M:%S'
# The name of the logfile to use.
c.TerminalInteractiveShell.logfile = '/home/sweethome/.mylog'
# Start logging to the given file in append mode.
c.TerminalInteractiveShell.logappend = '/home/mnost/.ipython/profile_default/mylog'
```

To distinguish each session, add the following lines to a `startup_01.py` file placed in the `startup` folder. 

```python
from time import strftime
iip=get_ipython()
iip.logger.log_write(u"# new sesstion " + strftime('%D %H:%M:%S')+ "====================="+"\n")
```
}
