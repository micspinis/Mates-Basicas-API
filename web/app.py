from flask import Flask, jsonify, request
#Para construit la API necesitamos los siguientes modulos
from flask_restful import Api, Resource

#Importar MongoDB
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

#Inicializando cliente de mondo, usando el mismo nombre que le dimos en el docke compose
# docker compose para mondo -> db
# Puerto -> 27017 (puerto por defecto para mongo)
client = MongoClient("mongodb://db:27017")

# Creando data base
# client."Nombre de la base de datos"
db = client.aNewDB

#Creando colleccion
UserNum = db["UserNum"]


#Schemas de los documentos
UserNum.insert({
    "num_of_user": 0
})


# Crear una clase que muestre el numero de visitante cuando el usuario entre, el numero de visitante sera almacenado en nuestra DB en la colleccion UserNum en el documento que creamos ahi.
class Visit(Resource):
    def get(self):
        # Query syntax monog para ingresar al campo deseado
        prev_num = UserNum.find({})[0]['num_of_user']
        new_num = prev_num + 1
        #Query syntax "UPDATE" para actualizar la db con el nuevo dato, en python debemos poner el set en comillas por que es una palabra reservada
        UserNum.update({}, {"$set":{"num_of_user":new_num}})
        return str("Hello visitor " + str(new_num))


#Resources


#el function name recibe el nombre del end point no de la clase.
def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200

class Add(Resource):
    """
    Los metodos (Como GET, POST, etc.) deben ser especificados.
     def post(self):
        #if I am here, then the resource Add was requested using the method POST
    def get(self):
        #if I am here, then the resource Add was requested using the method GET.
    def put(self):
        pass
    def delete(self):
        pass
    """
    def post(self):
        #if I am here, then the resource Add was requested using the method POST

        #Step 1: Get posted data
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code != 200):
            retJson = {
                    "Message": "An error happend",
                    "Status Code": status_code
                    }
            return jsonify(retJson)

        # If i am here, then status_code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        # Step 2: Add the posted data
        ret = x+ y
        retMap = {
                'Message': ret,
                'Status Code': status_code
                }
        return jsonify(retMap)


class Subtract(Resource):
     def post(self):
        #if I am here, then the resource subtract was requested using the method POST

        #Step 1: Get posted data
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")
        if (status_code != 200):
            retJson = {
                    "Message": "An error happend",
                    "Status Code": status_code
                    }
            return jsonify(retJson)

        # If i am here, then status_code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        # Step 2: Subtract the posted data
        ret = x - y
        retMap = {
                'Message': ret,
                'Status Code': status_code
                }
        return jsonify(retMap)   

class Multiply(Resource):
    def post(self):
        #if I am here, then the resource Multiply was requested using the method POST

        #Step 1: Get posted data
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")
        if (status_code != 200):
            retJson = {
                    "Message": "An error happend",
                    "Status Code": status_code
                    }
            return jsonify(retJson)

        # If i am here, then status_code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        # Step 2: Multiply the posted data
        ret = x * y
        retMap = {
                'Message': ret,
                'Status Code': status_code
                }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #if I am here, then the resource Divide was requested using the method POST

        #Step 1: Get posted data
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")
        if (status_code != 200):
            retJson = {
                    "Message": "An error happend",
                    "Status Code": status_code
                    }
            return jsonify(retJson)

        # If i am here, then status_code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = float(x)
        y = float(y)

        # Step 2: Divide the posted data
        ret = x / y
        retMap = {
                'Message': ret,
                'Status Code': status_code
                }
        return jsonify(retMap)


# PATH
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello_world():
    return "Hello World!"



if __name__  == "__main__":
    app.run(host='0.0.0.0')
