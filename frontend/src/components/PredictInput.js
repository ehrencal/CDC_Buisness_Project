import React, { useState } from "react";
import "../App.css";

/* Predict + Input */
function PredictInput() {
    const [predictValue, setPredictValue] = useState(0);

    const handleSliderChange = (event) => {
        setPredictValue(event.target.value);
    };

    return (
        <div className="predict-input">
            <label className="predict-btn">{predictValue}</label>
            <input
            type="range"
            min="0"
            max="11"
            step="1"
            value={predictValue}
            className="input-box"
            onChange={handleSliderChange}
            />
        </div>
    );
}

export default PredictInput;