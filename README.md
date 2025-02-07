# Agience CookieMaps

## Overview
Agience CookieMaps is an AI-powered cryptocurrency data visualization platform developed by Agience AI. It simplifies crypto market analysis through advanced clustering, AI-driven insights, and real-time data visualization. Our mission is to make cryptocurrency trading and investment more intuitive, data-driven, and accessible to all users.

## Features
- **AI-Driven Market Analysis** – Uses machine learning models to classify and cluster cryptocurrencies.
- **Dynamic Clustering** – Organizes cryptocurrencies into visually interactive groups based on market trends.
- **Real-Time Data Visualizations** – Provides insights from CookieDAO’s DataSwarm API, including social sentiment and trading activity.
- **AI Chatbot Assistance** – Natural Language Processing (NLP)-powered chatbot to help users understand market movements.
- **User-Friendly Interface** – Designed for novice traders and experienced investors alike.
- **Portfolio Tracking & Insights** – Analyze, track, and optimize crypto portfolios.

## Installation
### Clone the repository:
```sh
git clone https://github.com/ikailo/agience-cookiemaps.git
```
### Navigate into the project folder:
```sh
cd agience-cookiemaps
```
### Open the project files in your preferred code editor.

### Run the backend using Python:
```sh
python app.py
```
### Open the `index.html` file in a web browser to access the platform.

## Running with Docker
To run CookieMaps using Docker, use the following commands:

### Build the Docker image:
```sh
docker build -t agience-cookiemaps .
```
### Run the Docker container:
```sh
docker run -p 8000:8000 agience-cookiemaps
```
The application will be available at `http://localhost:8000/`.

## Usage
- Open the application in your browser.
- Explore AI-driven insights and market data visualizations.
- Utilize AI-powered chatbot assistance for cryptocurrency explanations.
- Make informed trading and investment decisions based on **CookieDAO API** data.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask/FastAPI)
- **AI & Analytics**: OpenAI models, CookieDAO DataSwarm API, K-means clustering
- **Deployment**: Docker, AWS EC2

## License
This project is licensed under the **AGPL-3.0 License**.

