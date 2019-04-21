import crud
import json
from bson import json_util
import bottle
from bottle import route, run, request, abort, static_file
import datetime

# set up URI paths for REST service
@route('/currentTime', method='GET')
def get_currentTime():
    dateString=datetime.datetime.now().strftime("%Y-%m-%d")
    timeString=datetime.datetime.now().strftime("%H:%M:%S")
    string="{\"date\":"+dateString+",\"time\":"+timeString+"}"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

@route ('/hello', method='GET')
def get_hello():
    string_dict = {'world': 'hello'}
    string = "{" + string_dict[request.query.name] + ": \"" + request.query.name + "\" }"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

@route ('/strings', method='POST')
def post_hello():
    first = request.json.get('string1')
    second = request.json.get('string2')
    string = "{ first: " + "\"" + first + "\"" + ", second: " + "\"" + second + "\" }"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

@route ('/create', method='POST')
def post_create():
    
    document = {}
    for key in request.query:
        try:
            document[key] = int(request.query[key].replace('"', ''))
        except:
            document[key] = request.query[key].replace('"', '')

    string = str(crud.create_document(document))
    return json.loads(json.dumps(string, indent=4, default=json_util.default))


@route ('/read', method='GET')
def get_read():

    search_criteria = {}

    for key in request.query:
        search_criteria[key] = request.query[key]

        
    result = crud.read_document(search_criteria)
    return json.loads(json.dumps(result, indent=4, default=json_util.default))

@route ('/update', method='GET')
def get_update():

    search_key = ""
    search_value = ""
    result_value = {}
    for key in request.query:
        if key == "column":
            search_key = request.query[key].replace('"', '')
        elif key == "searchvalue":
            try:
                search_value = int(request.query[key].replace('"', ''))
            except:
                search_value = request.query[key].replace('"', '')
        else:
            try:
                result_value[key] = int(request.query[key].replace('"', ''))
            except:
                result_value[key] = request.query[key].replace('"','')


    search_criteria = {search_key : search_value}
    changes = {'$set': result_value}
    print(changes)
    result = crud.update_document(search_criteria, changes)
    return json.loads(json.dumps(result, indent=4, default=json_util.default))

@route ('/delete', method='GET')
def get_delete():

    search_criteria = {}

    for key in request.query:
       try:
           search_criteria[key] = int(request.query[key].replace('"', ''))
       except:
           search_criteria[key] = request.query[key].replace('"', '')
    result = crud.remove_document(search_criteria)
    return json.loads(json.dumps(result, indent=4, default=json_util.default))

@route ('/search', method='GET')
def get_search():
    search_criteria = {}
    sort_criteria = None
    sort_value = None

    for key in request.query:
        if key == "sort_value":
            sort_value = request.query[key]
        else:
            try:
                search_criteria[key] = int(request.query[key].replace('"', ''))
            except:
                search_criteria[key] = request.query[key].replace('"', '')
            print(key, request.query[key])

    if sort_value == None:
        return "404: Missing sort_value"
    else:
        print(search_criteria)
        result = crud.read_document(search_criteria)
        result_json = json.loads(json.dumps(result, indent=4, default=json_util.default))
#For each item in the list, if the item = the sort value, it is switched to the top. 
#If not, it is switched to the bottom
        result_list = []
        if result_json is False:
            return "404: No results found"

        for item in result_json:
            if sort_value in str(item):
                result_list.insert(0, item)
            else:
                result_list.append(item)

        return result_list

@route('/', method='GET')
def serve_index():
    return static_file('index.html', root='/home/kazasu/Sherrys_folder/cs')


if __name__ == '__main__':
    #app.run(debug=True)
    run(host='54.39.40.227', port=8080)


