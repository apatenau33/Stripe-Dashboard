from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from database import get_connection, count_payments

app = FastAPI(title="Stripe Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/payments")
def list_payments(
    start: str | None = Query(None, description="ISO date, inclusive"),
    end: str | None = Query(None, description="ISO date, inclusive"),
    limit: int = Query(100, le=500),
):
    sql = "SELECT * FROM payments WHERE 1=1"
    params = []

    if start:
        sql += " AND created_at >= ?"
        params.append(start)
    if end:
        sql += " AND created_at <= ?"
        params.append(end + "T23:59:59")

    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()

    return [dict(row) for row in rows]


@app.get("/api/summary")
def summary():
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*)                                  AS transactions,
                COALESCE(SUM(amount), 0)                  AS gross,
                COALESCE(AVG(amount), 0)                  AS average,
                MAX(synced_at)                            AS last_synced
            FROM payments
            WHERE status = 'succeeded'
            """
        ).fetchone()

    return {**dict(row), "total_records": count_payments()}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", reload=True)