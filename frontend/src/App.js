import React from "react";
import "./App.css";
import PredictInput from "./components/PredictInput.js";

function App() {
  return (
    <div className="app">
      {/* Left side (Graph + Predict) */}
      <div className="left">
        {/* Graph/Image */}
        <div className="graph">
          <span className="graph-text">Graph / Image</span>
        </div>

        <PredictInput />
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