import os
from flask import Flask, render_template, request
import datetime
from pymongo import  MongoClient
from dotenv import load_dotenv

def crear_app():
    app = Flask(__name__)
    cliente = MongoClient(os.getenv("MONGODB_URI"))
    app.db = cliente.trades

    #entradas = []
    entradas = [entrada for entrada in app.db.entradas.find({})]
    print(entradas)

    @app.route("/", methods=["GET", "POST"])

    def home():
        if request.method == "POST":
            #tradeDate = request.form.get("tradeDate")
            raw_date = request.form.get("tradeDate")  # e.g. "2025-06-09T15:34"
            # Parseamos al objeto datetime y luego lo formateamos
            dt_obj = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M")
            tradeDate = dt_obj.strftime("%d/%m/%Y %H:%M")  # "09/06/2025 15:34"

            currencyPair = request.form.get("currencyPair")
            direction = request.form.get("direction")
            positionSize = request.form.get("positionSize")
            entryPrice = request.form.get("entryPrice")
            exitPrice = request.form.get("exitPrice")
            stopLoss = request.form.get("stopLoss")
            takeProfit = request.form.get("takeProfit")
            result = request.form.get("result")
            profitLoss = request.form.get("profitLoss")

            parametros = {
                "tradeDate" : tradeDate,
                "currencyPair" : currencyPair,
                "direction": direction,
                "positionSize": positionSize,
                "entryPrice": entryPrice,
                "exitPrice": exitPrice,
                "stopLoss": stopLoss,
                "takeProfit": takeProfit,
                "result": result,
                "profitLoss": profitLoss
            }

            entradas.append(parametros)

            app.db.entradas.insert_one(parametros)

        return render_template("index.html", entradas=entradas)
    return app

if __name__=="__main__":
    app = crear_app()
    app.run()