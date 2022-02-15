
import streamlit as st
from map_layer import draw_map
from preparation.data_praparation import aggregate_data
from settings.settings import LOCAL_DATA_PATH
from visualisations.visual import draw_piechart, draw_error_plot, draw_all_station_chart
import numpy as np
import pandas as pd
from preparation import data_praparation as dprep, data_praparation
from forecasting_metrics import evaluate_all

# -- Set page config
app_title = 'Stations map'
st.set_page_config(page_title=app_title, page_icon=":eyeglasses:", layout="wide")

# -- Default detector list
page_list = ['map', 'station', 'V1']
# -- Choose page
page = st.sidebar.selectbox('Page', page_list)
# uploaded_file = st.sidebar.file_uploader("Choose a file", type="xlsx")
uploaded_file = 'data/mart_operative_forecasting_results.csv'

if uploaded_file is not None:
    data = dprep.load_and_prepare_data(uploaded_file)
    aggregated_data = aggregate_data(data.copy())
    data_load_state = st.sidebar.text('Loading data...')
    data_load_state.text("Done! (using st.cache)")
    st.sidebar.success('File was successfully uploaded')
else:
    st.warning('First you need to upload excel file')
    data = []
    aggregated_data = []

d = st.sidebar.date_input(
    "Select date",
    value=data['date'].max().date(),
    min_value=data['date'].min().date(),
    max_value=data['date'].max().date())

st.write('Selected date id: :', d)

if page == 'map':
    col_1, col_2 = st.columns([19, 8])
    v_data = aggregated_data.loc[:, [d.strftime('%Y-%m-%d')], :]
    st.title('Stations map')
    choose_list = ('yeild', 'forecast', 'error',)
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
        with col_1:
            draw_map(forecast_map_data, midpoint[0], midpoint[1], 5)
    elif choose_radio == 'error':
        error_map_data = map_data[['site', 'error', 'lat', 'lon']]
        with col_1:
            draw_map(error_map_data, midpoint[0], midpoint[1], 5)
    else:
        yeild_map_data = map_data[['site', 'yeild', 'lat', 'lon']]
        with col_1:
            draw_map(yeild_map_data, midpoint[0], midpoint[1], 5)

    map_data = map_data.sort_values('yeild').set_index('site')
    with col_2:
        c = st.container()
        c.plotly_chart(draw_piechart(v_data).update_layout(width=550))
    col_3, col_4, col_5 = st.columns([16, 8, 8])
    with col_3:
        c1 = st.container()
        c1.plotly_chart(
            draw_all_station_chart(v_data, sort_by=choose_radio).update_layout(
                                                                               template='plotly_dark',
                                                                               paper_bgcolor='rgba(0,0,0,0)',
                                                                               plot_bgcolor='rgba(0,0,0,0)'
                                                                               ))
    with col_5:
        c2 = st.container()
        c2.plotly_chart(draw_error_plot(data.groupby(by=['hour']).agg('sum')).update_layout(
                                                                      template='plotly_dark',
                                                                      paper_bgcolor='rgba(0,0,0,0)',
                                                                      plot_bgcolor='rgba(0,0,0,0)'
                                                                      ))

    st.table(map_data)

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
            with st.expander(label=s):
                t_data = data[data['site'] == s]
                t_data = t_data.set_index('hour')
                t_data = t_data[t_data['date'] == d.strftime('%Y-%m-%d')]
                predicted = t_data['forecast'].abs()
                actual = t_data['yeild'].abs()
                t_aggregated_data = aggregated_data.loc[s, [d.strftime('%Y-%m-%d')], :]
                col_1, col_2 = st.columns([43, 100])

                with col_1:
                    st.table(t_data[['forecast', 'yeild', 'error']])
                with col_2:
                    c = st.container()
                    c.bar_chart(t_data[['forecast', 'yeild', 'error']], width=1080, height=400)
                    c.plotly_chart(draw_piechart(t_aggregated_data).update_layout(width=550))
                st.plotly_chart(draw_error_plot(t_data).update_layout(width=1000,
                                                                      height=600,
                                                                      template='plotly_dark',
                                                                      paper_bgcolor='rgba(0,0,0,0)',
                                                                      plot_bgcolor='rgba(0,0,0,0)'
                                                                      ))
                col_3, col_4 = st.columns([43, 100])
                with col_3:
                    e = evaluate_all(actual, predicted)
                    e = pd.DataFrame([e])
                    err = st.multiselect(
                        f'Error metrics for {s}: ', e.T.index.tolist(), help='choose error metrics',
                        default=['mae', 'rmse', 'mse'])
                with col_4:
                    st.table(e[err].T)

            # c.bar_chart(t_data[['error_shortage', 'error_excess']].abs(), width=1080, height=400)


elif page == 'V1':
    v_data = aggregated_data.loc[:, [d.strftime('%Y-%m-%d')], :]
    metrics_df = v_data.describe()
    choose_list = ('yeild', 'forecast', 'error_shortage', 'error_excess')
    col_1, col_2 = st.columns([1, 6])
    with col_1:
        choose_radio = st.radio('Choose sort metric', choose_list)
    with col_2:
        st.table(metrics_df)

    st.plotly_chart(
        draw_all_station_chart(v_data, sort_by=choose_radio).update_layout(width=1200,
                                                                           height=600,
                                                                           template='plotly_dark',
                                                                           paper_bgcolor='rgba(0,0,0,0)',
                                                                           plot_bgcolor='rgba(0,0,0,0)'
                                                                           ))
