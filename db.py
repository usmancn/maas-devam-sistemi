import pymysql

def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",          # şifren varsa buraya yaz
        database="maas_takip",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # SÖZLÜK şeklinde veri döndürsün
    )
    return connection
