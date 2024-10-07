import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import uvicorn
from glob import glob
import numpy as np
logging.basicConfig(level=logging.INFO)


# Load the latest model using joblib
logging.info(f"Loading model...")
model = joblib.load('../credit_scoring_random_forest_model.pkl')

# Create a FastAPI instance
app = FastAPI()

class InputData(BaseModel):
    CountryCode: float
    ProviderId: float
    ProductId: float
    ChannelId: float
    Amount: float
    Value: float
    PricingStategy: float
    FraudResult: float 
    TotalTransactionAmount: float
    AverageTransactionAmount: float
    TransactionCount: float
    StdTransactionAmount: float
    TransactionHour: float
    TransactionDay: float
    TransactionMonth: float
    TransactionYear: float
    ProductCategory_data_bundles: float 
    ProductCategory_financial_services: float
    ProductCategory_movies: float
    ProductCategory_other: float
    ProductCategory_ticket: float
    ProductCategory_transport: float
    ProductCategory_tv: float
    ProductCategory_utility_bill: float
    Season: float
    Recency: float
    Frequency: float
    Monetary: float
    Seasonality: float
    RFMS_Score: float
    WoE_RFMS: float

    

#  endpofloat
@app.post('/predict')
async def predict(input_data: InputData):
    try:
        # Convert input data to DataFrame
        input_df = np.array([[input_data.CountryCode,
            input_data.ProviderId,
            input_data.ProductId,
            input_data.ChannelId,
            input_data.Amount,
            input_data.Value,
            input_data.PricingStategy,
            input_data.FraudResult,
            input_data.TotalTransactionAmount,
            input_data.AverageTransactionAmount,
            input_data.TransactionCount,
            input_data.StdTransactionAmount,
            input_data.TransactionHour,
            input_data.TransactionDay,
            input_data.TransactionMonth,
            input_data.TransactionYear,
            input_data.ProductCategory_data_bundles,
            input_data.ProductCategory_financial_services,
            input_data.ProductCategory_movies,
            input_data.ProductCategory_other,
            input_data.ProductCategory_ticket,
            input_data.ProductCategory_transport,
            input_data.ProductCategory_tv,
            input_data.ProductCategory_utility_bill,
            input_data.Season,
            input_data.Recency,
            input_data.Frequency,
            input_data.Monetary,
            input_data.Seasonality,
            input_data.RFMS_Score,
            input_data.WoE_RFMS
            ]], 
                                 )
        
        # Make predictions
        predictions = model.predict(input_df)
        predicted_values = predictions.tolist() 

        # Return the predictions as a JSON response
        return {'predictions': predicted_values}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
