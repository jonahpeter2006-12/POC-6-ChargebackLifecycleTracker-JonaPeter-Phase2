# PoC-6: Chargeback Lifecycle Tracker

**Infocreon Internship | Phase 2 – Local-to-Cloud Mirroring Preparation**

## 1. Project Overview

The Chargeback Lifecycle Tracker is a web-based analytics dashboard designed to monitor payment disputes throughout their lifecycle.

The application displays synthetic chargeback records, dispute statuses, transaction amounts, financial losses, and case-level details through an interactive dashboard.

Phase 2 focuses on containerizing the application and validating its functionality in a local Docker environment.

## 2. Phase 2 Objectives

- Containerize the FastAPI backend.
- Containerize the Next.js frontend.
- Configure Docker Compose for application orchestration.
- Maintain frontend-to-backend communication.
- Validate dashboard functionality inside Docker containers.
- Prepare the application for future cloud deployment.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Backend | Python, FastAPI |
| API Server | Uvicorn |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Data Source | Synthetic JSON data |
| Version Control | Git and GitHub |

## 4. Project Structure

```text
POC-6-ChargebackLifecycleTracker-JonaPeter-Phase2/
├── backend/
│   ├── app/
│   ├── data/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── README.md
├── docker-compose.yml
├── UAT_CHECKLIST.md
├── VAR_REPORT.md
└── README.md
```

## 5. Application Architecture

The application uses two Docker containers:

- **Frontend:** Next.js application running on port 3000 inside the container.
- **Backend:** FastAPI application running on port 8000 inside the container.

Docker Compose manages both services.

| Service | Host Port | Container Port |
|---|---:|---:|
| Frontend | 3001 | 3000 |
| Backend | 8001 | 8000 |

## 6. Setup and Execution

### Prerequisites

- Docker Desktop
- Git
- A modern web browser

### Start the application

From the project root, run:

```powershell
docker compose up --build -d
```

### Check container status

```powershell
docker compose ps
```

### Stop the application

```powershell
docker compose down
```

## 7. Application URLs

- **Dashboard:** http://localhost:3001
- **Backend API:** http://localhost:8001
- **API documentation:** http://localhost:8001/docs

## 8. API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Backend status message |
| `/api/chargebacks` | Returns chargeback records |
| `/api/summary` | Returns dashboard summary metrics |
| `/docs` | FastAPI interactive API documentation |

## 9. Local Docker Validation

The following tests were completed successfully:

| Validation Test | Result |
|---|---|
| Backend Docker image build | PASS |
| Frontend Docker image build | PASS |
| Docker Compose startup | PASS |
| Backend API accessibility | PASS |
| Frontend dashboard accessibility | PASS |
| Chargeback data retrieval | PASS |
| Dashboard filters | PASS |
| Case-level details | PASS |
| Container restart | PASS |
| Dashboard availability after restart | PASS |

### Dashboard Summary

| Metric | Validated Value |
|---|---:|
| Total Cases | 6 |
| Transaction Amount | $985.49 |
| Total Loss | $215.00 |
| Won Cases | 2 |
| Lost Cases | 2 |
| Pending Cases | 2 |

## 10. Screenshots

Three dashboard screenshots are available in the `frontend/` directory:

- `Screenshot 2026-10-15 211611.png`
- `Screenshot 2026-10-15 211625.png`
- `Screenshot 2026-10-15 211637.png`

## 11. Current Limitations

- The application uses synthetic mock data.
- No live payment gateway integration is configured.
- No production database is connected.
- Cloud deployment has not yet been performed.

## 12. Future Enhancements

- Deploy the frontend and backend to a cloud environment.
- Configure cloud networking and environment variables.
- Introduce persistent database storage.
- Integrate authorized payment dispute data.
- Perform cloud deployment and visualization validation.

## 13. Phase 2 Completion Status

**Local Docker Validation: PASSED**

The frontend and backend have been successfully containerized and tested locally using Docker Compose.

The Phase 2 source code and documentation have been committed and pushed to GitHub.

Cloud deployment and production validation remain pending.

---

**Project:** PoC-6 Chargeback Lifecycle Tracker  
**Organization:** Infocreon Internship  
**Phase:** Phase 2 – Local-to-Cloud Mirroring Preparation