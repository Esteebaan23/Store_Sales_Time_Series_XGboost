import pandas as pd
from fastapi import FastAPI, Form
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import plotly.express as px
import plotly.io as pio
import xgboost as xgb
import random


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


loaded_model_sales = xgb.XGBRegressor()
loaded_model_sales.load_model("xgboost_model_sales.json")

loaded_model_transactions = xgb.XGBRegressor()
loaded_model_transactions.load_model("xgboost_model_transactions.json")


test_dataset_sales = pd.read_csv('Test_sales.csv')
test_dataset_transactions = pd.read_csv('Test_Transactions.csv')
tabla_nueva = pd.read_csv('test.csv')


predictions_sales = loaded_model_sales.predict(test_dataset_sales)
tabla_nueva['sales'] = predictions_sales

stores = tabla_nueva.groupby(['date', 'store_nbr'], as_index=False)['sales'].sum()
test_dataset_transactions.insert(1, 'sales', predictions_sales)

predictions_transactions = loaded_model_transactions.predict(test_dataset_transactions)
tabla_nueva['transactions'] = predictions_transactions

tabla_plot = tabla_nueva.groupby(['date', 'store_nbr'])['transactions'].mean().reset_index()
fechas_unicas = stores['date'].unique()
tiendas_unicas = stores['store_nbr'].unique()


@app.get("/", response_class=HTMLResponse)
def render_menu():
    html_content = '''
    <html>
        <head>
            <title>Sales and Transactions Dashboard</title>
            <style>
                body {{
                    text-align: center;
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                }}
                img {{
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    width: 200px;
                }}
                .menu {{
                    margin-top: 20px;
                    margin-bottom: 30px;
                }}
                .content {{
                    margin-top: 30px;
                }}
                .center {{
                    margin-left: auto;
                    margin-right: auto;
                    width: 80%;
                }}
                h1 {{
                    text-align: center;
                }}
                .prediction {{
                    margin-top: 20px;
                    font-size: 18px;
                    color: green;
                }}
                .container {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 400px;
                    margin: 20px auto;
                }}
                table {{
                    width: 100%;
                    margin: 10px 0;
                }}
                td {{
                    padding: 8px;
                    text-align: left;
                }}
                input, select {{
                    width: calc(100% - 16px);
                    padding: 8px;
                    margin: 4px 0;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }}
                .button {{
                    width: 100%;
                    padding: 10px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                .button:hover {{
                    background-color: #45a049;
                }}
                .prediction-result {{
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #e7f3e7;
                    border: 1px solid #d4edda;
                    border-radius: 4px;
                    color: #155724;
                    display: none;
                    text-align: center;
                }}
            </style>
            <script>
                function predictSales() {{
                    var date = document.getElementById('sales-date').value;
                    var store = document.getElementById('sales-store').value;
                    var salesValue = document.getElementById('sales-' + date + '-' + store).innerText;
                    var prediction = "On " + date + " the store " + store + " sold " + salesValue + " products.";
                    document.getElementById('sales-prediction').innerText = prediction;
                }}
                
                function predictTransactions() {{
                    var date = document.getElementById('transactions-date').value;
                    var store = document.getElementById('transactions-store').value;
                    var transactionsValue = document.getElementById('transactions-' + date + '-' + store).innerText;
                    var prediction = "On " + date + " the store " + store + " got " + transactionsValue + " transactions.";
                    document.getElementById('transactions-prediction').innerText = prediction;
                }}
            </script>
        </head>
        <body>
            <img src="/static/Corporación_Favorita_Logo.png" alt="Dashboard Logo" />

            <h1>Sales and Transactions Dashboard</h1>

            <div id="xgboost" class="content" style="display:block;">
                <h2>Sales per Store</h2>
                <div class="center">
                    {graph_sales}
                </div>
                
                <label for="sales-date">Date:</label>
                <select id="sales-date">
                    {fechas_options}
                </select>
                
                <label for="sales-store">Store:</label>
                <select id="sales-store">
                    {tiendas_options}
                </select>
                
                <button onclick="predictSales()">Predict</button>
                <div id="sales-prediction" class="prediction"></div>

                <h2>Transactions per Store</h2>
                <div class="center">
                    {graph_transactions}
                </div>
                
                <label for="transactions-date">Date:</label>
                <select id="transactions-date">
                    {fechas_options}
                </select>
                
                <label for="transactions-store">Store:</label>
                <select id="transactions-store">
                    {tiendas_options}
                </select>
                
                <button onclick="predictTransactions()">Predict</button>
                <div id="transactions-prediction" class="prediction"></div>
            </div>

            <div class="container">
                <h1>Sales prediction by Product</h1>
                <form action="/predict" method="post" id="prediction-form">
                    <table>
                        <tr>
                            <td><label for="store_nbr">Store Number:</label></td>
                            <td><input type="number" id="store_nbr" name="store_nbr" min="0" max="53" value="0"></td>
                        </tr>
                        <tr>
                            <tr>
                                <td><label for="onpromotion">On Promotion:</label></td>
                                <td><input type="number" id="onpromotion" name="onpromotion" min="0" max="646" value="0"></td>
                            </tr>
                        </tr>
                        <tr>
                            <td><label for="weekday">Week Day:</label></td>
                            <td><input type="number" id="weekday" name="weekday" min="0" max="6" value="0"></td>
                        </tr>
                        <tr>
                            <td><label for="date">Date:</label></td>
                            <td><input type="date" id="date" name="date"></td>
                        </tr>
                        <tr>
                            <td><label for="payday">Pay day?:</label></td>
                            <td>
                                <select id="payday" name="payday">
                                    <option value="1">Yes</option>
                                    <option value="0">No</option>
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td><label for="is_weekend">Is weekend?:</label></td>
                            <td>
                                <select id="is_weekend" name="is_weekend">
                                    <option value="1">Yes</option>
                                    <option value="0">No</option>
                                </select>
                            </td>
                        </tr>
                    </table>
                    <button type="submit" class="button">Predict</button>
                </form>
                <div id="prediction-result" class="prediction-result"></div>
            </div>

            <script>
                document.getElementById('prediction-form').addEventListener('submit', async function(event) {{
                    event.preventDefault();
                    const formData = new FormData(this);
                    const response = await fetch('/predict', {{
                        method: 'POST',
                        body: formData
                    }});
                    const result = await response.text();
                    document.getElementById('prediction-result').innerHTML = "The sales prediction is: " + result;
                    document.getElementById('prediction-result').style.display = 'block';
                }});
            </script>
        </body>
    </html>
    '''

    fig_sales = px.line(stores, x="date", y="sales", color="store_nbr")
    fig_sales.update_layout(width=1200, height=500)
    graph_sales = pio.to_html(fig_sales, full_html=False)

    fig_transactions = px.line(tabla_plot, x="date", y="transactions", color="store_nbr")
    fig_transactions.update_layout(width=1200, height=500)
    graph_transactions = pio.to_html(fig_transactions, full_html=False)

    fechas_options = ''.join([f'<option value="{fecha}">{fecha}</option>' for fecha in fechas_unicas])
    tiendas_options = ''.join([f'<option value="{tienda}">{tienda}</option>' for tienda in tiendas_unicas])

    sales_data = ''.join([f'<span id="sales-{row["date"]}-{row["store_nbr"]}" style="display:none;">{row["sales"]}</span>' 
                          for idx, row in stores.iterrows()])
    transactions_data = ''.join([f'<span id="transactions-{row["date"]}-{row["store_nbr"]}" style="display:none;">{row["transactions"]}</span>' 
                                 for idx, row in tabla_plot.iterrows()])

    return HTMLResponse(content=html_content.format(
        graph_sales=graph_sales,
        graph_transactions=graph_transactions,
        fechas_options=fechas_options,
        tiendas_options=tiendas_options
    ) + sales_data + transactions_data)

@app.post("/predict")
async def predict_sales(
    store_nbr: int = Form(...),
    onpromotion: int = Form(...), 
    weekday: int = Form(...),
    date: str = Form(...),
    payday: int = Form(...),
    is_weekend: int = Form(...)
):
    
    date_obj = pd.to_datetime(date)
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day

    
    fila_test1 = test_dataset_sales.iloc[random.randint(0, 28500)].copy()
    fila_test1['store_nbr'] = store_nbr
    fila_test1['family'] = random.randint(0, 32)  
    fila_test1['onpromotion'] = onpromotion  
    fila_test1['city'] = random.randint(0, 21)  
    fila_test1['state'] = random.randint(0, 15)  
    fila_test1['type'] = random.randint(0, 4)  
    fila_test1['cluster'] = random.randint(0, 16)  
    fila_test1['dcoilwtico'] = random.uniform(40, 50)  
    fila_test1['weekday'] = weekday
    fila_test1['year'] = year
    fila_test1['month'] = month
    fila_test1['day'] = day
    fila_test1['payday'] = payday
    fila_test1['is_weekend'] = is_weekend


    fila_test = fila_test1.values.reshape(1, -1)
    prediccion_fila = loaded_model_sales.predict(fila_test)


    return (str(prediccion_fila[0]) + " And the number of On promotion products were: " + str(fila_test1['onpromotion']))
