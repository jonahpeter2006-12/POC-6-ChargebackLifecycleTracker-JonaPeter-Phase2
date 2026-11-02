# UAT Checklist — POC #6 Chargeback Lifecycle Tracker

## Project Information

- Name: Jona Peter
- GitHub Username: jonahpeter2006-12
- PoC Number: 6
- PoC Title: Chargeback Lifecycle Tracker
- Rail: Payments

## Functional Testing

| Test | Result |
|---|---|
| Dashboard loads successfully | PASS |
| FastAPI backend starts successfully | PASS |
| Next.js frontend starts successfully | PASS |
| `/api/summary` returns correct data | PASS |
| `/api/chargebacks` returns chargeback records | PASS |
| Reason filter works | PASS |
| Stage filter works | PASS |
| Outcome filter works | PASS |
| Combined filters work | PASS |
| Dynamic summary metrics update | PASS |
| Lifecycle counts update | PASS |
| Dispute reason distribution updates | PASS |
| Case table updates | PASS |
| Intelligence sidebar updates | PASS |
| Empty/no-result state works | PASS |
| Browser refresh works | PASS |
| Filtered state works after refresh | PASS |

## Backend Validation

### Summary Endpoint

Expected:

- Total cases: 6
- Total transaction amount: 985.49
- Total loss: 215.00
- Won cases: 2
- Lost cases: 2
- Pending cases: 2

Result: PASS

### Chargeback Endpoint

The endpoint returns six synthetic chargeback records:

- CB001
- CB002
- CB003
- CB004
- CB005
- CB006

Result: PASS

## Filter Validation

### Fraudulent Transaction + Chargeback

Expected:
- 1 case
- CB006
- Transaction value: $150.25
- Loss: $150.25

Result: PASS

### Lost Outcome

Expected:
- 2 cases
- CB004
- CB006
- Transaction value: $215.00
- Total loss: $215.00

Result: PASS

### Zero-Result Combination

A filter combination producing no matching records was tested.

Expected behavior:
- Metrics become zero
- Lifecycle counts become zero
- Distribution shows no matching data
- Case table shows no matching records

Result: PASS

## Frontend-Backend Communication

The Next.js frontend successfully receives chargeback data from the FastAPI backend.

Result: PASS

## Data Integrity

The values displayed in the dashboard match the synthetic JSON dataset and API responses.

Result: PASS

## Refresh Validation

The dashboard was refreshed while filters were active and continued to display the correct filtered data.

Result: PASS

## UAT Result

**PASS**

The current implementation satisfies the tested Phase 1 functional requirements.

## Known Limitations
## Additional Phase 1 Validation

| Test | Result |
|---|---|
| Tooltip behavior verified | PASS |
| Loading state verified | PASS |
| Backend unavailable error state verified | PASS |
| Normal operation after backend restart verified | PASS |
| Browser console checked after recovery | PASS |
| Mobile/responsive layout verified | PASS |
| Download Sample Data action verified | PASS |
| Downloaded JSON contains all 6 chargeback cases | PASS |

## Error Handling Validation

The FastAPI backend was intentionally stopped to verify frontend behavior when the API is unavailable.

Expected behavior:

- Dashboard displays a clear unable-to-load message.
- User is instructed to ensure the FastAPI backend is running.
- No application crash occurs.

Result: PASS

The FastAPI backend was then restarted and the dashboard successfully recovered. The previous `Failed to fetch` console error was no longer present during normal operation.

Result: PASS

## Download Validation

The Download Sample Data action was tested successfully.

The downloaded JSON file contained all six synthetic chargeback cases:

- CB001
- CB002
- CB003
- CB004
- CB005
- CB006

Result: PASS

## Responsive Validation

The dashboard was tested using browser mobile/device emulation.

The interface remained usable with vertically stacked sections, readable content, accessible filters, and no major overlapping elements.

Result: PASS
The event-level chargeback dataset is synthetic and is intended for proof-of-concept demonstration.

Public sources provide contextual payment intelligence and are not represented as the source of the synthetic case records.
## Phase 2 - Docker Local Validation

| Test | Result |
|---|---|
| Backend Docker image builds successfully | PASS |
| Frontend Docker image builds successfully | PASS |
| Docker Compose starts both containers | PASS |
| Backend API accessible through host port 8001 | PASS |
| Frontend accessible through host port 3001 | PASS |
| Dashboard loads chargeback records inside Docker | PASS |
| Dashboard filters and case details work inside Docker | PASS |
| Both containers restart successfully | PASS |
| Dashboard remains accessible after container restart | PASS |

### Docker Configuration

- Backend container: `chargeback-backend`
- Frontend container: `chargeback-frontend`
- Backend mapping: `8001:8000`
- Frontend mapping: `3001:3000`
- Orchestration: Docker Compose

### Phase 2 Local Validation Result

**PASS - Local Docker validation completed.**

Both containers were successfully built, started, tested, and restarted. The frontend successfully communicates with the FastAPI backend, and the dashboard displays the six synthetic chargeback records.

Cloud deployment and production validation have not yet been performed.