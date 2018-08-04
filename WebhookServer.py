from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def index():
    return 'Choose Option'


@app.route('/test_cmd', methods = ['POST','GET'])
def test_cmd():
    print("Test cmd done")
    return  "Test cmd done"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7000)