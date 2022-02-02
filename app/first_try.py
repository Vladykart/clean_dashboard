import streamlit as st
from datetime import datetime as dt
import datetime
import pandas as pd

from preparation import data_praparation as dprep, data_praparation

st.title('Stations map')

uploaded_file = st.file_uploader("Choose a file", type="xlsx")

if uploaded_file is not None:
    data = dprep.load_and_prepare_data(uploaded_file)
    data_load_state = st.text('Loading data...')
    data_load_state.text("Done! (using st.cache)")
    st.success('File was successfully uploaded')
else:
    st.warning('First you need to upload excel file')

site = st.multiselect('Select station', data.site.unique())
d = st.date_input(
     "Select date",
     datetime.date(2022, 1, 1))
st.write('Selected date id: :', d)

if site:
    for s in site:
        t_data = data[data['site'] == s]
        t_data = t_data.set_index('hour')
        t_data = t_data[t_data['date'] == d.strftime('%Y-%m-%d')]
        st.bar_chart(t_data[['forecast', 'yeild', 'error']])
        if st.checkbox(f'Show table for {s}'):
            st.table(t_data[['forecast', 'yeild', 'error']])
