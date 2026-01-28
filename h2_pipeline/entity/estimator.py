"""
Estimator model for H2 pipeline leak detection
"""
import sys
from pandas import DataFrame
from h2_pipeline.exception import H2PipelineException


class H2PipelineModel:
    """
    H2 Pipeline leak detection model
    """

    def __init__(self, preprocessor, model):
        """
        :param preprocessor: preprocessing object
        :param model: trained model object
        """
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, dataframe: DataFrame) -> str:
        """
        Predict leak status for given input dataframe
        :param dataframe: input features
        :return: prediction result
        """
        try:
            # Transform the input data using preprocessor
            transformed_data = self.preprocessor.transform(dataframe)
            
            # Make prediction
            prediction = self.model.predict(transformed_data)
            
            return prediction

        except Exception as e:
            raise H2PipelineException(e, sys)
