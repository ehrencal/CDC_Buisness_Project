import React, { useState, useEffect } from "react";
import "./App.css";
import PredictInput from "./components/PredictInput.js";
import Graphs from "./components/Graphs.js";
import information from "./imformation.json";

const App = () => {
  const [graphNumber, setGraphNumber] = useState(1);
  const [forecastData, setForecastData] = useState(null);
  const [columns, setColumns] = useState([]);
  const [info, setInfo] = useState(information["Space economy"])

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
  }, []);

  const handleDropdownChange = (event) => {
    const selectedColumn = event.target.value;
    setInfo(information[selectedColumn] || "No information available for this selection.");
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
          <span className="blob-text">{info}</span>
        </div>
      </div>
    </div>
  );
};

export default App;