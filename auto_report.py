import psycopg2
import requests
import jwt
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")


def get_connection():
    
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),  # no DNS force
        port=os.getenv("POSTGRES_PORT"),
        sslmode="require"
    )


def auto_generate_and_get_reports_from_token(token: str, express_url: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        if not user_id:
            raise ValueError("Missing user ID in token")
    except Exception as e:
        print("[JWT DECODE ERROR]:", e)
        return {"error": "Invalid token"}, 403

    month_now = datetime.now().strftime("%Y-%m")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_reports (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            month TEXT,
            total_spent NUMERIC,
            top_category TEXT,
            overbudget_categories TEXT
        )
    """)
    conn.commit()

    try:
        res = requests.get(f"{express_url}/api/reports/summary", headers={
            "Authorization": f"Bearer {token}"
        })
        data = res.json()
        total = data.get("total", 0)
        top_cat = data.get("topCategory", "")
        overbudget = data.get("overbudgetCategories", [])  # optional

        # Check if current month report exists
        cursor.execute("SELECT 1 FROM monthly_reports WHERE month = %s AND user_id = %s", (month_now, user_id))
        exists = cursor.fetchone()

        if exists:
            print(f"[INFO] Updating report for user {user_id}, month {month_now}")
            cursor.execute("""
                UPDATE monthly_reports
                SET total_spent = %s, top_category = %s, overbudget_categories = %s
                WHERE month = %s AND user_id = %s
            """, (total, top_cat, ','.join(overbudget), month_now, user_id))
        else:
            print(f"[INFO] Inserting new report for user {user_id}, month {month_now}")
            cursor.execute("""
                INSERT INTO monthly_reports (user_id, month, total_spent, top_category, overbudget_categories)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, month_now, total, top_cat, ','.join(overbudget)))

        conn.commit()

    except Exception as e:
        print(f"[ERROR] Fetch or DB operation failed: {e}")
        return {"error": "Failed to process report"}, 500

    # Return last 6 months for the user
    cursor.execute("""
        SELECT month, total_spent, top_category
        FROM monthly_reports
        WHERE user_id = %s
        ORDER BY month DESC
        LIMIT 6
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    reports = [
        {"month": row[0], "total_spent": float(row[1]), "top_category": row[2]}
        for row in rows
    ]
    return reports, 200
