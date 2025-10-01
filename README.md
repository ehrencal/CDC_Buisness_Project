# 🚀 AstroIntel
AstroIntel is a launch control–style dashboard that visualizes the U.S. space economy and forecasts its future using time-series modeling.

## Inspiration  
We were interested in the outlook of jobs in the space industry and wanted to analyze a large government dataset to uncover which areas of the space economy are poised for the most growth.

## What It Does  
AstroIntel is a Mission Control dashboard that:

- Visualizes space economy metrics (jobs, value added, compensation, and output)
- Forecasts multi-year trends (1–3 years) using ARIMA time-series models
- Lets users explore different industries through dropdowns and sliders for quick insights

## How We Built It  
- **Backend:** Python (Flask) for data cleaning, ARIMA forecasting, and serving plots as JSON/PNG  
- **Frontend:** React + HTML/CSS for an interactive dashboard with industry dropdowns, horizon sliders, and Matplotlib-generated charts  

## Challenges We Ran Into  
- Getting the ARIMA model to properly generate stable forecasts for multiple industries  
- Connecting the frontend slider to dynamically request and display multi-year forecasts from the backend  

## Accomplishments That We’re Proud Of  
- Building a working full-stack prototype in 24 hours  
- Successfully integrating ARIMA forecasting to produce outlooks for multiple parts of the dataset  
- Designing a clean dashboard that makes complex economic data easy to explore  

## What’s Next for AstroIntel  
- Add insight-driven briefs to assist stakeholders in making data-informed decisions  
- Incorporate additional datasets to improve forecast accuracy and broaden coverage  
- Enhance the UI/UX with richer visualizations and comparison tools
