import React, { useState } from "react";
import "./App.css";
import PredictInput from "./components/PredictInput.js";
import Graphs from "./components/Graphs.js";

const App = () => {
  const [graphNumber, setGraphNumber] = useState(0);

  return (
    <div className="app">
      {/* Left side (Graph + Predict) */}
      <div className="left">
        <Graphs 
          graphNumber={graphNumber}
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