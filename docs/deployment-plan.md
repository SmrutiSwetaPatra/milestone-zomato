# Deployment Plan

This document outlines the step-by-step process for deploying the Zomato Milestone application. The deployment will be split into two parts: the FastAPI backend will be hosted on **Railway**, and the static frontend will be hosted on **Vercel**.

## 1. Backend Deployment (Railway)

The backend is built with FastAPI. Railway is an excellent platform for deploying Python web services as it can automatically detect standard Python environments.

### Prerequisites & Preparation
Before deploying, we need to make a few modifications to the backend codebase to support a decoupled architecture.

1. **Enable CORS (Cross-Origin Resource Sharing):**
   Since the frontend will be hosted on a different domain (Vercel), the backend must explicitly allow requests from it. We need to add `CORSMiddleware` to `main.py`.
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"], # In production, restrict this to the Vercel domain
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Add a Procfile (Optional but Recommended):**
   Create a `Procfile` at the root of the project to tell Railway exactly how to start the FastAPI server:
   ```text
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Database Considerations (Important):**
   The application uses a local SQLite database (`data/zomato.db`). Railway uses an ephemeral filesystem, meaning if the app restarts, any new data written to the database will be lost. If the database is strictly read-only, this is fine. If it requires write operations, we should migrate to a managed PostgreSQL database provided by Railway.

4. **Environment Variables:**
   Ensure any keys in the `.env` file (like `GROQ_API_KEY`) are kept secret and are configured directly in the Railway dashboard.

### Deployment Steps
1. Push the latest code to your GitHub repository.
2. Log in to [Railway](https://railway.app/) and click **New Project** -> **Deploy from GitHub repo**.
3. Select the `milestone-zomato` repository.
4. Go to the project's **Variables** tab in Railway and add the required environment variables (e.g., `GROQ_API_KEY`).
5. Wait for the build to complete.
6. Once deployed, go to the **Settings** tab -> **Networking** -> **Generate Domain** to get the public URL for your backend API (e.g., `https://milestone-zomato-production.up.railway.app`).

---

## 2. Frontend Deployment (Vercel)

The frontend is a static site (HTML, JS, CSS) currently living in the `frontend/` directory. Vercel is highly optimized for deploying static sites.

### Prerequisites & Preparation
1. **Update API Endpoints:**
   In `frontend/app.js`, the API requests are likely using relative paths (e.g., `/locations`). Now that the backend is separated, these need to point to the new Railway backend URL.
   - Example change:
     ```javascript
     // Before
     const response = await fetch('/locations');
     
     // After
     const API_BASE_URL = 'https://milestone-zomato-production.up.railway.app'; // Replace with actual Railway URL
     const response = await fetch(`${API_BASE_URL}/locations`);
     ```

### Deployment Steps
1. Log in to [Vercel](https://vercel.com/) and click **Add New...** -> **Project**.
2. Import the `milestone-zomato` GitHub repository.
3. **Configure the Project:**
   - Framework Preset: **Other** (since it's purely static HTML/JS)
   - Root Directory: **frontend** (This tells Vercel to only serve the files inside the `frontend/` folder)
4. Click **Deploy**.
5. Once complete, Vercel will provide a public URL for your frontend application (e.g., `https://milestone-zomato.vercel.app`).

---

## 3. Post-Deployment Verification

1. Open the Vercel URL in your browser.
2. Check the browser console (`F12` -> Console) to ensure there are no CORS errors.
3. Test the application workflows to verify that the frontend correctly communicates with the Railway backend and that predictions/data fetching work as expected.
