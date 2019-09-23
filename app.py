from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import uuid


app = Flask(__name__)

# configuring pusher object
pusher = Pusher(
    app_id='866933',
    key='74cff551bcd791c64f05',
    secret='3a377cdc775d18f7920a',
    cluster='mt1',
    ssl=True
)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


@app.route('/feed')
def feed():
    return render_template('feed.html')

# API endpoints
# store post


@app.route('/post', methods=['POST'])
def addPost():
    data = {
        'id': "post-{}".format(uuid.uuid4().hex),
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'status': 'active',
        'event_name': 'created'
    }
    pusher.trigger("blog", "post-added", data)
    return jsonify(data)

# deactivate or delete post
@app.route('/post/<id>', methods=['PUT', 'DELETE'])
def updatePost(id):
    data = {'id': id}
    if request.methodd == 'DELETE':
        data['event_name'] = 'deleted'
        pusher.trigger("blog", "post-deleted", data)
    else:
        data['event_name'] = 'deactivated'
        pusher.trigger("blog", "post-deactivated", data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
