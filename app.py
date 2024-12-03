from flask import Flask, render_template, request

app = Flask(__name__)

# Dados de triagem
entradas = {
    "Análise Meli": {
        "perguntas": [
            "O produto está funcional?",
            "Há danos estéticos?"
        ],
        "decisoes": {
            ("sim", "não"): "AT LN",
            ("sim", "sim"): "IN-HOUSE LN",
            ("não", "sim"): "Fábrica de Reparos",
            ("não", "não"): "Qualidade",
        }
    },
    "RunOff": {
        "perguntas": [
            "O produto está dentro da garantia?",
            "Há defeitos funcionais?"
        ],
        "decisoes": {
            ("sim", "não"): "AT Same",
            ("sim", "sim"): "Fábrica de Reparos",
            ("não", "sim"): "Qualidade",
            ("não", "não"): "IN-HOUSE Same",
        }
    },
    # Adicionar outras entradas conforme necessário...
}

def decidir_destino(entrada, respostas):
    dados = entradas.get(entrada)
    if not dados:
        return "Entrada inválida"
    
    respostas_tuple = tuple(respostas)
    return dados["decisoes"].get(respostas_tuple, "Destino não definido")

@app.route("/", methods=["GET", "POST"])
def index():
    destino = None
    if request.method == "POST":
        entrada = request.form.get("entrada")
        respostas = [request.form.get(f"pergunta_{i}") for i in range(len(entradas[entrada]["perguntas"]))]
        destino = decidir_destino(entrada, respostas)
    
    return render_template("index.html", entradas=entradas, destino=destino)

if __name__ == "__main__":
    app.run(debug=True)
