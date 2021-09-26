def get_data():
    import sqlite3

    conn = sqlite3.connect('plants.db')

    cursor = conn.cursor()
    data = []

    for row in cursor.execute('SELECT * FROM plants'):
        column = [i for i in row]
        data.append(column)

    conn.commit()
    conn.close()
    return data
