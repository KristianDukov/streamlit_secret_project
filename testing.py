from itertools import product
import pandas as pd
import streamlit as st
from datetime import date

segments = []
for i in range(1,8):
    segments.append(f'Segment_{i}')

channels = []
for i in range(1,8):
    channels.append(f'Channel_{i}')

hotels = []
for i in range(1,601):
    hotels.append(f'Hotel_{i}')

dates = pd.date_range(start='1/1/2023', end='31/12/2023')

@st.cache
def create_df(segments,channels,hotels,dates):
    df = pd.DataFrame(list(product(segments,channels,hotels,dates)), columns=['segments', 'channels', 'hotels', 'dates'])
    df['KPI_1']=1
    df['KPI_2']=2
    df['KPI_3']=3
    df['KPI_4']=4
    df['dates'] = pd.to_datetime(df['dates']).dt.date
    return df

df = create_df(segments,channels,hotels,dates)
tab1,tab2,tab3,tab4 = st.tabs(['KPI_1', 'KPI_2', 'KPI_3', 'KPI_4'])

dates  = st.sidebar.date_input(label='range', value = [date(2023,1,5), date(2023,1,10)],min_value=date(2023,1,1), max_value =date(2023,12,31))
# dates = st.sidebar.slider('Select dates', value = [date(2023,1,1), date(2024,1,1)] , format = "YYYY-MM-DD")
start_date = dates[0]
end_date = dates[1]

segments_selection = st.sidebar.multiselect(
    'Select Segment',
    segments, segments, help= 'Please Select one or multiple Segments')

channels_selection = st.sidebar.multiselect(
    'Select Channel',
    channels, channels, help= 'Please Select one or multiple Channels')

hotels_selection = st.sidebar.multiselect(
    'Select Hotels',
    hotels, help= 'Please Select one or multiple Hotels')

# TAB 1
percentage_change_tab1 = tab1.number_input('Enter percentage to adjust the KPI', min_value=None, max_value=None, value=0.00, key='tab_1')
filtered = df[(df['segments'].isin(segments_selection))& (df['channels'].isin(channels_selection)) & (df['hotels'].isin(hotels_selection)) & (df['dates']>=start_date) & (df['dates']<=end_date)].reset_index()
filtered['KPI_1']=filtered['KPI_1']*(1+percentage_change_tab1)
# tab1.snow()
tab1.write(filtered[['segments', 'channels', 'hotels', 'dates', 'KPI_1']].head(100))
if tab1.button('Submit Changes'):
    tab1.success('Changes Submitted')
# TAB 2   
percentage_change_tab2 = tab2.number_input('Enter percentage to adjust the KPI', min_value=None, max_value=None, value=0.00, key='tab_2')
filtered['KPI_2']=filtered['KPI_2']*(1+percentage_change_tab2)

tab2.write(filtered[['segments', 'channels', 'hotels', 'dates', 'KPI_2']].head(100))
tab3.write(filtered[['segments', 'channels', 'hotels', 'dates', 'KPI_3']].head(100))
tab4.write(filtered[['segments', 'channels', 'hotels', 'dates', 'KPI_4']].head(100))