__author__ = 'beast'


from flask import Flask, request
app = Flask(__name__)

@app.route('/test_endpoint', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        return "<xml>"
    else:
        return "<xml>"

if __name__ == '__main__':
    app.run()