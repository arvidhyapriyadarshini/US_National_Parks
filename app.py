import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Change the page configuration
st.set_page_config(
    page_title="US National Parks - Data Dashboard",
    #page_icon="🌟",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

########################################################################################################################
st.title('US National Parks Dashboard')
st.markdown('Hello there! Welcome to explore the US National Park Dataset')
st.subheader('Dataset')
dataset_description = """
The dataset used for this project is from Kaggle: [United States National Parks Dataset](https://www.kaggle.com/datasets/thedevastator/the-united-states-national-parks). 
This dataset contains comprehensive information about national parks across the country. It includes details such as the state where each park is situated, the date of establishment, the park's total area, the annual count of recreation visitors, and a description highlighting the key features of each park.
"""
st.markdown(dataset_description)
st.write('---')
df = pd.read_csv('https://raw.githubusercontent.com/arvidhyapriyadarshini/US_National_Parks/main/USNationalPark_Dataset_Cleaned.csv', index_col=False)
df = df.drop(columns='Unnamed: 0')
#st.write(df)

# Define the values for the cards
park_count = "63 Parks"
state_count = "30 States"
acre_count = "52.4 Million Acres"
visitor_count = "92.3 Million"
# Create the boxes with centered metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("Parks")
    st.markdown("<h2 style='text-align: center;'>{}</h2>".format(park_count), unsafe_allow_html=True)
with col2:
    st.success("States")
    st.markdown("<h2 style='text-align: center;'>{}</h2>".format(state_count), unsafe_allow_html=True)
with col3:
    st.success("Land")
    st.markdown("<h2 style='text-align: center;'>{}</h2>".format(acre_count), unsafe_allow_html=True)
with col4:
    st.success("Visitors")
    st.markdown("<h2 style='text-align: center;'>{}</h2>".format(visitor_count), unsafe_allow_html=True)
st.write('---')
########################################################################################################################
#US Map
# Calculate the logarithm of the 'Acres' column
df['AcresLog'] = np.log(df['Acres'])
# Round the values in the 'AcresLog' column to two decimal places
df['AcresLog'] = df['AcresLog'].round(3)
# Create a scattermapbox trace with all the markers
fig_usmap = go.Figure(go.Scattermapbox(
    mode='markers',
    lon=df['Longitude'],
    lat=df['Latitude'],
    marker=go.scattermapbox.Marker(
        size=df['AcresLog'],
        color=df['Acres'],  # Set the marker color based on the 'Acres' column
        colorscale='aggrnyl',
        showscale=True,
        colorbar=dict(
            title='Acres'
        ),
        opacity=0.7
    ),
    text=df['Name'],
    hovertext=df[['Name', 'State', 'Acres']],
    hovertemplate='<b>%{hovertext[0]}</b><br>' +
                  'State: %{hovertext[1]}<br>' +
                  'Acres: %{hovertext[2]}'
))

# Add GeoJSON overlay for choropleth effect
fig_usmap.update_layout(
    mapbox=dict(
        style='open-street-map',
        center=dict(lon=-98.5, lat=39.8),
        zoom=3,
        layers=[
            dict(
                source='your_geojson_file.geojson',  # Replace with the path to your GeoJSON file
                type='fill',
                color='rgba(0, 0, 255, 0.2)',  # Set the color and opacity of the choropleth overlay
                below='traces'
            )
        ]
    ),
    margin=dict(r=0, t=0, l=0, b=0),
    width=1000,
    height=400,
)
#######################################################################################################################
#Bar Chart_Acres
# Add the sidebar
st.sidebar.title("@DataScienceChef")
st.sidebar.markdown("Vidhya Radhakrishnan")
st.sidebar.markdown("Hi there! Welcome to my dashboard, explore the details about the US Nation Park here! Happy Summer!")

# Get user input for the number of parks to compare from the sidebar
st.sidebar.title("Select number to view top parks by size")
num_parks = st.sidebar.slider("Select number of parks to compare", 10, 25, 5)

# Get the top parks based on the number selected
top_parks = df.nlargest(num_parks, 'Acres')
# Create the bar chart with horizontal orientation
fig_barchart = go.Figure(data=go.Bar(
    y=top_parks['Name'],
    x=top_parks['Acres'],
    orientation='h',
    marker_color='lightseagreen'
))
# Update layout and labels
fig_barchart.update_layout(
    title='Top {} Parks by Acres'.format(num_parks),
    xaxis_title='Acres',
    yaxis_title='Park Name'
)
# Display the figure in Streamlit
col5, col6 = st.columns([3, 2])
with col5:
    st.subheader("US National Parks Location")
    st.plotly_chart(fig_usmap, use_container_width=True )
with col6:
    st.subheader("Top Parks By Acres")
    st.plotly_chart(fig_barchart, use_container_width=True)
########################################################################################################################
#Donut Chart
state_counts = df['State'].value_counts()
fig_donut = go.Figure(go.Pie(
    labels=state_counts.index,
    values=state_counts.values,
    hole=0.7,
    textinfo='label',
    textposition='inside'
))
fig_donut.update_layout(
    title='Count of Parks in Each State',
    annotations=[dict(text='Parks by State', x=0.5, y=0.5, font_size=20, showarrow=False)],
    height=400,
    width=400,
)

#Line Chart
# Calculate the park counts by year of establishment
park_counts = df.groupby(df['Year Established'])['Name'].count()
# Create a line chart
fig_linechart = go.Figure(data=go.Scatter(
    x=park_counts.index,
    y=park_counts.values,
    mode='lines+markers',
    marker=dict(color='green'),  # Set the marker color
    line=dict(color='green')  # Set the line color
))

# Set chart title and labels
fig_linechart.update_layout(title='Number of Parks by Year of Establishment',
                  xaxis_title='Year',
                  yaxis_title='Number of Parks',
                  height=400,
                  width=800,
                  plot_bgcolor='#C8DBBE',  # Set the plot background color
                  #paper_bgcolor='#C8DBBE'
                    )

col3, col4 = st.columns([2, 2])
with col3:
    st.subheader('National Park Count By State')
    st.plotly_chart(fig_donut, use_container_width=True)
with col4:
    st.subheader("Line Chart")
    st.plotly_chart(fig_linechart, use_container_width=True)
st.write('---')

# Get unique park names
parks = df['Name'].unique()
# Add the sidebar
st.sidebar.title("Select Park")
selected_park = st.sidebar.selectbox("Park", parks)
# Filter the data based on the selected park
park_data = df[df['Name'] == selected_park]

# Create a container for the main section
st.subheader('National Park Details')
col1, col2 = st.columns([2, 2])
# Display park details in the main section
with col1:
    st.header(selected_park)
    for index, park in park_data.iterrows():
        st.write("State:", park['State'])
        st.write("Date Established:", park['Date Established'])
        st.write("Latitude:", park['Latitude'])
        st.write("Longitude:", park['Longitude'])
        st.write("Acres:", park['Area'])
        st.write("Recreation Visitors:", park['Recreation Visitors'])
        st.write("Description:", park['Description'])

# Create a map centered around the selected park
fig = px.scatter_mapbox(
    park_data,
    lat="Latitude",
    lon="Longitude",
    hover_name="Name",
    hover_data=["State", "Date Established"],
    zoom=5
)
fig.update_traces(marker=dict(size=10, color='green'))
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Display the map in the main section
with col2:
    st.write("Park Location")
    st.plotly_chart(fig, use_container_width=True)

st.write('---')
