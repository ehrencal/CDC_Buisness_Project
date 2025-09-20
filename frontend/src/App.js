import React, { useState, useEffect } from "react";
import "./App.css";
import PredictInput from "./components/PredictInput.js";
import Graphs from "./components/Graphs.js";

const App = () => {
  const [graphNumber, setGraphNumber] = useState(2);
  const [forecastData, setForecastData] = useState(null);

  const parseForecastImage = (data, altText = "Forecast Plot") => {
    if (!data || !data.plot_base64) {
      return <p>No image available.</p>;
    }

    return (
      <img
        src={`data:image/png;base64,${data.plot_base64}`}
        alt={altText}
        style={{ maxWidth: "100%", border: "1px solid #ccc", borderRadius: "8px" }}
      />
    );
  }


  useEffect(() => {
    fetch("http://localhost:5000/forecast")
      .then(response => response.json())
      .then(data => setForecastData(data))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="app">
      {/* Left side (Graph + Predict) */}
      <div className="left">
        <Graphs
          forecastImage={
            Array.isArray(forecastData) && forecastData.length > graphNumber
              ? parseForecastImage(forecastData[graphNumber])
              : <p>Loading...</p>
          }
        />
        <PredictInput 
          setGraphNumber={setGraphNumber}
        />
      </div>

      {/* Right side (Dropdown + Blob) */}
      <div className="right">
        {/* Dropdown */}
        <select className="dropdown">
          <option>ARIMA Forecast</option>
          <option>Option 2</option>
          <option>Option 3</option>
        </select>

        {/* Blob Box */}
        <div className="blob">
          <span className="blob-text">Very helpful information</span>
        </div>
      </div>
    </div>
  );
}

export default App;