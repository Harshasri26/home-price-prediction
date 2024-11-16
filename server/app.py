from flask import Flask, render_template, request, jsonify
from util import load_saved_artifacts, get_location_names, get_estimated_price
app = Flask(__name__, template_folder='templates', static_folder='static')
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/api/location_names', methods=['GET'])
def api_get_location_names():
    locations = get_location_names()  
    return jsonify({'locations': locations})  
@app.route('/api/predict_home_price', methods=['POST'])
def api_predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        estimated_price = get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*') 
        return response

    except Exception as e:
        print("Error in prediction API:", e)
        return jsonify({'error': str(e)}), 400 
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts() 
    app.run(debug=True) 
