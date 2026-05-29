# TODO

- [x] Confirm the backend crash is due to missing `pydantic_settings` dependency (from logs).
- [x] Update `backend/Dockerfile` to install dependencies deterministically from `requirements.txt` and fail build if `pydantic_settings` import fails.
- [x] Rebuild the backend Docker image.
- [x] Redeploy to Railway.
- [ ] Verify container starts successfully and `uvicorn` serves the app.
