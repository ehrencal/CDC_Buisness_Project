from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64



def forecast(df, column_name, forecast_steps=5, arima_order=(1, 1, 1)):
    """
    Forecasts future values of a specified time series column from a DataFrame using ARIMA.
    
    Args:
        df (pd.DataFrame): Time-indexed DataFrame.
        column_name (str): Name of the column to forecast.
        forecast_steps (int): How many steps ahead to forecast.
        arima_order (tuple): ARIMA(p,d,q) order.
    
    Returns:
        JSON: Forecast data and base64 plot image.
    """
    # 1. Ensure the column exists and is numeric
    if column_name not in df.columns:
        return {"error": f"Column '{column_name}' not found in DataFrame."}
    series = pd.to_numeric(df[column_name], errors='coerce').dropna()

    # 2. Fit ARIMA model
    model = ARIMA(series, order=arima_order)
    model_fit = model.fit()

    # 3. Forecast
    forecast = model_fit.forecast(steps=forecast_steps)

    # 4. Smooth connection (prevent gap in plot)
    full_forecast = pd.concat([series[-1:], forecast])

    # 5. Plot historical + forecast
    plt.figure(figsize=(10, 5))
    series.plot(label='Historical')
    full_forecast.plot(label='Forecast', style='--')
    plt.title(f"{column_name} Forecast")
    plt.legend()
    plt.grid(True)

    # 6. Save plot as base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded_plot = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # 7. Return forecast as JSON
    forecast_json = {
        "dates": forecast.index.tolist(),
        "values": forecast.tolist()
    }

    return {
        "forecast": forecast_json,
        "plot_base64": encoded_plot
    }