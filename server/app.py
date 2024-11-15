from flask import Flask, render_template, request, jsonify
from util import load_saved_artifacts, get_location_names, get_estimated_price

# Initialize the Flask app and set correct paths for static and templates
app = Flask(__name__, template_folder='templates', static_folder='static')

# Route to render the HTML page
@app.route("/")
def index():
    return render_template('app.html')  # Renders the HTML file (app.html)

# Route to fetch location names for the dropdown
@app.route('/api/location_names', methods=['GET'])
def api_get_location_names():
    locations = get_location_names()  # Fetches the list of locations
    return jsonify({'locations': locations})  # Sends the data as JSON

# Route to predict home price based on user input
@app.route('/api/predict_home_price', methods=['POST'])
def api_predict_home_price():
    try:
        # Get the input values from the request
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Call the model prediction function
        estimated_price = get_estimated_price(location, total_sqft, bhk, bath)

        # Return the estimated price as a JSON response
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow CORS for all origins
        return response

    except Exception as e:
        print("Error in prediction API:", e)
        return jsonify({'error': str(e)}), 400  # Return error message with 400 status code

# Start the Flask app
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()  # Loads saved machine learning model and other artifacts
    app.run(debug=True)  # Runs the app in debug mode
