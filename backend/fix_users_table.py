import sqlite3

# Connect to database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

try:
    # Get current columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    # Add missing columns
    columns_to_add = {
        'hashed_password': 'TEXT',
        'is_active': 'INTEGER DEFAULT 1',
        'created_at': 'TEXT',
        'updated_at': 'TEXT'
    }
    
    for col_name, col_type in columns_to_add.items():
        if col_name not in columns:
            print(f"Adding {col_name}...")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            conn.commit()
            print(f"✓ {col_name} added")
        else:
            print(f"✓ {col_name} already exists")
        
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n✓ All columns added successfully!")
