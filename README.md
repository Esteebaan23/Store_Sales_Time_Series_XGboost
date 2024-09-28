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
Open your Windows Terminal and follow the next steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Esteebaan23/XGboost.git

2. Unzip the Statics folder inside the cloned folder

3. Create Viirtual environments
   ```bash
   python -m venv myenv
   source myenv/bin/activate
    # On Windows: myenv\Scripts\activate
4. Replace the data file path in app.py according to your local file path
   ```bash
   cd + "Your path"
5. Install dependencies
    ```bash
    pip install -r requirements.txt

6. If for some reason scikit-learn, uvicorn and python-multipart don't get installed try:
   ```bash
   pip install scikit-learn uvicorn python-multipart

6. Then, in your cmd paste:
   ```bash
   uvicorn app:app --reload
   
7. Open the deployment at: http://127.0.0.1:8000


If there is any questions you may follow the Steps.docx that you can find in the Deployment ZIP file or in the repository.
