# Credit Scoring Model for Bati Bank

## Project Overview
This project aims to develop a **credit scoring model** for Bati Bank to enable a "buy-now-pay-later" system by assessing users' creditworthiness. The model classifies users as **high-risk** or **low-risk** based on their transaction data, helping the bank mitigate default risks and improve loan decision-making.

---

## Features
- **Data Preprocessing**:
  - Handling missing values and outliers.
  - Encoding categorical variables and normalizing numerical data.
- **Feature Engineering**:
  - Aggregate features: Total transaction amount, average transaction value, transaction count, and variability.
  - Extracted features: Transaction hour, month, and year.
  - RFMS-based default estimator with Weight of Evidence (WoE) binning.
- **Model Development**:
  - Trained models: Random Forest and Gradient Boosting Machines.
  - Hyperparameter tuning for optimal performance.
- **API Development**:
  - Built a REST API using FastAPI for real-time predictions.
  - Endpoints for receiving input data and returning classification results.
- **Deployment**:
  - Dockerized application for seamless deployment.
  - CI/CD pipeline for automated testing and deployment.
- **Visualization Dashboard**:
  - Interactive dashboard for visualizing fraud trends, risk categories, and geographic data.

---

## Installation

### Prerequisites
Ensure the following are installed on your system:
- Python 3.9 or higher
- Docker
- Git

### Clone the Repository

- git clone https://github.com/GuleWako/Credit-Risk-Analysis.git
- cd Credit-Risk-Analysis

### Install Dependencies
- pip install -r requirements.txt
```bash