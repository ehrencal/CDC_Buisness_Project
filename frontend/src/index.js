import React from 'react';
import ReactDOM from 'react-dom/client'; // For React 18+
import App from './App'; // Import your main App component

// Create a root for React 18+
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render your App component into the 'root' element in index.html
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);