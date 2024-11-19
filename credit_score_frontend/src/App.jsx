import React, { useState,useEffect } from 'react';
import { useForm } from 'react-hook-form';
import {
  Card,
  Input,
  Button,
  Typography,
  Accordion,
  AccordionHeader,
  AccordionBody,
} from "@material-tailwind/react";
function App() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [result, setResult] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(true);
  // Define the min and max values for each attribute (based on your training data)
const minMaxValues = {
  CountryCode: { min: 0, max: 256 },
  ProviderId: { min: 1, max: 6 },
  ProductId: { min: 1, max: 27 },
  ChannelId: { min: 1, max: 5 },
  Amount: { min: -4325, max: 7075 },
  Value: { min: 2, max: 12087 },
  PricingStategy: { min: 0, max: 4 },
  FraudResult: { min: 0, max: 1 },
  TotalTransactionAmount: { min: -2.421208e+07	, max: 1.983448e+06 },
  AverageTransactionAmount: { min: -4325, max: 7075 },
  TransactionCount: { min: 1, max: 30893 },
  StdTransactionAmount: { min: 0, max: 4649.227086 },
  TransactionHour: { min: 0, max: 23 },
  TransactionDay: { min: 1, max: 31 },
  TransactionMonth: { min: 1, max: 12 },
  TransactionYear: { min: 2018, max: 2019 },
  ProductCategory_data_bundles: { min: 0, max: 1 },
  ProductCategory_financial_services: { min: 0, max: 1 },
  ProductCategory_movies: { min: 0, max: 1 },
  ProductCategory_other: { min: 0, max: 1 },
  ProductCategory_ticket: { min: 0, max: 1 },
  ProductCategory_transport: { min: 0, max: 1 },
  ProductCategory_tv: { min: 0, max: 1 },
  ProductCategory_utility_bill: { min: 0, max: 1 },
  Season: { min: 1, max: 4 },
  Recency: { min: 0, max: 90 },
  Frequency: { min: 1, max: 4091 },
  Monetary: { min: -1.769358e+07, max: 1.869489e+06 },
  Seasonality: { min: 0, max: 4 },
  RFMS_Score: { min: -1.768951e+07, max: 1.871361e+06 },
  WoE_RFMS: { min: -6.753046, max: 6.075848 },
};

const normalize = (data) => {
  const normalized = {};
  Object.keys(data).forEach((key) => {
    if (minMaxValues[key]) {
      const { min, max } = minMaxValues[key];
      normalized[key] = (data[key] - min) / (max - min); // Min-Max scaling
    } else {
      normalized[key] = data[key]; // Leave non-numeric fields unchanged
    }
  });
  return normalized;
};

useEffect(() => {
  if (result) {
    setLoading(false);
  }
}, [result]);

const [selectedModel, setSelectedModel] = useState("randomforest");

const handleModelChange = (event) => {
  setSelectedModel(event.target.value);
};


const [open, setOpen] = React.useState(1);
 
const handleOpen = (value) => setOpen(open === value ? 0 : value);


  const onSubmit = (data) => {
    const normalizedData = normalize(data);
    setResponseData(data); // Set the submitted data
    selectedModel === "gradientboosting"?(
    fetch('https://credit-score-model.onrender.com/predict/gradient_boosting', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(normalizedData),
    })):( fetch('https://credit-score-model.onrender.com/predict/random_forest', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(normalizedData),
    }))
      .then((response) => response.json())
      .then((result) => setResult(result))
      .catch((error) => console.error('Error:', error));
  };

  return (
    <div className="p-6">
      <Card color="transparent" shadow={false} className="p-6">
        <div className="mb-8">
          <h2 className='text-blue-900 text-4xl text-center'>User Transaction Data Form</h2>
          <Accordion open={open === 1}>
        <AccordionHeader onClick={() => handleOpen(1)}>What is the purpose of this model?</AccordionHeader>
        <AccordionBody className="text-xl ">
        The purpose of credit scoring model is to classify users as high risk or low-risk. High-risk groups are those with high likelihood of default - those who do not pay the loan principal and interest in the specified time frame.
        </AccordionBody>
      </Accordion>
        </div>
        <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-4 gap-x-20 gap-y-3">
          {[
            { label: 'Country Code', name: 'CountryCode',  type: 'select', options: [256]},
            { label: 'Provider ID', name: 'ProviderId', type: 'select', options: [1,2,3,4,5,6] },
            { label: 'Product ID', name: 'ProductId', type: 'select', options: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] },
            { label: 'Channel ID', name: 'ChannelId', type: 'select', options: [1,2,3,4,5] },
            { label: 'Amount', name: 'Amount', type: 'number' },
            { label: 'Value', name: 'Value', type: 'number' },
            { label: 'Pricing Strategy', name: 'PricingStrategy', type: 'select', options: [0,1,2,3,4] },
            { label: 'Fraud Result', name: 'FraudResult', type: 'select', options: [0,1] },
            { label: 'Total Transaction Amount', name: 'TotalTransactionAmount', type: 'number' },
            { label: 'Average Transaction Amount', name: 'AverageTransactionAmount', type: 'number' },
            { label: 'Transaction Count', name: 'TransactionCount', type: 'number' },
            { label: 'Standard Transaction Amount', name: 'StdTransactionAmount', type: 'number' },
            { label: 'Transaction Hour', name: 'TransactionHour', type: 'select', options: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] },
            { label: 'Transaction Day', name: 'TransactionDay', type: 'select',options:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] },
            { label: 'Transaction Month', name: 'TransactionMonth', type: 'select',options:[1,2,3,4,5,6,7,8,9,10,11,12] },
            { label: 'Transaction Year', name: 'TransactionYear', type: 'select',options:[2018,2019] },
            { label: 'ProductCategory data bundles', name: 'ProductCategory_data_bundles', type: 'select',options:[0,1] },
            { label: 'ProductCategory financial services', name: 'ProductCategory_financial_services', type: 'select',options:[0,1] },
            { label: 'ProductCategory movies', name: 'ProductCategory_movies', type: 'select',options:[0,1] },
            { label: 'ProductCategory other', name: 'ProductCategory_other', type: 'select',options:[0,1] },
            { label: 'ProductCategory ticket', name: 'ProductCategory_ticket', type: 'select',options:[0,1] },
            { label: 'ProductCategory transport', name: 'ProductCategory_transport', type: 'select',options:[0,1]},
            { label: 'ProductCategory tv', name: 'ProductCategory_tv', type: 'select',options:[0,1] },
            { label: 'ProductCategory utility bill', name: 'ProductCategory_utility_bill', type: 'select',options:[0,1]},
            { label: 'Season', name: 'Season', type: 'select',options:[1,2,3,4] },
            { label: 'Recency', name: 'Recency', type: 'number' },
            { label: 'Frequency', name: 'Frequency', type: 'number' },
            { label: 'Monetary', name: 'Monetary', type: 'number' },
            { label: 'Seasonality', name: 'Seasonality', type: 'select',options:[0,1,2,3,4] },
            { label: 'RFMS Score', name: 'RFMS_Score', type: 'number' },
            { label: 'Weight of Evidence (RFMS)', name: 'WoE_RFMS', type: 'number' },
          ].map((field, index) => (
            <div key={index}>
              <label className="block text-lg font-medium text-gray-900 mb-2">
                {field.label}
              </label>
              {field.type === 'select' ? (
                <select
                  className="w-full p-2 text-lg border border-gray-300 rounded-lg"
                  {...register(field.name, { required: true })}
                >
                  {field.options.map((option, idx) => (
                    <option key={idx} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              ) : (
                <Input
                  size="lg"
                  type={field.type}
                  {...register(field.name, { required: true })}
                  error={errors[field.name] ? true : false}
                />
              )}
              {errors[field.name] && (
                <Typography variant="small" color="red" className="mt-1">
                  {field.label} is required.
                </Typography>
              )}
            </div>
          ))}
        <div className=''>
      <h1>Choose a Model</h1>
      <select
        id="model-select"
        value={selectedModel}
        onChange={handleModelChange}
      >
        <option value="gradientboosting">Gradient Boosting</option>
        <option value="randomforest">Random Forest</option>
      </select>
          </div>
          
      <div className="">
        {selectedModel === "gradientboosting" ? (
          <button type="submit" color='blue' fullwidth className='border flex items-center justify-center w-96 h-20 text-2xl bg-blue-900 text-white'>
            Predict Using Gradient Boosting
          </button>
        ) : (
          <button type="submit" color='blue' fullwidth className='border flex items-center justify-center w-96 h-20 text-2xl bg-blue-900 text-white'>
            Predict Using Random Forest
          </button>
        )}
      </div>
    
         
        </form>
      </Card>

      {loading? (
        <Card className="mt-6 p-8 shadow-lg border">
          <Typography variant="h3" color="blue-gray" className="text-center">
            Fill And Submit The Form (Loading Prediction...)
          </Typography>
        </Card>
      ) : (
        result && (
          <Card className="mt-6 p-8 shadow-lg border">
            <Typography variant="h3" color="blue-gray" className="text-center">
              Prediction Result of Classifying Users as High Risk (Bad) or Low Risk (Good)
            </Typography>
            <Typography
              variant="h3"
              className={`mt-4 text-center ${
                result.prediction === 1 ? "text-red-500" : "text-green-500"
              }`}
            >
              {result.prediction === 1 ? "Bad 🚫" : "Good ✅"}
            </Typography>
          </Card>
        )
      )}

      <div className="mt-8">
        <Typography variant="h5" color="blue-gray" className="mb-4">
          Submitted Data
        </Typography>
        {!responseData && (
          <Typography variant="body1" color="gray" className="mt-4">
            No submitted data yet...
          </Typography>
        )}
        {responseData && (
          <table className="table-auto border-collapse border border-gray-300 mt-6 w-full">
            <thead>
              <tr>
                {Object.keys(responseData).map((key, index) => (
                  <th key={index} className="border border-gray-300 px-4 py-2 text-left">
                    {key}
                  </th>
                ))}
                <th className="border border-gray-300 px-4 py-2 text-left">default_estimator</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                {Object.values(responseData).map((value, index) => (
                  <td key={index} className="border border-gray-300 px-4 py-2">
                    {value}
                  </td>
                ))}
                <td className="border border-gray-300 px-4 py-2">
                  {result?.prediction !== undefined ? result.prediction : "N/A"}
                </td>
              </tr>
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;

