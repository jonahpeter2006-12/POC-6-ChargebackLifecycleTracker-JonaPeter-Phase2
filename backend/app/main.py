from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

app = FastAPI(
    title="Chargeback Lifecycle Tracker API",
    description="Backend API for Real Rails PoC #6",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
  allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "https://poc6-chargeback-frontend.onrender.com",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATA_FILE = Path(__file__).parent.parent / "data" / "mock_data.json"


def load_chargeback_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/")
def root():
    return {
        "message": "Chargeback Lifecycle Tracker API is running",
        "data_source": "Synthetic mock data"
    }


@app.get("/api/chargebacks")
def get_chargebacks():
    return load_chargeback_data()


@app.get("/api/summary")
def get_summary():
    cases = load_chargeback_data()

    total_cases = len(cases)
    total_amount = sum(case["amount"] for case in cases)
    total_loss = sum(case["loss_amount"] for case in cases)
    won_cases = sum(1 for case in cases if case["final_outcome"] == "Won")
    lost_cases = sum(1 for case in cases if case["final_outcome"] == "Lost")
    pending_cases = sum(
        1 for case in cases if case["final_outcome"] == "Pending"
    )

    return {
        "total_cases": total_cases,
        "total_transaction_amount": round(total_amount, 2),
        "total_loss": round(total_loss, 2),
        "won_cases": won_cases,
        "lost_cases": lost_cases,
        "pending_cases": pending_cases
    }