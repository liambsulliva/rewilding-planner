# Rewilding Planner

This project is a web application that generates a random ecosystem on a grid, featuring trees, water, and animals. It's built using Svelte for the frontend and Flask for the backend. Although we couldn't implement all the features in time, it was a very fulfilling project! This is submitted for the Eaton Sustainability for AI track.

[Live View](https://rewilding-project-wine.vercel.app) (Frontend Only)

[Video Demo](https://www.youtube.com/watch?v=IkalxMRn_rk)

## Features

- Random generation of trees, water, and animals on a grid
- Frontend built with Svelte
- Backend API using Flask
- BMP file integration (planned feature)

## Project Structure

```
rewilding-project/
├── frontend/
│   ├── src/
│   │   ├── App.svelte
│   │   ├── app.css
│   │   └── ...
│   ├── public/
│   └── package.json
├── backend/
│   ├── process.py
│   ├── firsttake.bmp
│   └── ...
└── README.md
```

## Setup and Installation

### Frontend (Svelte)

1. Navigate to the `frontend` directory
2. Install dependencies:
   ```
   npm install
   ```
3. Run the development server:
   ```
   npm run dev
   ```

### Backend (Flask)

1. Navigate to the `backend` directory
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```
   flask run
   ```

## Usage

Open your browser and navigate to `http://localhost:5000` to view the flask application, and `http://localhost:5173`. When opening the frontend, the grid will be populated with randomly generated trees, water, and animals.

## Planned Features

- Import ecosystem recommendations from a BMP file sent from the backend
- Export the current map state as a BMP file to the backend

Scoring Functions:
Carbon Capture(kg) = .5kg per pound of tree and bush
1 bmp pixel = 3cm^2
Tree weight(Spruce) = 1.9kg per 3cm^2
Bush weight(Hemlock) = 1.6kg per 3cm^2
Biodiversity= Difference from 4open:1water:1 shaded ratio
Bush Count= (Biodiversity score-.2)\*Open Space Available
