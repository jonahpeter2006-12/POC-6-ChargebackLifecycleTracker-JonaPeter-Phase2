# POC #6 — Chargeback Lifecycle Tracker

## Real Rails — Payments

An interactive intelligence dashboard that tracks payment disputes through the chargeback lifecycle, from transaction and dispute filing through chargeback, merchant response, representment, and final decision.

## Problem Statement

Chargeback information can become difficult to understand when individual dispute records, lifecycle stages, outcomes, and financial impact are viewed separately.

This proof of concept provides a single dashboard for understanding the current position of chargeback cases, identifying dispute patterns, tracking outcomes, and viewing financial losses.

## Objective

The purpose of this proof of concept is to transform chargeback case information into useful intelligence by showing:

- Chargeback lifecycle stages
- Dispute patterns
- Case outcomes
- Financial losses
- Current dispute positions
- Merchant evidence and representment status

## Working Features

- Chargeback lifecycle visualization
- Total case, transaction value, loss, and pending metrics
- Lifecycle stage counts
- Dispute reason distribution
- Chargeback case table
- Dispute reason filtering
- Current stage filtering
- Final outcome filtering
- Combined filters
- Dynamic summary metrics
- Dynamic lifecycle counts
- Dynamic dispute reason distribution
- Dynamic case table
- Empty/no-result state
- Frontend-to-backend data communication
- Backend unavailable error handling
- Browser refresh support
- Responsive/mobile layout
- Download Sample Data functionality
- Payment intelligence/context section

## Architecture Summary

The application uses a two-part architecture:

### Frontend

The frontend is implemented with Next.js and provides the interactive dashboard, filters, lifecycle visualization, case table, metrics, intelligence content, responsive presentation, and sample-data download.

### Backend

The backend is implemented with FastAPI and provides the chargeback and summary API endpoints used by the frontend.

### Data

The current proof of concept uses a synthetic chargeback dataset for demonstration and validation.

### Data Flow

```text
Synthetic Chargeback Data
          |
          v
      FastAPI Backend
          |
          | REST API
          v
      Next.js Frontend
          |
          v
 Interactive Intelligence Dashboard
 ## Setup and Run Instructions

### Prerequisites
- Node.js and npm for the frontend.
- Python for the FastAPI backend.

### Frontend Setup
1. Open a terminal in the `frontend` folder.
2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

4. Open `http://localhost:3000` in your browser.

### Backend Setup

1. Open a terminal in the `backend` folder.
2. Activate the project's Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt



## Screenshots
![alt text](<Screenshot 2026-10-15 211611.png>)
![alt text](<Screenshot 2026-10-15 211625.png>)
![alt text](<Screenshot 2026-10-15 211637.png>)



## AI Summary

AI assistance was used to support the development and documentation of this proof of concept. The application demonstrates a chargeback lifecycle dashboard using a synthetic dataset, with contextual payment intelligence from public sources.



## Future Enhancements

- Integrate validated real-world chargeback data where authorized.
- Add more detailed lifecycle and outcome analysis.
- Improve payment intelligence and dispute pattern identification.
- Expand automated testing and validation.
- Explore deployment and production-readiness improvements.

## Known Limitations

- Event-level chargeback records are synthetic and intended for proof-of-concept demonstration.
- Public sources provide contextual payment intelligence and are not the source of the synthetic case records.
- Production data integration and deployment readiness require separate validation.
- Backend setup and API configuration should be confirmed before handover.