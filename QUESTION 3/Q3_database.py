# QUESTION 3 (PART 2) (PYTHON)

import sqlite3

def view_compact_rows():
    conn = sqlite3.connect('dbs_applications.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()

    print("\nDBS APPLICATIONS DATABASE\n" + "-"*80)
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} {row[7]} | {row[8]}")
    print(f"\nTotal Records: {len(rows)}\n")
    conn.close()

# Call this instead of tabulate
view_compact_rows()