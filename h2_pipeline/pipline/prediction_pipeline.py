import os
import sys

import numpy as np
import pandas as pd
from h2_pipeline.entity.config_entity import H2PipelinePredictorConfig
from h2_pipeline.entity.s3_estimator import H2PipelineEstimator
from h2_pipeline.exception import H2PipelineException
from h2_pipeline.logger import logging
from h2_pipeline.utils.main_utils import read_yaml_file
from pandas import DataFrame


class H2SensorData:
    def __init__(self,
                pressure_mpa,
                temperature_celsius,
                hydrogen_concentration_ppm,
                vibration_hz,
                pipe_age_years,
                material,
                flow_rate_kg_h,
                corrosion_rate_mm_year,
                soil_moisture_percent,
                operating_hours
                ):
        """
        H2 Sensor Data constructor
        Input: all sensor features for hydrogen pipeline leak detection
        """
        try:
            self.pressure_mpa = pressure_mpa
            self.temperature_celsius = temperature_celsius
            self.hydrogen_concentration_ppm = hydrogen_concentration_ppm
            self.vibration_hz = vibration_hz
            self.pipe_age_years = pipe_age_years
            self.material = material
            self.flow_rate_kg_h = flow_rate_kg_h
            self.corrosion_rate_mm_year = corrosion_rate_mm_year
            self.soil_moisture_percent = soil_moisture_percent
            self.operating_hours = operating_hours

        except Exception as e:
            raise H2PipelineException(e, sys) from e

    def get_h2_input_data_frame(self) -> DataFrame:
        """
        This function returns a DataFrame from H2SensorData class input
        """
        try:
            h2_input_dict = self.get_h2_data_as_dict()
            return DataFrame(h2_input_dict)

        except Exception as e:
            raise H2PipelineException(e, sys) from e

    def get_h2_data_as_dict(self):
        """
        This function returns a dictionary from H2SensorData class input 
        """
        logging.info("Entered get_h2_data_as_dict method as H2SensorData class")

        try:
            input_data = {
                "pressure_mpa": [self.pressure_mpa],
                "temperature_celsius": [self.temperature_celsius],
                "hydrogen_concentration_ppm": [self.hydrogen_concentration_ppm],
                "vibration_hz": [self.vibration_hz],
                "pipe_age_years": [self.pipe_age_years],
                "material": [self.material],
                "flow_rate_kg_h": [self.flow_rate_kg_h],
                "corrosion_rate_mm_year": [self.corrosion_rate_mm_year],
                "soil_moisture_percent": [self.soil_moisture_percent],
                "operating_hours": [self.operating_hours],
            }

            logging.info("Created h2 sensor data dict")
            logging.info("Exited get_h2_data_as_dict method as H2SensorData class")

            return input_data

        except Exception as e:
            raise H2PipelineException(e, sys) from e


class H2PipelineLeakDetector:
    def __init__(self, prediction_pipeline_config: H2PipelinePredictorConfig = H2PipelinePredictorConfig()) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise H2PipelineException(e, sys)

    def predict(self, dataframe) -> str:
        """
        This is the method of H2PipelineLeakDetector
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of H2PipelineLeakDetector class")
            model = H2PipelineEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result = model.predict(dataframe)

            return result

        except Exception as e:
            raise H2PipelineException(e, sys)
