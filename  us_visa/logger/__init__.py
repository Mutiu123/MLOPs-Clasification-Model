import logging
import os

from from_root import from_root
from datetime import datetime
#logging string
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#logging directory/folder name
log_dir = 'logs'
#create file
logs_path = os.path.join(from_root(), log_dir, LOG_FILE)
#create log directory
os.makedirs(log_dir, exist_ok=True)

#script for creating logging information
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

