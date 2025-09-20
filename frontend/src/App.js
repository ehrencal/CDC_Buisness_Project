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

  const getColumns = () => {
    let return_data;
    fetch("http://localhost:5000/getColumns")
      .then(response => response.json())
      .then(data => return_data = data)
      .catch(error => console.error("Error fetching columns:", error));
    return return_data;
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
          {getColumns() && getColumns().map((col, index) => (
            <option key={index} value={col}>{col}</option>
          ))}
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