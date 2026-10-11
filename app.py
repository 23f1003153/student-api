# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
# ]
# ///

import csv
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow GET requests from any website (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Find the CSV next to this file
CSV_PATH = Path(__file__).parent / "q-fastapi.csv"


def load_students():
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        return [
            {"studentId": int(row["studentId"]), "class": row["class"].strip()}
            for row in csv.DictReader(f)
        ]


# Read the file once when the server starts
students = load_students()


@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    # No ?class=... given -> return everyone
    if not class_:
        return {"students": students}

    wanted = set(class_)
    # Go through students in CSV order, keep only the wanted classes
    return {"students": [s for s in students if s["class"] in wanted]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
