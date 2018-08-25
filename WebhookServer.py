

from LEDController import LEDController
from flask import Flask, request

app = Flask(__name__)
"""
This code receives commands from IFTTT and executes the commands on the pi

"""
@app.route('/', methods = ['POST','GET'])
def index():
    return 'Choose Option'


@app.route('/test_cmd', methods = ['POST','GET'])
def test_cmd():
    print("Test cmd done")
    return  "Test cmd done"

@app.route('/set_color', methods = ['POST'])
def set_color():
    color = request.args.get('color')
    ledControl.set_color(color)
    print("setting color to"+str(color))
    return ("setting color to"+str(color))


if __name__ == '__main__':
    ledControl = LEDController()
    app.run(debug=False, host='0.0.0.0', port=7000)