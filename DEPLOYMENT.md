# Deployment Guide

This project is split into two deployments:

- Backend: FastAPI on Railway
- Frontend: Vite static app on Vercel

## Backend on Railway

1. Push this repository to GitHub.
2. In Railway, create a new project from the GitHub repository.
3. Keep the Railway service root at the repository root.
4. Railway will use `railway.toml`, which points to the root `Dockerfile`.
5. Add these Railway variables:

```bash
GROQ_API_KEY=your_groq_key
GROQ_API_BASE=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
EMBEDDINGS_MODEL=local-hash-embedding
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
```

Railway injects `PORT` automatically. The backend start script binds to that port.

After deployment, verify:

```bash
https://your-railway-backend.up.railway.app/health
https://your-railway-backend.up.railway.app/docs
```

### Railway Build Troubleshooting

If Railway logs show `using build driver railpack` and `Railpack could not determine how to build the app`, Railway did not receive `railway.toml` and the root `Dockerfile`.

Fix it by committing and pushing these root files:

```bash
git add Dockerfile railway.toml DEPLOYMENT.md
git add backend/start.sh backend/requirements.txt backend/pyproject.toml backend/app
git commit -m "Add Railway backend deployment config"
git push
```

Then redeploy the Railway service from the latest commit.

Alternative fix: set the Railway service root directory to `backend` and use:

```bash
Start Command: sh start.sh
Healthcheck Path: /health
```

The recommended setup is still the root `railway.toml` plus root `Dockerfile`, because it keeps the monorepo deployment explicit.

## Frontend on Vercel

1. Create a Vercel project from the same GitHub repository.
2. Set the Vercel root directory to `frontend`.
3. Use these build settings:

```bash
Build Command: npm run build
Output Directory: dist
Install Command: npm ci
```

4. Add this Vercel environment variable:

```bash
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app/api/v1
```

5. Deploy the frontend.
6. Copy the Vercel production domain and update Railway:

```bash
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
```

Then redeploy the Railway backend so CORS uses the final frontend domain.

## Local Production Check

Before deploying, run:

```bash
cd frontend
npm run build
```

```bash
cd backend
python -m pytest
```
