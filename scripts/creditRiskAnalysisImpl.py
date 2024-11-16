import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder


def dataLoading():
    return pd.read_csv('docs/data.csv')
def distOfNumericalColumns(data,numerical_columns):
    for col in numerical_columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[col],bins=50, kde=True)
        plt.title(f'Distribution of {col}')
        plt.show()
def distOfCategoricalColumns(data,categorical_columns):
    for col in categorical_columns:
        plt.figure(figsize=(20, 6))
        sns.countplot(data=data, x=data[col])
        plt.title(f'Distribution of {col}')
        plt.xticks(rotation=45) 
        plt.show()
def correlationOfNumColumns(data):
    numerical_data=data.select_dtypes(include=['float64', 'int64'])
    if 'CountryCode' in numerical_data.columns:
        numerical_data=numerical_data.drop(['CountryCode'],axis=1)
    correlation_matrix=numerical_data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title('Correlation Matrix')
    plt.show()
def find_missing_values(df):
    null_counts = df.isnull().sum()
    missing_value = null_counts
    percent_of_missing_value = 100 * null_counts / len(df)
    data_type = df.dtypes

    missing_data_summary = pd.concat([missing_value, percent_of_missing_value, data_type], axis=1)
    missing_data_summary_table = missing_data_summary.rename(columns={0: "Missing values", 1: "Percent of Total Values", 2: "DataType"})
    missing_data_summary_table = missing_data_summary_table[missing_data_summary_table.iloc[:, 1] != 0].sort_values('Percent of Total Values', ascending=False).round(1)

    print(f"From {df.shape[1]} columns selected, there are {missing_data_summary_table.shape[0]} columns with missing values.")

    return missing_data_summary_table

def boxPlotForDetectOutliers(data,column_names):
    for column in column_names:
        sns.boxplot(data=data[column])
        plt.title(f"Box Plot of {column}")
        plt.show()
def remove_outliers_winsorization(data,column_names):
    for column_name in column_names:
        q1 = data[column_name].quantile(0.25)
        q3 = data[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        data[column_name] = data[column_name].clip(lower_bound, upper_bound)
    return data
def aggregateFeatures(data):
    # Aggregate features by customer (AccountId)
    agg_data = data.groupby('AccountId').agg(
        TotalTransactionAmount=('Amount', 'sum'),
        AverageTransactionAmount=('Amount', 'mean'),
        TransactionCount=('TransactionId', 'count'),
        StdTransactionAmount=('Amount', 'std')
    ).reset_index()
    return agg_data
def extractDateAndTime(new_dataframe):
    # Converting TransactionStartTime to datetime format
    new_dataframe['TransactionStartTime'] = pd.to_datetime(new_dataframe['TransactionStartTime'])

    # Extracting date and time-based features
    new_dataframe['TransactionHour'] = new_dataframe['TransactionStartTime'].dt.hour
    new_dataframe['TransactionDay'] = new_dataframe['TransactionStartTime'].dt.day
    new_dataframe['TransactionMonth'] = new_dataframe['TransactionStartTime'].dt.month
    new_dataframe['TransactionYear'] = new_dataframe['TransactionStartTime'].dt.year
    return new_dataframe
def encodingCategoricalVariables(new_dataframe):
    categorical_columns = ['CurrencyCode', 'ProductCategory']
    encoder = OneHotEncoder(sparse_output=False, drop='first')  
    encoded_data = encoder.fit_transform(new_dataframe[categorical_columns])
    encoded_new_dataframe = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
    new_dataframe_encoded = pd.concat([new_dataframe.reset_index(drop=True), encoded_new_dataframe], axis=1)
    new_dataframe_encoded.drop(columns=categorical_columns, inplace=True)
    return new_dataframe_encoded
def calculateRFMSscores(new_dataframe_encoded):
    # Ensure TransactionStartTime is in datetime format
    new_dataframe_encoded['TransactionStartTime'] = pd.to_datetime(new_dataframe_encoded['TransactionStartTime'])

    # Set the current date (or use the last date in your dataset)
    current_date = new_dataframe_encoded['TransactionStartTime'].max()

    # Recency: Number of days since the last transaction
    recency_new_dataframe_encoded = new_dataframe_encoded.groupby('CustomerId').agg({'TransactionStartTime': lambda x: (current_date - x.max()).days})
    recency_new_dataframe_encoded.rename(columns={'TransactionStartTime': 'Recency'}, inplace=True)

    # Frequency: Count of transactions per customer
    frequency_new_dataframe_encoded = new_dataframe_encoded.groupby('CustomerId').agg({'TransactionId': 'count'})
    frequency_new_dataframe_encoded.rename(columns={'TransactionId': 'Frequency'}, inplace=True)

    # Monetary: Sum of transaction amounts per customer
    monetary_new_dataframe_encoded = new_dataframe_encoded.groupby('CustomerId').agg({'Amount': 'sum'})
    monetary_new_dataframe_encoded.rename(columns={'Amount': 'Monetary'}, inplace=True)

    # Seasonality: You can derive this by checking the number of transactions per season (quarter)
    new_dataframe_encoded['Season'] = new_dataframe_encoded['TransactionStartTime'].dt.quarter
    seasonality_new_dataframe_encoded = new_dataframe_encoded.groupby('CustomerId').agg({'Season': 'mean'})
    seasonality_new_dataframe_encoded.rename(columns={'Season': 'Seasonality'}, inplace=True)

    # Merge the dataframes into a single dataframe
    rfms_new_dataframe_encoded = recency_new_dataframe_encoded.merge(frequency_new_dataframe_encoded, on='CustomerId')
    rfms_new_dataframe_encoded = rfms_new_dataframe_encoded.merge(monetary_new_dataframe_encoded, on='CustomerId')
    rfms_new_dataframe_encoded = rfms_new_dataframe_encoded.merge(seasonality_new_dataframe_encoded, on='CustomerId')

    # Normalize the RFMS scores (equal weights for simplicity)
    rfms_new_dataframe_encoded['RFMS_Score'] = (rfms_new_dataframe_encoded['Recency'] * -1 +
                            rfms_new_dataframe_encoded['Frequency'] +
                            rfms_new_dataframe_encoded['Monetary'] +
                            rfms_new_dataframe_encoded['Seasonality'])

    # # Normalize the RFMS scores between 0 and 1
    # rfms_new_dataframe_encoded['RFMS_Score'] = (rfms_new_dataframe_encoded['RFMS_Score'] - rfms_new_dataframe_encoded['RFMS_Score'].min()) / (rfms_new_dataframe_encoded['RFMS_Score'].max() - rfms_new_dataframe_encoded['RFMS_Score'].min())
    return rfms_new_dataframe_encoded
def visualizeRFMSscore(rfms_new_dataframe_encoded):
    # Plot the histogram of RFMS scores
    plt.figure(figsize=(8,6))
    plt.hist(rfms_new_dataframe_encoded['RFMS_Score'], bins=30, color='blue', alpha=0.7)
    plt.title('RFMS Score Distribution')
    plt.xlabel('RFMS Score')
    plt.ylabel('Frequency')
    plt.show()
    
def calculate_woe_iv(data, feature, target):
    lst = []
    unique_values = data[feature].unique()
    total_good = len(data[data[target] == 1])
    total_bad = len(data[data[target] == 0])

    for val in unique_values:
        dist_good = len(data[(data[feature] == val) & (data[target] == 1)]) / total_good if total_good != 0 else 0
        dist_bad = len(data[(data[feature] == val) & (data[target] == 0)]) / total_bad if total_bad != 0 else 0

        # Handle cases where dist_good or dist_bad is zero
        if dist_good == 0:
            dist_good = 0.0001
        if dist_bad == 0:
            dist_bad = 0.0001

        woe = np.log(dist_good / dist_bad)
        iv = (dist_good - dist_bad) * woe
        lst.append({'Value': val, 'WoE': woe, 'IV': iv})

    return pd.DataFrame(lst)