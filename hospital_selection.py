from taipy import Gui
from taipy.gui import notify
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import skcriteria as skc
from skcriteria.preprocessing import invert_objectives, scalers
from skcriteria.agg import simple

address = "Type address here..."
address_completed = False
location = None
final_location = ""
found_address = False
df = pd.read_csv("hospital_data.csv", engine='pyarrow')
df.dropna(axis=0, inplace=True)
# df.set_index("Phone Number", drop=False, inplace=True)
distance_completed = False
matrix = None
objectives = [max, max, min]
weights = []
default_weights = [0.25, 0.25, 0.5]
custom_weights = pd.DataFrame({'criteria': ["Patient Satisfaction", "Quality Care Measures", "Distance"],'weights': default_weights})

weights_correct = False

rankings_finished = False

ranks = pd.DataFrame({'Rank': [], 'Name': [], 'Phone Number': []})

page = """
# Hospital Selection
Hello! This application is designed to help you select a hospital that suits your needs best.


<|layout|columns=1 1|
First, please input your address.  
This information is for distance calculation purposes only and will not be stored.  
<|part|
<|input|id=input_address|value={address}|> <|button|label=Submit|id=submit_button|on_action=submit_button_action|> 
<|Can't find your address?|expandable|expanded=False|
Due to the nature of OpenStreetMap, the API we use for geocoding, sometimes being too specific can cause errors. Try listing only the state instead of the city and state, for example.
Also, try refreshing the page!
|>
|>
|>

<|layout|columns=1 1|
<|part|id=location_reveal|render={found_address}|
Your location is: **<|{final_location}|>**.  
If this is not correct, please resubmit your answer.    

<|Click for instructions|expandable|expanded=False|
The following are the weights for finding the hospital that is best for you.  
Please change the weights to be proportional to the importance this criteria has to you.  
**'Patient Satisfaction'** refers to an average of star ratings for satisfaction given by patients surveyed across a variety of services for this hospital. 
Example measures include "Nurse communication" and "Staff responsiveness. " These values range between 1 to 5 stars.  
**'Quality Care Measures'** refers to the average score this hospital received across a variety of services during a controlled study of sampled patients. 
This score is based on how well the hospital performed relative to expectations, and focuses more on quality of care given than simple patient satisfaction.
Example measures include "Prophylactic antibiotic received within 1 hour prior to surgical incision." These values range between 0 to 100.  
**'Distance'** refers to the distance between you and this hospital.  
|>
<|expandable|
<|{custom_weights}||table|editable=True|editable[criteria]=False|on_edit=edit_table|>
|>
<|button|label=Submit|id=table_submit|on_action=table_submit_action|>
|>


<|part|id=final_rankings|render={rankings_finished}|
<|Details of Rankings|expandable|expanded=False|
All rankings are normalized before computation. Therefore, a star rating halfway between 1 and 5 would become 0.5, and a quality score of 50 would also become 0.5.  
Distance is computed based on OpenStreetMap. Since many places have similar names, please double check the state you are located in.  
While the geolocator can calculate distances for anywhere on the globe, all hospitals in this dataset are located in the US, and therefore 
it is not recommended to use locations outside of the United States.  
Our algorithm seeks to maximize patient satisfaction and quality care measures while minimizing distance.
|>
<|expandable|expanded=True|
<|{ranks}|table|editable=False|page_size=5|>
|>
|>
|>
"""


def submit_button_action(state, id):
    # print(id)
    state.address_completed = True
    

def on_change(state, var, val):
    if var == "address_completed" and state.address_completed:
        # print("Address completed","\n", state.address)
        calculate_position(state, state.address)
    if var == "weights_correct" and state.weights_correct:
        state.weights = state.custom_weights['weights'].tolist()
        # print(state.weights)
        decision_making(state)
        
        

def calculate_position(state, address):
    geolocator = Nominatim(user_agent="HospitalSelector_v4")
    try:
        state.location = geolocator.geocode(address)
        print(state.location)
        if state.location == None:
            raise ValueError("Returned no location")
        # print(state.location.address, state.location.latitude, state.location.longitude)
        # print(state.location.raw)
        
        state.final_location = state.location.address
        state.found_address = True
        calculate_distance(state, state.location)
        
        
    except ValueError:
        state.found_address = False
        state.rankings_finished = False
        notify(state, notification_type="error", message="Address retrieval failed. Please make sure your address is valid and try again.", system_notification=True)

def calculate_distance(state, location):
    location_tup = (location.latitude, location.longitude)
    state.df['distance'] = state.df.apply(lambda x: geodesic((x.Latitude, x.Longitude), location_tup).km,axis=1)
    
    
    # with pd.option_context('display.max_rows', 15, 'display.max_columns', None):  # more options can be specified also
        # print(state.df)
        
    print(state.df.columns)
    
    state.matrix = state.df[['Patient Survey Star Rating', 'Score', "distance"]]
    state.matrix.rename(columns={'Patient Survey Star Rating': 'Patient Satisfaction', 'Score': 'Quality Care Measures', 'distance': "Distance"}, inplace=True)
    
    state.distance_completed = True
    
def edit_table(state, var, payload):
    print(payload)
    index = payload['index']
    col = payload['col']
    val = payload['value']
    temp = state.custom_weights.copy()
    temp.loc[index, col] = val
    test = pd.to_numeric(temp[col], errors='coerce').isnull().any()
    if test:
        notify(state, notification_type="error", message="Weights are incorrect. Please check your weights are of numeric types.")
    else:
        state.custom_weights = temp
    
def table_submit_action(state, id):
    check_weights = (state.custom_weights['weights'] < 0).any()
    if not check_weights:
        state.weights_correct = True
    else:
        notify(state, notification_type="error", message="Weights are incorrect. Please check your weights are positive.", system_notification=True)

def decision_making(state):
    # print("decision making called")
    # print(state.matrix)
    # print(objectives)
    # print(state.weights)
    # print(state.matrix.index)
    # print(state.matrix.isnull().sum().sum())
    dm = skc.mkdm(
        state.matrix, 
        objectives, 
        weights=state.weights, 
        alternatives=state.matrix.index,
        criteria=['Patient Satisfaction', 'Quality Care Measures', 'Distance'])
    # print(dm)
    inverter = invert_objectives.InvertMinimize()
    dmt = inverter.transform(dm)
    # print(dmt)
    scaler = scalers.SumScaler(target="both")
    dmt = scaler.transform(dmt)
    # print(dmt)
    dec = simple.WeightedSumModel()
    rank = dec.evaluate(dmt).to_series()
    rank.sort_values(ascending=True, inplace=True)
    # print(rank)
    rank_indexes = rank.index.tolist()
    # print(rank_indexes)
    
    state.ranks = state.df.loc[rank_indexes, ['Name', 'Phone Number']].copy()
    # print(state.ranks)
    state.ranks['Rank'] = rank.values
    reordered_indexes = state.ranks.columns.tolist()
    reordered_indexes = reordered_indexes[-1:] + reordered_indexes[:-1]
    state.ranks = state.ranks[reordered_indexes]
    # state.ranks = pd.DataFrame({'test': [1, 2, 3]})
    # print(state.ranks)
    state.rankings_finished = True
    
stylekit = {
    "color_background_light": "#efedf5",
    "color_paper_light": "#bcbddc"
}    

Gui(page=page).run(use_reloader=True, dark_mode=True, stylekit=stylekit, debug=True)