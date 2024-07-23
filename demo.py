
"""
import os 
mongodb_db_url = os.getenv("MONGODB_URL")
print(mongodb_db_url)

"""
from us_visa.pipline.training_pipeline import TrainPipeline

obj = TrainPipeline()
obj.run_pipeline()
