import React, { useState } from "react";
import "../App.css";

/* Predict + Input */
const PredictInput = ({ setGraphNumber }) => {
    const [predictValue, setPredictValue] = useState(1);

    const handleSliderChange = (event) => {
        setPredictValue(event.target.value);
        setGraphNumber(event.target.value);
    };

    return (
        <div className="predict-input">
            <label className="predict-btn">{parseInt(predictValue)+1}</label>
            <input
            type="range"
            min="1"
            max="7"
            step="1"
            value={predictValue}
            className="input-slider"
            onChange={handleSliderChange}
            />
        </div>
    );
}

export default PredictInput;