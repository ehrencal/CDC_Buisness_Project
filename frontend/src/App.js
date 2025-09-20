import React, { useState, useEffect } from "react";
import "./App.css";
import PredictInput from "./components/PredictInput.js";
import Graphs from "./components/Graphs.js";

const App = () => {
  const info = require("./imformation.json");
  const [graphNumber, setGraphNumber] = useState(1);
  const [forecastData, setForecastData] = useState(null);
  const [columns, setColumns] = useState([]);
  const [information, setInformation] = useState("This column represents the year of observation. Each row corresponds to a calendar year and provides real gross output values for the different industries and sectors listed in the dataset. The values in this column establish the time series structure of the dataset.");

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
  };

  useEffect(() => {
    // Fetch forecast data
    fetch("http://localhost:5000/forecast")
      .then(response => response.json())
      .then(data => setForecastData(data))
      .catch(error => console.error("Error fetching data:", error));

    // Fetch column names
    fetch("http://localhost:5000/getColumns")
      .then(response => response.json())
      .then(data => setColumns(data))
      .catch(error => console.error("Error fetching columns:", error));

    fetch("/imformation.json")
      .then(response => response.json())
      .then(data => setInformation(data))
      .catch(error => console.error("Error fetching information:", error));
  }, []);

  const handleDropdownChange = (event) => {
    const selectedColumn = event.target.value;
    setInformation(info[selectedColumn] || "No information available for this selection.");
    // Fetch new forecast data based on selected column
    fetch(`http://localhost:5000/forecast?column=${encodeURIComponent(selectedColumn)}`)
      .then(response => response.json())
      .then(data => setForecastData(data))
      .catch(error => console.error("Error fetching data:", error));
  }

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
        <PredictInput setGraphNumber={setGraphNumber} />
      </div>

      {/* Right side (Dropdown + Blob) */}
      <div className="right">
        {/* Dropdown */}
        <select 
          className="dropdown"
          onChange={(e) => handleDropdownChange(e)}
        >
          {columns.map((col, index) => (
            <option key={index} value={col}>{col.trim()}</option>
          ))}
        </select>

        {/* Blob Box */}
        <div className="blob">
          <span className="blob-text">{information}</span>
        </div>
      </div>
    </div>
  );
};

export default App;