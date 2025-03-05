# Main backend server file for AOMC

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'AOMC Backend Running!'

if __name__ == '__main__':
    app.run(debug=True)