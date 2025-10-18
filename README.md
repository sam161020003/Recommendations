---
title: Ikarus3D AI Backend
emoji: 🚀
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 3.11
app_file: backend/main.py
pinned: false
---

# Ikarus3D AI Recommender Project

This Space hosts the FastAPI backend for the Ikarus3D product recommender.

AI-Powered Multimodal Furniture Recommendation App

This project is a full-stack web application that serves as an intelligent furniture recommendation system. It leverages a combination of Computer Vision and Natural Language Processing to provide users with a conversational search experience, complemented by a data analytics dashboard.

## Features

* **Conversational Search**: Users can type natural language queries (e.g., "a modern leather sofa for a large living room") to find relevant products.
* **Multimodal Embeddings**: The recommendation engine is powered by CLIP embeddings, which combine both the product's text description and its primary image for a richer, more accurate search.
* **Generative AI Descriptions**: Users can generate new, creative product descriptions on-the-fly using **Google's Gemini-Pro model**.
* **Vector Search**: A Pinecone vector database is used for highly efficient, real-time similarity searches.
* **Data Analytics Dashboard**: A separate page visualizes key insights from the product dataset, including top brands, materials, and countries of origin, using interactive charts.

## Tech Stack

**Backend:** FastAPI, Uvicorn

**Frontend:** React, React Router, Axios, Tailwind CSS

**Vector Database:** Pinecone

**ML/AI:**
* **Embedding Model:** `sentence-transformers/clip-ViT-B-32`
* **Generative LLM:** `google/gemini-pro`
* **Integration Framework:** LangChain, Google AI

**Data Processing:** Pandas, Jupyter

**Visualization:** Recharts

## Project Structure
├── backend/ # FastAPI application │ ├── .env # Secret keys (PINECONE, GOOGLE) │ ├── main.py # Main API logic │ └── requirements.txt # Backend dependencies ├── frontend/ # React application │ ├── src/ │ └── package.json ├── data_analytics.ipynb # Notebook for data cleaning and visualization ├── model_training.ipynb # Notebook for generating and uploading embeddings └── README.md # This file


## Setup and Installation

### Prerequisites

* Python 3.9+
* Node.js and npm
* A free Pinecone account
* A Google AI API key (from Google AI Studio)

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
2. Backend Setup
Bash

# Navigate to the backend folder
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your API keys
# (Create this file manually in the 'backend' folder)
PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
3. Frontend Setup
Bash

# Navigate to the frontend folder
cd ../frontend

# Install dependencies
npm install
4. Data and Model Setup
Before running the application, you need to process the data and populate the vector database.

Run the data_analytics.ipynb notebook to generate the analytics_output.json file (and move it into the backend folder).

Run the model_training.ipynb notebook to generate embeddings and upload them to your Pinecone index.

Running the Application
You need to have two terminals open to run the backend and frontend servers simultaneously.

Terminal 1: Start the Backend
Bash

cd backend
source venv/bin/activate
uvicorn main:app --reload
The backend will be running at http://127.0.0.1:8000.

Terminal 2: Start the Frontend
Bash

cd frontend
npm start
The React app will open in your browser at http://1.0.0.1:3000.