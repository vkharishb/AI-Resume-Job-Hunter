# AI Resume Job Hunter

Production-oriented FastAPI + React application that parses a resume PDF, analyzes it with OpenAI, searches India-focused job boards, ranks opportunities, exports Excel, creates a Google Sheet, and emails the tracker.

## Features

- PDF upload or GitHub PDF URL input with GitHub blob-to-raw conversion
- `pdfplumber` resume extraction with validation and graceful API errors
- OpenAI GPT-4.1 recruiter analysis returning structured JSON
- India-only job search via Adzuna plus Greenhouse and Lever company boards
- Ranking using keyword match, skill overlap, experience overlap, ATS score, and role relevance
- Excel export with `pandas` and `openpyxl`
- Google Sheets creation and public share URL
- Gmail SMTP email with Excel attachment
- PostgreSQL persistence for resume metadata, job history, and processing logs
- Structured logging, CORS, rate limiting, Docker, APScheduler daily refresh hook
- React + Tailwind responsive UI with light/dark mode, spinner, results table, and Sheet link
- Pytest backend tests and Vitest React component test

## Project Structure

```text
resume-job-hunter/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── utils/
│   │   ├── prompts/
│   │   ├── database/
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Environment Variables

Copy the backend example file:

```bash
cd resume-job-hunter/backend
cp .env.example .env
```

Required for full production behavior:

- `OPENAI_API_KEY`: OpenAI API key. The app uses `OPENAI_MODEL=gpt-4.1`.
- `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`: Adzuna API credentials for India job search.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: One-line Google service account JSON with Sheets and Drive access.
- `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL`: Gmail SMTP credentials.
- `DATABASE_URL`: PostgreSQL async SQLAlchemy URL.

Without OpenAI credentials, the backend returns a deterministic fallback analysis so local wiring can still be tested. Without Google or SMTP credentials, those integrations are skipped and logged.

## Google Sheets Setup

1. Create a Google Cloud project.
2. Enable Google Sheets API and Google Drive API.
3. Create a service account and generate a JSON key.
4. Paste the complete JSON into `GOOGLE_SERVICE_ACCOUNT_JSON` as one line.
5. The app creates a spreadsheet and shares it as public read-only.

## Gmail App Password Setup

1. Enable 2-step verification on the sender Google account.
2. Create an App Password for Mail.
3. Set `SMTP_USERNAME` to the Gmail address and `SMTP_PASSWORD` to the app password.
4. The email subject is `Apply for the jobs` and the body is `Attached is your AI-generated job application tracker.`

## Local Development

Backend:

```bash
cd resume-job-hunter/backend
py -3.11 -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend dependencies are intended for Python 3.11, matching `backend/Dockerfile`.

Frontend:

```bash
cd resume-job-hunter/frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Docker Deployment

```bash
cd resume-job-hunter
cp backend/.env.example backend/.env
docker compose up --build
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000`  
Health check: `http://localhost:8000/health`

## API

`GET /health`

Returns service status.

`POST /analyze`

Multipart form fields:

- `email`: destination email
- `resume_pdf`: PDF file, mutually exclusive with `github_url`
- `github_url`: HTTPS GitHub PDF URL, mutually exclusive with `resume_pdf`

Response includes:

- `resume_id`
- `google_sheet_url`
- `excel_file`
- `jobs`
- `analysis_summary`

## Testing

Backend:

```bash
cd resume-job-hunter/backend
pytest
```

Frontend:

```bash
cd resume-job-hunter/frontend
npm test
```

## Job Source Notes

Adzuna is used as the broad live search source for India. Greenhouse and Lever do not provide a single global search API, so the app queries configured company boards through `GREENHOUSE_COMPANIES` and `LEVER_COMPANIES`. Wellfound does not expose a stable public jobs API suitable for server-side production scraping, so it is intentionally not scraped; add a licensed partner feed in `app/services/job_sources.py` if you obtain one.

## Deployment Guides

### AWS ECS Fargate

1. Build and push backend and frontend images to ECR.
2. Create an RDS PostgreSQL instance.
3. Store environment variables in AWS Secrets Manager.
4. Create ECS task definitions for backend and frontend.
5. Put the backend behind an internal or public Application Load Balancer target group.
6. Put the frontend behind an ALB or serve the built assets from S3 + CloudFront with `VITE_API_BASE_URL` pointing to the backend URL.
7. Configure CloudWatch logs and health checks on `/health`.

### EC2

1. Install Docker and Docker Compose.
2. Clone the repository and create `backend/.env`.
3. Set DNS and TLS with Nginx or Caddy.
4. Run `docker compose up -d --build`.
5. Back up the PostgreSQL volume or point `DATABASE_URL` to managed RDS.

### Render

1. Create a PostgreSQL database.
2. Create a Web Service for `backend` using the Dockerfile.
3. Set all backend environment variables in Render.
4. Create a Static Site for `frontend`; build command `npm install && npm run build`, publish directory `dist`.
5. Set `VITE_API_BASE_URL` to the backend service URL.

### Railway

1. Add PostgreSQL plugin.
2. Deploy backend from `backend/Dockerfile`.
3. Deploy frontend from `frontend/Dockerfile` or as a Vite static app.
4. Add environment variables and set `VITE_API_BASE_URL` to the backend domain.

## Production Hardening Checklist

- Replace `Base.metadata.create_all` with Alembic migrations before multi-team production use.
- Add persistent object storage for generated PDFs and Excel files.
- Add authenticated users if trackers should not be publicly accessible.
- Add a licensed Wellfound source or vendor job feed if that market coverage is required.
- Add observability dashboards for failed external integrations and processing latency.
