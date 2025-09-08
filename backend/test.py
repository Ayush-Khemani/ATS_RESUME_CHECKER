from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Test app working!"

if __name__ == '__main__':
    print("Starting test app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("This should not print until app stops")