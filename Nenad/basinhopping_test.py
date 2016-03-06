from scipy.optimize import basinhopping
from pylab import *

func = lambda x: cos(14.5 * x - 0.3) + (x + 0.2) * x
x0=[1.]
"""
Basinhopping, internally, uses a local minimization algorithm.  We will use
the parameter ``minimizer_kwargs`` to tell basinhopping which algorithm to
use and how to set up that minimizer.  This parameter will be passed to
``scipy.optimize.minimize()``.
"""
minimizer_kwargs = {"method": "BFGS"}
ret = basinhopping(func, x0, minimizer_kwargs=minimizer_kwargs,niter=200)
print("global minimum: x = %.4f, f(x0) = %.4f" % (ret.x, ret.fun))
