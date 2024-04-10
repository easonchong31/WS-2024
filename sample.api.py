from flask import Flask
from flask_restful import Resource, Api
import json
from flask import Flask, jsonify, request
from graphene import ObjectType, String, List, Schema, Field
from pymongo import MongoClient

from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask import request

app = Flask(__name__)
api = Api(app)

API_KEY = "apikey"

class route(Resource):
    def get(self):
        return [
            {'URL': 'http://127.0.0.1:5000/insertProduct'},
            {'URL': 'http://127.0.0.1:5000/getProducts'},
            {'URL': 'http://127.0.0.1:5000/getTitles'},
        ]
api.add_resource(route, '/')

#creates the /getProducts class 
class GetProducts(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.products
        collection = db.products_data

        results = dumps(collection.find())
        return json.loads(results)
api.add_resource(GetProducts, '/getProducts')

#starts mongoDB connection
client = MongoClient("mongodb://root:example@localhost:27017/")
db = client.products
collection = db.products_data

#starts the graphQL schema
class Product(ObjectType):
    title = String()

class Query(ObjectType):
    product_titles = List(String)

    def resolve_product_titles(self, info, collection):
        titles = [doc["title"] for doc in collection.find({}, {"_id": 0, "title": 1})]
        return titles

schema = Schema(query=Query)

# the graphQL endpoint
class GraphQLResource(Resource):
    def post(self):
        data = json.loads(request.data)
        result = schema.execute(data['query'], collection=collection)
        return jsonify(result.data)

api.add_resource(GraphQLResource, '/graphql')

##########################################################################################

    #creates the /GetTitles class 
class GetTitles(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.products
        collection = db.products_data
#ID of the object
        filter = {"_id": 0, "title": 1}
#find it
        results = collection.find({}, filter)
        print(results)
#dump to JSON
        results = dumps(results)
#return
        return json.loads(results)
api.add_resource(GetTitles, '/getTitles')

#########################################################################################

class insertProduct(Resource):
    def get(self):
        api_key = request.args.get('api_key')
        if api_key != API_KEY:
            return {"error": "Unable to Connect, Wrong API KEY"}

        # make the class
            client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.products
        collection = db.products_data
        collection.insert_one([
            {
                "id": 1,
                "title": "Jam",
                "price": 1.50,
                "quantity": 2
            },
            {
                "id": 2,
                "title": "Coffee",
                "price": 2.30,
                "quantity": 1
            },
            {
                "id": 3,
                "title": "Cola",
                "price": 11.20,
                "quantity": 2
            },
            {
                "id": 4,
                "title": "Tea",
                "price": 4.50,
                "quantity": 3
            }
        ])

        return {"status": "inserted"}
api.add_resource(insertProduct, '/insertProduct')

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client.products
collection = db.products_data

class InsertOne(Resource):
    def get(self):
        try:
            sale_id = request.args.get('SaleId')
            order_id = request.args.get('OrderId')
            product_id = request.args.get('ProductId')
            quantity = request.args.get('Quantity')

            sale_id = int(sale_id)
            order_id = int(order_id)
            product_id = int(product_id)
            quantity = int(quantity)

            new_record = {"SaleId": sale_id, "OrderId": order_id, "ProductId": product_id, "Quantity": quantity}

            res = collection.insert_one(new_record)

            return {"status": "inserted"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(InsertOne, '/insertOne')

if __name__ == '__main__':
    app.run(debug=True)
