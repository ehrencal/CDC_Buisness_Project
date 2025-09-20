import React from "react";
import "../App.css";

/* Graph/Image */

const Graphs = ({ forecastImage }) => {
    return (
        <div className="graph">
            {forecastImage}
        </div>
    );
}

export default Graphs;