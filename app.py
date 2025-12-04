from flask import Flask, render_template, request, redirect, url_for
from db import get_connection


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/testdb")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM personel")
        count = cursor.fetchone()["COUNT(*)"] if isinstance(cursor.fetchone(), dict) else count
        # Yukarıdaki satır biraz karıştıysa boşver, zaten testdb'yi geçeceğiz :)
        return f"Veritabanı bağlantısı OK! Personel sayısı: {count}"
    except Exception as e:
        return f"Veritabanı bağlantı HATASI: {e}"

@app.route("/personel")
def personel_list():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 
            p.personel_id,
            p.ad,
            p.soyad,
            p.maas,
            p.aktif_mi,
            d.departman_adi
        FROM personel p
        LEFT JOIN departman d ON p.departman_id = d.departman_id
        ORDER BY p.personel_id;
    """
    cursor.execute(sql)
    personeller = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("personel_list.html", personeller=personeller)

@app.route("/personel_ekle", methods=["GET", "POST"])
def personel_ekle():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        departman_id = request.form.get("departman_id") or None
        maas = request.form.get("maas") or None

        insert_sql = """
            INSERT INTO personel (ad, soyad, departman_id, maas, aktif_mi)
            VALUES (%s, %s, %s, %s, 1)
        """
        cursor.execute(insert_sql, (ad, soyad, departman_id, maas))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for("personel_list"))

    # GET isteği: departmanları çek ve formu göster
    cursor.execute("SELECT departman_id, departman_adi FROM departman ORDER BY departman_adi")
    departmanlar = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("personel_ekle.html", departmanlar=departmanlar)


if __name__ == "__main__":
    app.run(debug=True)
