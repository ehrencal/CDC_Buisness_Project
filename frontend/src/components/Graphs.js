import React from "react";
import "../App.css";

/* Graph/Image */

const Graphs = ({ graphNumber }) => {
    return (
        <div className="graph">
            <span className="graph-text">Graph Number: {graphNumber}</span>
        </div>
    );
}

export default Graphs;