import forecast as forecast
import streamlit as st
from map_layer import draw_map
import numpy as np
from preparation import data_praparation as dprep, data_praparation


# -- Set page config
app_title = 'Stations map'
st.set_page_config(page_title=app_title, page_icon=":eyeglasses:")

# -- Default detector list
page_list = ['map', 'station', 'V1']
# -- Choose page
page = st.sidebar.selectbox('Page', page_list)
uploaded_file = st.sidebar.file_uploader("Choose a file", type="xlsx")

if uploaded_file is not None:
    data = dprep.load_and_prepare_data(uploaded_file)
    data_load_state = st.sidebar.text('Loading data...')
    data_load_state.text("Done! (using st.cache)")
    st.sidebar.success('File was successfully uploaded')
else:
    st.warning('First you need to upload excel file')
    data = []

d = st.sidebar.date_input(
    "Select date",
    value=data['date'].max().date(),
    min_value=data['date'].min().date(),
    max_value=data['date'].max().date())

st.write('Selected date id: :', d)

if page == 'map':
    st.title('Stations map')
    choose_list = ('yeald', 'forecast', 'error',)
    choose_radio = st.sidebar.radio('Choose metric', choose_list)
    map_data = data.groupby(
        by=['date', 'site', 'region']).agg(
        {'yeild': 'sum',
         'forecast': 'sum',
         'error': 'mean',
         'lat': 'first',
         'lon': 'first'}).reset_index()

    map_data = map_data[map_data['date'] == d.strftime('%Y-%m-%d')]
    map_data['error'] = map_data['error'].abs()
    if st.checkbox(f'Show table for stations'):
        st.table(map_data)
    midpoint = (np.average(map_data["lat"]), np.average(map_data["lon"]))

    # match choose_radio:
    #     case 'forecast':
    #         forecast_map_data = map_data[['site', 'forecast', 'lat', 'lon']]
    #         draw_map(forecast_map_data, midpoint[0], midpoint[1], 5)
    #     case 'error':
    #         error_map_data = map_data[['site', 'error', 'lat', 'lon']]
    #         draw_map(error_map_data, midpoint[0], midpoint[1], 5)
    #     case _:
    #         yeild_map_data = map_data[['site', 'yeild', 'lat', 'lon']]
    #         draw_map(yeild_map_data, midpoint[0], midpoint[1], 5)

    if choose_radio == 'forecast':
        forecast_map_data = map_data[['site', 'forecast', 'lat', 'lon']]
        draw_map(forecast_map_data, midpoint[0], midpoint[1], 5)
    elif choose_radio == 'error':
        error_map_data = map_data[['site', 'error', 'lat', 'lon']]
        draw_map(error_map_data, midpoint[0], midpoint[1], 5)
    else:
        yeild_map_data = map_data[['site', 'yeild', 'lat', 'lon']]
        draw_map(yeild_map_data, midpoint[0], midpoint[1], 5)



    map_data = map_data.sort_values('yeild').set_index('site')

    st.bar_chart(map_data[['forecast', 'yeild', 'error']], width=1080)


elif page == 'station':
    st.title('Stations charts')
    # Title the app

    st.markdown("""
     * Use the menu at left to select data and set plot parameters
     * Your plots will appear below
    """)
    site = st.sidebar.multiselect(
        'Select station', data.site.unique(), help='choose station or stations', default=data.site.unique()[0])

    if site:
        for s in site:
            t_data = data[data['site'] == s]
            t_data = t_data.set_index('hour')
            t_data['error'] = t_data['error'].abs()
            t_data = t_data[t_data['date'] == d.strftime('%Y-%m-%d')]
            st.bar_chart(t_data[['forecast', 'yeild', 'error']])
            if st.checkbox(f'Show table for {s}'):
                st.table(t_data[['forecast', 'yeild', 'error']])





elif page == 'V1':
    pass