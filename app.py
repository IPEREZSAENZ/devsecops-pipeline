from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    r = requests.get('https://httpbin.org/get')
    return "OK " + str(r.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
