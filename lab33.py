import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import pydeck as pdk
import altair as alt
import datetime

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# Add some markdown
st.sidebar.markdown("Made with love using [Streamlit](https://streamlit.io/).")
st.sidebar.markdown("# :chart_with_upwards_trend:")

# Add app title
st.sidebar.title("Visualization App")
#naming the datasets
ny = pd.read_csv("C:/Users/Aicha Nzeket/Desktop/M1 EFREI/Dataviz/ny-trips-data.csv")
uber = pd.read_csv("C:/Users/Aicha Nzeket/Desktop/M1 EFREI/Dataviz/uber-raw-data-apr14.csv")

# LOADING DATA
uber['Date/Time'] = uber['Date/Time'].map(pd.to_datetime)
DATE_TIME = "date/time"
DATA_URL = (
    "C:/Users/Aicha Nzeket/Desktop/M1 EFREI/Dataviz/uber-raw-data-apr14.csv "
)

st.header('NY Trips Dashboards')
st.info('Welcome to your visualization page')

#the progress bar 
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
# Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
bar.progress(i + 1)
time.sleep(0.1)
'...Your data is loaded!'
#uploading the uber dataset
@st.cache
def load_data1():
    uber = pd.read_csv("C:/Users/Aicha Nzeket/Desktop/M1 EFREI/Dataviz/uber-raw-data-apr14.csv")
    #Convert date/time column type from object to datetime
    uber['Date/Time'] = pd.to_datetime(uber['Date/Time'])
    lowercase = lambda x: str(x).lower()
    uber.rename(lowercase, axis='columns', inplace=True)
    return uber
df = load_data1()

@st.cache
def load_data(): 
    ny = pd.read_csv("C:/Users/Aicha Nzeket/Desktop/M1 EFREI/Dataviz/ny-trips-data.csv")
    return ny
df = load_data()

#the checkbox on the sidebar
mon_choix = st.sidebar.selectbox("",
        ["uber-raw-data-apr14", "ny-trips-data"])

if mon_choix == "ny-trips-data":
        load_data()
        if st.checkbox('Show the dataset'):
            st.write(ny.head())
#first histogram
        st.subheader("The proportion of tip in the total amount")
        chart_data = pd.DataFrame(ny[:40], columns=["total_amount", "tip_amount"])
        st.area_chart(chart_data)
#second histo
        st.subheader("The correlation between the distance and the fee")
        df = pd.DataFrame(ny[:200], columns = ["trip_distance","fare_amount"])
        st.line_chart(df)
#third one
        st.subheader("Total of amount")
        @st.cache(suppress_st_warning=True)
        def the_amount():
            plt.figure(figsize = (20, 10))
            plt.hist(ny["total_amount"],bins=70,range=(0, 100), rwidth=0.8)
            plt.xlabel('Amount paid')
            plt.ylabel('Frequency')
            plt.title('Cash evolution')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()        
        the_amount()
    #comment obtenir les dates et les heures
        ny['tpep_pickup_datetime'] = ny['tpep_pickup_datetime'].map(pd.to_datetime)
        ny['tpep_dropoff_datetime'] = ny['tpep_dropoff_datetime'].map(pd.to_datetime)
        ny['pickup_day'] = ny['tpep_pickup_datetime'].dt.day
        ny['pickup_hour'] = ny['tpep_pickup_datetime'].dt.hour
        ny['dropoff_day'] = ny['tpep_dropoff_datetime'].dt.day
        ny['dropoff_hour'] = ny['tpep_dropoff_datetime'].dt.hour
        st.write(ny.head())
#évolution des courses par heure
        st.title('Daily Trips in NY')
        st.write("You have the opportunity to see the evolution of the total amount paid")
        st.subheader("The total amount paid")
        chart_data = pd.DataFrame(ny[:40], columns=["total_amount"])
        st.area_chart(chart_data)
elif mon_choix == "uber-raw-data-apr14":
    load_data1()
    if st.checkbox('Show the dataset'):
        st.write(uber.head())

    if st.checkbox('Show the map of the position of your clients'):
        st.map(uber)
    #convertir les dates 
    uber['Date/Time'] = uber['Date/Time'].map(pd.to_datetime)
    uber['Day'] = uber['Date/Time'].dt.day
    uber['Hour'] = uber['Date/Time'].dt.hour
    @st.cache(suppress_st_warning=True)
    def the_uber_trips():
        plt.figure(figsize = (20, 10))
        plt.hist(uber["Day"],bins=50,range=(0, 30), rwidth=0.8)
        plt.xlabel('Days of the month')
        plt.ylabel('Frequency')
        plt.title('This is the evolution of the trips on a daily basis')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()        
    the_uber_trips()

#interactive maps for uber Trips in Paris 
# LOADING DATA
    DATE_TIME = "date/time"
    DATA_URL = (
        "C:/Users/Aicha Nzeket/Desktop/M1 EFREI/Dataviz/uber-raw-data-apr14.csv"
    )

    @st.cache(persist=True)
    def load_data2(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis="columns", inplace=True)
        data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
        return data

    data = load_data2(100000)

# CREATING FUNCTION FOR MAPS

    def map(data, lat, lon, zoom):
        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
    row1_1, row1_2 = st.columns((2,3))

    with row1_1:
        st.title("NYC Uber Ridesharing Data")
        hour_selected = st.slider("Select hour of pickup", 0, 23)

    with row1_2:
        st.write(
    """
    ##
    Examining how Uber pickups vary over time in NYC and at its most famous spots.
    By sliding the slider on the left you can view different slices of time and explore different trends for ypur vacation.
    """)

# FILTERING DATA BY HOUR SELECTED
    data = data[data[DATE_TIME].dt.hour == hour_selected]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    row2_1, row2_2, row2_3, row2_4 = st.columns((2,1,1,1))

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    la_guardia= [40.7900, -73.8700]
    jfk = [40.6650, -73.7821]
    newark = [40.7090, -74.1805]
    zoom_level = 12
    midpoint = (np.average(data["lat"]), np.average(data["lon"]))

    with row2_1:
        st.write("**All NYC from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
        map(data, midpoint[0], midpoint[1], 11)

    with row2_2:
        st.write("**LGA**")
        map(data, la_guardia[0],la_guardia[1], zoom_level)

    with row2_3:
        st.write("**JFK**")
        map(data, jfk[0],jfk[1], zoom_level)

    with row2_4:
        st.write("**EWR**")
        map(data, newark[0],newark[1], zoom_level)

# FILTERING DATA FOR THE HISTOGRAM
    filtered = data[
        (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
        ]

    hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

    chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

# LAYING OUT THE HISTOGRAM SECTION

    st.write("")

    st.write("**Breakdown of rides per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

    st.altair_chart(alt.Chart(chart_data)
        .mark_area(
            interpolate='step-after',
        ).encode(
            x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("pickups:Q"),
            tooltip=['minute', 'pickups']
        ).configure_mark(
            opacity=0.5,
            color='orange'
        ), use_container_width=True) 

    st.subheader("The evolution of trips day by day")
    st.write ("Can you please show up?")

