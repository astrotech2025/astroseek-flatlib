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
    luogo = request.args.get("luogo", "Roma")

    if not data or not ora or not luogo:
        return jsonify({"error": "Parametri insufficienti"}), 400

    try:
        anno, mese, giorno = data.split("-")
        hh, mm = ora.split(":")
        dt = Datetime(f"{anno}-{mese}-{giorno}", f"{hh}:{mm}", '+01:00')  # UTC+1

        # Coordinate provvisorie basate sul luogo
        if "Taranto" in luogo:
            pos = GeoPos("40.4644", "17.2470")
        elif "Roma" in luogo:
            pos = GeoPos("41.9028", "12.4964")
        else:
            # Default generico (es. Bari)
            pos = GeoPos("41.1171", "16.8719")

        chart = Chart(dt, pos)

        sole = chart.get(const.SUN)
        luna = chart.get(const.MOON)
        asc = chart.get(const.ASC)

        return jsonify({
            "nome": nome,
            "sole": sole.sign,
            "luna": luna.sign,
            "ascendente": asc.sign
        })
    except Exception as e:
        return jsonify({"error": f"Errore di calcolo: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)