from us_visa.logger import logging

logging.info("double logging test")

from us_visa.exception import USvisaException
import sys 

try:
    comp = 5/1 
except Exception as e:
    raise USvisaException(e, sys)