from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

dir = [
    {
        'name': 'file1',
        'content': 'Cel mai frumos content care apartine file1'
    },
    {
        'name': 'file2',
        'content': 'O placere din file2'
    },
    {
        'name': 'file3',
        'content': 'Dell Technologies World file3'
    }
]


def add_file_links(file):
    return {
        **file,
        '_links': {
            'self': f'/dir/{file["name"]}',
            'update': {
                'href': f'/dir/{file["name"]}',
                'method': 'PUT'
            },
            'delete': {
                'href': f'/dir/{file["name"]}',
                'method': 'DELETE'
            },
            'parent': {
                'href': '/dir',
                'method': 'GET'
            }
        }
    }


def add_directory_links(files):
    return {
        'Files': [add_file_links(file) for file in files],
        '_links': {
            'self': {
                'href': '/dir',
                'method': 'GET'
            },
            'create': {
                'href': '/dir',
                'method': 'POST'
            }
        }
    }


@app.route("/dir", methods=['GET'])
def getAllFiles():
    return jsonify(add_directory_links(dir)), 200

@app.route("/dir/<name>", methods=['GET'])
def getSingleFile(name):
    for file in dir:
        if file['name'] == name:
            return jsonify({'File': add_file_links(file)}), 200
    return jsonify({'error': 'File not found'}), 404

@app.route("/dir/<name>", methods=["PUT"])
def createOrUpdateFile(name):
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing Content'}), 400

    for file in dir:
        if file['name'] == name:
            file['name'] = name
            file['content'] = data['content']
            return '', 204

    new_file = {'name': name, 'content': data['content']}
    dir.append(new_file)
    return jsonify({'message': 'Created', 'file': add_file_links(new_file)}), 201

@app.route("/dir", methods=['POST'])
def createFile():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing name or content'}), 400

    name = "file"+str(len(dir)+1)

    for file in dir:
        if file['name'] == name:
            return jsonify({'error': 'File already exists'}), 409

    new_file = {'name': name, 'content': data['content']}
    dir.append(new_file)
    
    return jsonify({'message': 'File created', 'file': add_file_links(new_file)}), 201

@app.route("/dir/<name>", methods=['DELETE'])
def deleteFile(name):
    global dir
    for file in dir:
        if file['name'] == name:
            dir = [f for f in dir if f['name'] != name]
            return '', 204
    return jsonify({'error': 'File not found'}), 404

@app.route("/")
def main():
    return redirect('/dir')
