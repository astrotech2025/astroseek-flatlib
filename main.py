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
    data = request.args.get("data")  # yyyy-mm-dd
    ora = request.args.get("ora")    # HH:MM
    luogo = request.args.get("luogo", "Roma")

    try:
        anno, mese, giorno = data.split("-")
        ora, minuti = ora.split(":")
        dt = Datetime(f"{anno}-{mese}-{giorno}", f"{ora}:{minuti}", '+01:00')  # UTC+1

        # Geolocalizzazione fittizia per il luogo, sostituibile con lookup
        pos = GeoPos('40.4644', '17.2470') if 'Taranto' in luogo else GeoPos('41.9028', '12.4964')  # Roma default

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
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)