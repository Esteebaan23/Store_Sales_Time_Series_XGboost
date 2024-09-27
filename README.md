# Sales Prediction App(XGboost)

This is a simple web-based application for predicting sales using the XGboost model. The app is built with **FastAPI** on the backend, and the frontend is a basic HTML form that takes user input for various features and returns a predicted sales value. It also has predicted the sales and transactions for each store given from the test dataset.

## Features

- **Predict sales** using historical data and external factors like promotions, oil prices, day of the week, and payday.
- **Interactive web form** to input the necessary data and get the sales prediction in real-time.
- Uses a trained **XGboost model** for time series forecasting.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, JavaScript (Vanilla)
- **Machine Learning**: XGBoost model
- **Deployment**: Can be deployed on Heroku or any server supporting FastAPI, for now just in local host.

## Requirements

- Python 3.7+
- FastAPI
- Pandas
- Statsmodels
- Uvicorn (for running the FastAPI server)
- starlette
- plotly
- xgboost
- scikit-learn
- python-multipart

## Setup

1. Download the Zip file and open it.

2. Create Viirtual environments
   ```bash
   python -m venv myenv
   source myenv/bin/activate
    # On Windows: myenv\Scripts\activate
5. Replace the data file path in app.py according to your local file path
6. install dependencies
     ```bash
    pip install -r requirements.txt

If there is any questions you may follow the Steps.docx that you can find in the ZIP file or in the repository.
