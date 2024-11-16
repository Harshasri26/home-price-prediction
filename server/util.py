import os
import json
import pickle
import numpy as np
__locations = None
__data_columns = None
__model = None
def get_estimated_price(location, sqft, bhk, bath):
    """Function to get estimated price based on the inputs."""
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1
    x = np.zeros(len(__data_columns)) 
    x[0] = sqft  
    x[1] = bath  
    x[2] = bhk  
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)
def load_saved_artifacts():
    """Function to load the saved model and other artifacts."""
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    current_folder = os.path.dirname(__file__)  
    artifacts_folder = os.path.join(current_folder, 'artifacts')
    columns_path = os.path.join(artifacts_folder, 'columns.json')
    with open(columns_path, 'r') as f:
        columns_data = json.load(f)
        __data_columns = columns_data['data_columns'] 
        __locations = __data_columns[3:] 
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
if __name__ == '__main__':
    load_saved_artifacts()  
    print(get_location_names()) 
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))  
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2)) 
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2)) 
