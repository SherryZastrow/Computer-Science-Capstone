import json
from bson import json_util
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['City']
collection = db['inspections']


def create_document(document):
    try:
       collection.save(document)
    except Exception as e:
        print(e)
        return False
    return True

def read_document(search_criteria):
    try:
        result = collection.find(search_criteria)
    except:
        return False

    if result.count() == 0:
        return False

    result_lists = [item for item in result]

    return json_util.dumps(result_lists)

def update_document(search_criteria, new_values):
    try:
        result = collection.update_many(search_criteria, new_values)
    except Exception as e:
        return False
        raise SystemExit(e)
    return json_util.dumps(result.raw_result,
                           default=json_util.default)

def remove_document(search_criteria):
    try:
        result=collection.delete_many(search_criteria)
    except Exception as e:
        raise SystemExit(e)
    return json_util.dumps(result.raw_result,
                           default=json_util.default)

