import sqlite3

def check():
    conn = sqlite3.connect("data/zomato.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT name, location, cuisines, cost, rating FROM restaurants WHERE location LIKE '%MG Road%' ORDER BY name, rating DESC LIMIT 20")
    rows = cursor.fetchall()
    for row in rows:
        print(dict(row))
    conn.close()

if __name__ == "__main__":
    check()
