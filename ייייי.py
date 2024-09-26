from sqlalchemy import create_engine, text

# הגדרת פרטי החיבור
DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/normal_db'  # כולל פורט
engine = create_engine(DATABASE_URL)

try:
    # בודק אם החיבור עובד
    with engine.connect() as connection:
        # שימוש באובייקט text כדי להריץ את השאילתה
        result = connection.execute(text("SELECT version();"))
        for row in result:
            print("PostgreSQL version:", row[0])
except Exception as e:
    print("Error:", e)
