from ._anvil_designer import PredictorToolTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server

class PredictorTool(PredictorToolTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    # --- Load client data when the app starts ---
    client_data = anvil.server.call('get_client_data')
    self.client_country_map = client_data['country_map']
    self.client_name_dropdown.items = client_data['clients']
    # Check if there are any clients in the dropdown
    if self.client_name_dropdown.items:
        # Get the first client from the list to use as the default
      initial_client = self.client_name_dropdown.items[0]
      # Set the dropdown's selected value programmatically
      self.client_name_dropdown.selected_value = initial_client
        # Now, manually call the change handler to populate the country box
      self.client_name_dropdown_change()
  
  def client_name_dropdown_change(self, **event_args):
    """This method is called when the user selects a client."""
    selected_client = self.client_name_dropdown.selected_value
    if selected_client:
      # Automatically fill the country text box
      self.destination_country_box.text = self.client_country_map[selected_client]
    else:
      print("--")

  def predict_button_click(self, **event_args):
    """This method is called when the button is clicked."""
    numerical_boxes = [self.length_box,self.width_box, self.height_box, self.weight_box]
    for box in numerical_boxes:
      try:
        #Check if the input is empty or the number is zero or less
        if not box.text or float(box.text) <= 0:
          alert("Input for dimensions and weight cannot be zero or empty. Please try again.")
          return # Stop the function here
      except (TypeError, ValueError):
        # This handles cases where the user types non-numeric text (e.g., "abc")
        alert(f"Invalid input: '{box.text}'. Please enter a valid number.")
        return # Stop the function here

    # --- The rest of the function proceeds only if the inputs are valid ---                           
    
    self.predict_button.enabled = False
    self.predict_button.text = "Predicting..."
  
    try:
      results = anvil.server.call('predict_shipment',
                                  self.client_name_dropdown.selected_value,
                                  self.destination_country_box.text,
                                  self.length_box.text,
                                  self.width_box.text,
                                  self.height_box.text,
                                  self.weight_box.text)
  
      if "error" in results:
        alert(f"An error occurred: {results['error']}")
      else:
        self.shipment_type_score_label.text = f"{results['shipment_type']}"
        self.carrier_score_label.text = f"{results['carrier']}"
        # --- Show overall confidence score ---
        ov_conf = results.get('overall_confidence', 0)
        self.overall_confidence_score_label.text = f"{ov_conf:.1%}"
  
    except Exception as e:
      alert(f"Failed to communicate with the server: {e}")
  
    finally:
      self.predict_button.enabled = True
      self.predict_button.text = "Predict Carrier"

  def length_box_pressed_enter(self, **event_args):
    self.predict_button_click()

  def width_box_pressed_enter(self, **event_args):
    self.predict_button_click()

  def height_box_pressed_enter(self, **event_args):
    self.predict_button_click()

  def weight_box_pressed_enter(self, **event_args):
    self.predict_button_click()

  def dashboard_link_click(self, **event_args):
    open_form('PredictorTool.Dashboard')


