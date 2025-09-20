from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import forcasts
import dataframes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    #return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/forecast')
def forcastYears():
    plots = []
    for i in range(11):
        plots.append(forcastRoute(column="Space economy1",length=10))
    return plots

def forcastRoute(column, length):
    return forcasts.forecast(dataframes.real_output_df, column, length, (5,1,1))

if __name__ == '__main__':
    app.run(debug=True)