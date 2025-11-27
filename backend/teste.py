from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin123@clustertrabalho.hfrkame.mongodb.net/?appName=ClusterTrabalho")

db = client["osmanager"]

try:
    print("Conectando ao MongoDB...")
    print("Collections existentes:", db.list_collection_names())
    print("Deu bom, conexão funcionando.")
except Exception as e:
    print("DEU RUIM NA CONEXÃO:")
    print(e)