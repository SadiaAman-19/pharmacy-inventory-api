import sqlite3
from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

DB_FILE = "pharmacy.db"
app = FastAPI(title="Pharmacy Inventory API")


# ---------- Database ----------
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS medicines (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                batchNo    TEXT    NOT NULL UNIQUE,
                category   TEXT    NOT NULL,
                price      REAL    NOT NULL CHECK (price > 0),
                quantity   INTEGER NOT NULL CHECK (quantity >= 0),
                expiryDate TEXT    NOT NULL
            )"""
        )


init_db()


# ---------- Validation model ----------
class Medicine(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    batchNo: str = Field(min_length=1, max_length=50)
    category: Literal["Tablet", "Syrup", "Injection", "Capsule", "Ointment"]
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    expiryDate: date

    @field_validator("expiryDate")
    @classmethod
    def expiry_must_be_future(cls, v: date):
        if v <= date.today():
            raise ValueError("expiryDate must be a future date")
        return v


# ---------- Error handling ----------
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(status_code=400, content={"error": "Validation failed", "details": errors})


def row_to_dict(row):
    return dict(row)


def get_or_404(conn, med_id: int):
    row = conn.execute("SELECT * FROM medicines WHERE id = ?", (med_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Medicine with id {med_id} not found")
    return row


def values(m: Medicine):
    return (m.name, m.batchNo, m.category, m.price, m.quantity, m.expiryDate.isoformat())


# ---------- CRUD endpoints ----------
@app.post("/api/medicines", status_code=201)
def create_medicine(m: Medicine):
    try:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO medicines (name, batchNo, category, price, quantity, expiryDate) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                values(m),
            )
            row = conn.execute("SELECT * FROM medicines WHERE id = ?", (cur.lastrowid,)).fetchone()
        return row_to_dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail=f"batchNo '{m.batchNo}' already exists")


@app.get("/api/medicines")
def get_all_medicines():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM medicines ORDER BY id").fetchall()
    return [row_to_dict(r) for r in rows]


@app.get("/api/medicines/{med_id}")
def get_medicine(med_id: int):
    with get_conn() as conn:
        return row_to_dict(get_or_404(conn, med_id))


@app.put("/api/medicines/{med_id}")
def update_medicine(med_id: int, m: Medicine):
    try:
        with get_conn() as conn:
            get_or_404(conn, med_id)
            conn.execute(
                "UPDATE medicines SET name=?, batchNo=?, category=?, price=?, quantity=?, "
                "expiryDate=? WHERE id=?",
                values(m) + (med_id,),
            )
            row = conn.execute("SELECT * FROM medicines WHERE id = ?", (med_id,)).fetchone()
        return row_to_dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail=f"batchNo '{m.batchNo}' already exists")


@app.delete("/api/medicines/{med_id}")
def delete_medicine(med_id: int):
    with get_conn() as conn:
        get_or_404(conn, med_id)
        conn.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
    return {"message": f"Medicine with id {med_id} deleted successfully"}