from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use
use('Agg')  
import io
import base64
import forcasts
import dataframes

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    #return render_template('index.html')
    return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/forecast')
def forcastYears():
    plots = []
    for i in range(1, 11):
        plots.append(forcastRoute(column="Space economy",length=i))
    return jsonify(plots)

def forcastRoute(column, length):
    return forcasts.forecast(dataframes.real_output_df, column, length, (6,1,1))

if __name__ == '__main__':
    app.run(debug=True)