import anvil.server
import pandas as pd
import numpy as np
import joblib
import os
import io
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry

# --- Connect to Anvil ---
uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
anvil.server.connect(uplink_key)
print("Connected to Anvil server.")

# --- Load Models and Data ---
print("Loading models and data...")
shipment_classifier = joblib.load('./models/shipment_classifier.joblib')
carrier_predictor = joblib.load('./models/carrier_predictor.joblib')
carrier_label_encoder = joblib.load('./models/carrier_label_encoder.joblib')
full_dataset = pd.read_csv('./data/shipping-data.csv')

# --- Perform Feature Engineering on the Full Dataset ---
# Create the columns needed for the dashboard plots.
full_dataset['Volume_cubic_in'] = full_dataset['Length_in'] * full_dataset['Width_in'] * full_dataset['Height_in']
full_dataset['Density_lbs_per_cubic_in'] = full_dataset['Weight_lbs'] / (full_dataset['Volume_cubic_in'] + 1e-6)

print("Models and data loaded successfully.")

# --- Function to get client names and countries ---
@anvil.server.callable
def get_client_data():
    """Reads the dataset and returns a list of unique client names and a client-to-country map."""
    client_country_map = full_dataset.drop_duplicates(subset=['Client_Name']).set_index('Client_Name')['Destination_Country'].to_dict()
    client_list = sorted(list(client_country_map.keys()))
    return {'clients': client_list, 'country_map': client_country_map}

@anvil.server.callable
def get_dashboard_plots():
    """Generates and returns three interactive Plotly charts for the dashboard."""
    
    px.defaults.template = "plotly_dark"

    # --- Chart 1: Carrier Shipment Volume (Bar Chart) ---
    carrier_counts = full_dataset['Carrier_Service'].value_counts().reset_index()
    carrier_counts.columns = ['Carrier_Service', 'Count']
    fig1 = px.bar(carrier_counts, 
                  x='Count', 
                  y='Carrier_Service', 
                  orientation='h',
                  labels={'Count': 'Number of Shipments', 'Carrier_Service': 'Carrier'},
                  color_discrete_sequence=['#018374'],
                 )
    fig1.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis={'categoryorder':'total ascending'}, 
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # --- Chart 2: Global Shipments by Country (Map) ---
    country_counts = full_dataset['Destination_Country'].value_counts().reset_index()

    country_counts.columns = ['Country', 'Shipments']

    # Helper function to convert country names to ISO-3 codes
    def get_iso_alpha(country_name):
        if country_name == 'USA': return 'USA' # Handle special cases
        try:
            return pycountry.countries.get(name=country_name).alpha_3
        except AttributeError:
            return None # Return None for names not found

    country_counts['iso_alpha'] = country_counts['Country'].apply(get_iso_alpha)
    fig2 = px.choropleth(country_counts, 
                         locations='iso_alpha', 
                         locationmode='ISO-3',
                         color='Shipments',
                         hover_name='Country',
                         color_continuous_scale='tealgrn'
                        )
    fig2.update_layout(
        # Set all margins to 0 to make the map fill its container
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showframe=False,
        )
    )

    # --- Chart 3: Shipment Weight vs. Volume (Scatter Plot) ---
    fig3 = px.scatter(full_dataset,
                      x='Weight_lbs',
                      y='Volume_cubic_in',
                      color='Carrier_Service',
                      labels={'Weight_lbs': 'Weight (lbs)', 'Volume_cubic_in': 'Volume (cubic inches)'},
                      hover_data=['Shipment_Type', 'Client_Name'],
                      color_discrete_sequence=px.colors.qualitative.G10
                     )
    fig3.update_layout(
        title_x=0.5,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return {'plot1': fig1, 'plot2': fig2, 'plot3': fig3}

# --- Prediction function ---
@anvil.server.callable
def predict_shipment(client_name, destination_country, length, width, height, weight):
    """Accepts user inputs and returns predictions and confidence scores."""
    try:
        # --- Data Prep & Feature Engineering ---
        length, width, height, weight = float(length), float(width), float(height), float(weight)
        input_data = pd.DataFrame({
            'Client_Name': [client_name], 'Destination_Country': [destination_country],
            'Weight_lbs': [weight], 'Length_in': [length], 'Width_in': [width], 'Height_in': [height]
        })
        input_data['Volume_cubic_in'] = input_data['Length_in'] * input_data['Width_in'] * input_data['Height_in']
        input_data['Density_lbs_per_cubic_in'] = input_data['Weight_lbs'] / (input_data['Volume_cubic_in'] + 1e-6)
        
        # --- Model 1 Prediction & Confidence ---
        features_for_model1 = ['Weight_lbs', 'Length_in', 'Width_in', 'Height_in', 'Volume_cubic_in', 'Density_lbs_per_cubic_in']
        
        type_probabilities = shipment_classifier.predict_proba(input_data[features_for_model1])[0]
        shipment_type_confidence = np.max(type_probabilities)
        predicted_type_encoded = np.argmax(type_probabilities)
        predicted_type = shipment_classifier.classes_[predicted_type_encoded]
        
        input_data['predicted_shipment_type'] = predicted_type

        # --- Model 2 Prediction & Confidence ---
        carrier_probabilities = carrier_predictor.predict_proba(input_data)[0]
        carrier_confidence = np.max(carrier_probabilities)
        predicted_carrier_encoded = np.argmax(carrier_probabilities)
        predicted_carrier = carrier_label_encoder.inverse_transform([predicted_carrier_encoded])[0]
        
        # --- Overall Confidence Calculation ---
        overall_confidence = shipment_type_confidence * carrier_confidence

        # --- Return Results ---
        return {
            'shipment_type': predicted_type, 
            'shipment_type_confidence': shipment_type_confidence,
            'carrier': predicted_carrier,
            'carrier_confidence': carrier_confidence,
            'overall_confidence': overall_confidence
        }
    except Exception as e:
        return {"error": str(e)}

# --- Keep the server running ---
print("Uplink server is running. Waiting for calls...")
anvil.server.wait_forever()