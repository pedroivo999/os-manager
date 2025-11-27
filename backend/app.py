from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import hashlib
import uuid

app = Flask(__name__)
CORS(app)

# Conexão MongoDB Atlas
client = MongoClient("mongodb+srv://admin:admin123@clustertrabalho.hfrkame.mongodb.net/?appName=ClusterTrabalho")
db = client["osmanager"]
usuarios = db["usuarios"]
ordens = db["ordens_servico"]

# ------------------------
# FUNÇÕES AUXILIARES
# ------------------------
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def autenticar(token):
    user = usuarios.find_one({"token": token})
    return user is not None


# ------------------------
# ROTAS DE AUTENTICAÇÃO
# ------------------------
@app.route("/", methods=["GET"])
def index():
    return "Backend OS Manager rodando bonitinho."

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = usuarios.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if user["senha"] != hash_senha(data["senha"]):
        return jsonify({"error": "Senha incorreta"}), 401

    return jsonify({"token": user["token"]})


@app.route("/criar_usuario", methods=["POST"])
def criar_usuario():
    data = request.json

    if usuarios.find_one({"email": data["email"]}):
        return jsonify({"error": "Usuário já existe"}), 400

    token = str(uuid.uuid4())

    usuarios.insert_one({
        "email": data["email"],
        "senha": hash_senha(data["senha"]),
        "token": token
    })

    return jsonify({"msg": "Usuário criado", "token": token})


# ------------------------
# CRUD ORDEM DE SERVIÇO
# ------------------------
@app.route("/os", methods=["GET"])
def listar_os():
    token = request.headers.get("Authorization")
    if not autenticar(token):
        return jsonify({"error": "Não autorizado"}), 401

    lista = list(ordens.find({}, {"_id": 0}))
    return jsonify(lista)


@app.route("/os", methods=["POST"])
def criar_os():
    token = request.headers.get("Authorization")
    if not autenticar(token):
        return jsonify({"error": "Não autorizado"}), 401

    data = request.json
    ordens.insert_one(data)
    return jsonify({"msg": "OS criada"})


@app.route("/os", methods=["PUT"])
def editar_os():
    token = request.headers.get("Authorization")
    if not autenticar(token):
        return jsonify({"error": "Não autorizado"}), 401

    data = request.json
    ordens.update_one({"numero": data["numero"]}, {"$set": data})
    return jsonify({"msg": "OS atualizada"})


@app.route("/os", methods=["DELETE"])
def deletar_os():
    token = request.headers.get("Authorization")
    if not autenticar(token):
        return jsonify({"error": "Não autorizado"}), 401

    numero = request.args.get("numero")
    ordens.delete_one({"numero": numero})
    return jsonify({"msg": "OS excluída"})


if __name__ == "__main__":
    app.run(debug=True)
