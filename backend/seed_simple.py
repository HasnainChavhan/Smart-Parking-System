import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

try:
    # Check if lot exists
    cursor.execute("SELECT COUNT(*) FROM lots WHERE id = 1")
    lot_exists = cursor.fetchone()[0] > 0
    
    if not lot_exists:
        print("Creating parking lot...")
        
        # Insert parking lot
        now = datetime.datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO lots (id, name, location, total_slots, lot_type, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (1, "Main Parking Lot", "Building A", 3, "outdoor", now, now))
        
        # Insert 3 parking slots
        for i in range(1, 4):
            cursor.execute("""
                INSERT INTO slots (id, lot_id, name, status, rate_per_hour, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (i, 1, f"A{i}", "free", 50, now, now))
        
        conn.commit()
        print("✓ Created 1 parking lot with 3 slots (A1, A2, A3)")
    else:
        print("✓ Parking lot already exists")
        cursor.execute("SELECT COUNT(*) FROM slots WHERE lot_id = 1")
        slot_count = cursor.fetchone()[0]
        print(f"✓ Found {slot_count} parking slots")
        
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n✓ Database seeded successfully!")
