from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Call the backend function to get the interactive plots
    plots = anvil.server.call('get_dashboard_plots')

    # Display the plots in the plot components
    self.carrier_plot.figure = plots['plot1']
    self.map_plot.figure = plots['plot2']
    self.scatter_plot.figure = plots['plot3']

  def carrier_predictor_link_click(self, **event_args):
    open_form('PredictorTool')



