from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    #return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/forecast')
def forecast():
    data = [10, 12, 15, 13, 16, 18, 20, 19, 22, 25, 23]
    index = pd.date_range(start='2012', periods=len(data), freq='Y')
    series = pd.Series(data, index=index)

    model = ARIMA(series, order=(4, 1, 1))
    model_fit = model.fit()
    forecast_steps = 10
    forecast = model_fit.forecast(steps=forecast_steps)

    # Forecast as JSON
    forecast_json = {
        "dates": forecast.index.strftime('%Y-%m-%d').tolist(),
        "values": forecast.tolist()
    }

    # Combine historical and forecast for smoother plot
    full_forecast = pd.concat([series[-1:], forecast])  # Add last point of actual series

    # Plot
    plt.figure(figsize=(10, 5))
    series.plot(label='Historical')
    full_forecast.plot(label='Forecast', style='--')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded_plot = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    response = {
        "forecast": forecast_json,
        "plot_base64": encoded_plot
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)