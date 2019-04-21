#!/usr/bin/python
import json
from bson import json_util
import bottle
from bottle import route, run, request, abort

id = 0
# set up URI paths for REST service
@route('/greeting', method='GET')
def get_greeting():
    global id
    id = id + 1
    try:
        request.query.name
        name=request.query.name
        if name: 
          #make calls to database from here
               string="{ \"id\": "+str(id)+", \"content\": \"Hello, \""+request.query.name+"\"}"
        else:
               string="{ \"id\": "+str(id)+", \"content\": \"Hello, World!\"}"
    except NameError:
        abort(404, 'No parameter for id %s' % id)

    if not string:
        abort(404, 'No id %s' % id)
    return json.loads(json.dumps(string, indent=4, default=json_util.default))


if __name__ == '__main__': #declare instance of request
    #app.run(debug=True)
    run(host='localhost', port=8080)

