
#from us_visa.logger import *
import sys
from us_visa.logger import logging 
from us_visa.exception import USvisaException


logging.info("logging info testing")

try: 
    b = 5/0
except Exception as e:
    raise USvisaException(e, sys)
