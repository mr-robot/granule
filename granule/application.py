__author__ = 'beast'

from flask import Flask, request, g, jsonify

from flask.ext.httpauth import HTTPBasicAuth
from granular.store import get_manager
from granular.work import subscribe
auth = HTTPBasicAuth()

app = Flask(__name__)

def get_granule():
    granule = getattr(g, '_granular', None)
    if granule is None:
        granule = g._granular = get_manager(host="172.17.0.1")
    return granule

@app.teardown_appcontext
def close_connection(exception):
    granule = getattr(g, '_granular', None)
    if granule is not None:
        granule.close()


@auth.verify_password
def verify_pw(username, password):
    return get_granule().login(username, password)

@app.route('/api/2015-05-30/authenticate' , methods=['POST', 'GET'])
@auth.login_required
def login():
    return jsonify({})

@app.route('/api/2015-05-30/activity/' , methods=['POST', 'GET'])
@auth.login_required
def activities():
    if request.method == 'POST':

        input = request.get_json()

        activity = get_granule().run_activity(input)
        return jsonify(activity)
    else:

        activities_result = get_granule().get_user_activities(user_id=get_granule().user_id)


        return jsonify(activities=activities_result)

@app.route('/api/2015-05-30/activity/<activity_id>', methods=['GET'])
@auth.login_required
def activity(activity_id):

    activity = get_granule().get_activity(activity_id, get_granule().user_id)

    return jsonify(activity)

@app.route('/api/2015-05-30/activity/<activity_id>/result', methods=['GET', 'POST'])
@auth.login_required
def activity_result(activity_id):

    activity = get_granule().get_activity(activity_id, get_granule().user_id)

    return jsonify(activity)

@app.route('/')
def home():


    #get_granule().create_user("Test","Test")
    return ""

if __name__ == "__main__":
    app.run(debug=True, port=8080)