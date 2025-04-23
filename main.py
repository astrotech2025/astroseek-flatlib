from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
import re

app = Flask(__name__)
CORS(app)

# Funzioni di supporto
def normalize_date(d):
    # Estrae solo numeri dalla data
    return re.sub(r"[^\d\-]", "", d.strip())

def normalize_time(t):
    parts = t.strip().split(":")
    if len(parts) == 1:
        return f"{parts[0]}:00"
    elif len(parts) == 2:
        return f"{int(parts[0]):02d}:{int(parts[1]):02d}"
    return "12:00"

@app.route("/astroseek", methods=["GET"])
def astro_data():
    nome = request.args.get("nome", "Anonimo")
    data = request.args.get("data")
    ora = request.args.get("ora")
    luogo = request.args.get("luogo", "Taranto")
    genere = request.args.get("genere", "neutro")

    print(f"➡️ Parametri ricevuti: nome={nome}, data={data}, ora={ora}, luogo={luogo}, genere={genere}")

    if not data or not ora or not luogo:
        return jsonify({"error": "Parametri insufficienti"}), 400

    try:
        # Parsing data robusto
        data = normalize_date(data)
        parts = re.findall(r"\d+", data)
        if len(parts) != 3:
            raise ValueError("Data non valida")
        anno, mese, giorno = map(int, parts)

        # Parsing ora robusto
        ora = normalize_time(ora)
        hh, mm = map(int, ora.split(":"))

        # Costruzione oggetto Datetime
        dt = Datetime(f"{anno:04d}-{mese:02d}-{giorno:02d}", f"{hh:02d}:{mm:02d}", '+01:00')

        # Coordinate semplificate
        if "Taranto" in luogo:
            lat, lon = "40.4644", "17.2470"
        elif "Roma" in luogo:
            lat, lon = "41.9028", "12.4964"
        elif "Milano" in luogo:
            lat, lon = "45.4642", "9.1900"
        elif "Napoli" in luogo:
            lat, lon = "40.8522", "14.2681"
        else:
            lat, lon = "41.1171", "16.8719"  # Default Bari

        print(f"📍 Coordinate usate: lat={lat}, lon={lon}")
        pos = GeoPos(lat, lon)

        chart = Chart(dt, pos)
        sole = chart.get(const.SUN).sign
        luna = chart.get(const.MOON).sign
        asc = chart.get(const.ASC).sign

        print(f"✅ Sole: {sole}, Luna: {luna}, Ascendente: {asc}")

        # Messaggio poetico
        if genere.lower() == "maschile":
            messaggio = "✦ Messaggio per lui: Tu sei codice che sogna. Sei emozione che organizza. Sei futuro che si muove con stile."
        elif genere.lower() == "femminile":
            messaggio = "✦ Messaggio per lei: Tu sei luce che danza. Sei memoria che guida. Sei universo che respira bellezza."
        else:
            messaggio = "✦ Messaggio per te: Sei armonia in movimento. Sei spirito che crea. Sei equilibrio tra tempo e stelle."

        return jsonify({
            "nome": nome,
            "sole": sole,
            "luna": luna,
            "ascendente": asc,
            "messaggio": messaggio
        })

    except Exception as e:
        print(f"❌ Errore durante il calcolo: {str(e)}")
        return jsonify({"error": f"Errore durante il calcolo: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
