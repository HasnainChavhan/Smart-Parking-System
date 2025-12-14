import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

try:
    # Check if parking_lots table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='parking_lots'")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        print("❌ Tables don't exist. Run init_db.py first!")
    else:
        # Check if lot exists
        cursor.execute("SELECT COUNT(*) FROM parking_lots WHERE id = 1")
        lot_exists = cursor.fetchone()[0] > 0
        
        if not lot_exists:
            print("Creating parking lot...")
            
            # Insert parking lot
            now = datetime.datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO parking_lots (id, name, address, geo_location, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (1, "Main Parking Lot", "Building A", "0,0", now, now))
            
            # Insert 3 parking slots
            for i in range(1, 4):
                cursor.execute("""
                    INSERT INTO slots (id, lot_id, name, status, rate_per_hour, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (i, 1, f"A{i}", "free", 50, 1, now, now))
            
            conn.commit()
            print("✓ Created 1 parking lot with 3 slots (A1, A2, A3)")
        else:
            print("✓ Parking lot already exists")
            cursor.execute("SELECT COUNT(*) FROM slots WHERE lot_id = 1")
            slot_count = cursor.fetchone()[0]
            print(f"✓ Found {slot_count} parking slots")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

print("\n✓ Database ready!")
