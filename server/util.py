import os
import json
import pickle
import numpy as np

# Global variables for the locations, columns, and the model
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    """Function to get estimated price based on the inputs."""
    try:
        # Get the index of the location in the list of data columns
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # If the location is not found, set index to -1
        loc_index = -1

    # Create the input feature vector (one-hot encoded for location)
    x = np.zeros(len(__data_columns))  # Create an array of zeros
    x[0] = sqft  # Square footage
    x[1] = bath   # Number of bathrooms
    x[2] = bhk    # Number of bedrooms

    if loc_index >= 0:
        x[loc_index] = 1  # Set the location feature to 1 if found in the columns

    # Predict the price using the model
    return round(__model.predict([x])[0], 2)

def load_saved_artifacts():
    """Function to load the saved model and other artifacts."""
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    # Get the path for the artifacts folder (where the saved files are stored)
    current_folder = os.path.dirname(__file__)  # Get the current directory
    artifacts_folder = os.path.join(current_folder, 'artifacts')  # Path to the artifacts folder

    # Load columns.json to get the data columns (features)
    columns_path = os.path.join(artifacts_folder, 'columns.json')
    with open(columns_path, 'r') as f:
        columns_data = json.load(f)
        __data_columns = columns_data['data_columns']  # Get all columns
        __locations = __data_columns[3:]  # Skip the first 3 columns (sqft, bath, bhk) for locations

    # Load the machine learning model
    global __model
    if __model is None:
        model_path = os.path.join(artifacts_folder, 'banglore_home_prices_model.pickle')
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)

    print("loading saved artifacts...done")

def get_location_names():
    """Return the list of location names."""
    return __locations

def get_data_columns():
    """Return the list of all data columns (including location and other features)."""
    return __data_columns

# Main function to test the loading of artifacts and prediction
if __name__ == '__main__':
    load_saved_artifacts()  # Load the artifacts (model and columns)
    print(get_location_names())  # Print the available locations
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))  # Test the price prediction
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))  # Test the price prediction
    print(get_estimated_price('Kalhalli', 1000, 2, 2))  # Test the price prediction
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # Test the price prediction
