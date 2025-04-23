
from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = Flask(__name__)
CORS(app)

@app.route("/astroseek", methods=["GET"])
def astro_data():
    nome = request.args.get("nome", "Anonimo")
    data = request.args.get("data")
    ora = request.args.get("ora")
    luogo = request.args.get("luogo", "Taranto")

    print(f"➡️ Ricevuto: nome={nome}, data={data}, ora={ora}, luogo={luogo}")

    if not data or not ora or not luogo:
        print("⛔ Parametri mancanti.")
        return jsonify({"error": "Parametri insufficienti"}), 400

    try:
        print(f"🧪 Debug: valore di data prima del parsing: {data}")
        anno, mese, giorno = map(int, data.strip().split("-"))
        hh, mm = map(int, ora.strip().split(":"))
        dt = Datetime(f"{anno:04d}-{mese:02d}-{giorno:02d}", f"{hh:02d}:{mm:02d}", '+01:00')
    except Exception as e:
        print(f"⚠️ Errore parsing data/ora: {str(e)}")
        return jsonify({"error": f"Errore parsing data/ora: {str(e)}"}), 400

    try:
        if "Taranto" in luogo:
            lat, lon = "40.4644", "17.2470"
        elif "Roma" in luogo:
            lat, lon = "41.9028", "12.4964"
        else:
            lat, lon = "41.1171", "16.8719"

        pos = GeoPos(lat, lon)
        print(f"📍 Coordinate usate: {lat}, {lon}")

        chart = Chart(dt, pos)
        sole = chart.get(const.SUN)
        luna = chart.get(const.MOON)
        asc = chart.get(const.ASC)

        print(f"✅ Sole: {sole.sign}, Luna: {luna.sign}, Ascendente: {asc.sign}")

        return jsonify({
            "nome": nome,
            "sole": sole.sign,
            "luna": luna.sign,
            "ascendente": asc.sign
        })

    except Exception as e:
        print(f"❌ Errore di calcolo: {str(e)}")
        return jsonify({"error": f"Errore di calcolo: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
