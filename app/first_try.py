import streamlit as st
from datetime import datetime as dt
import datetime
import pandas as pd

from preparation import data_praparation as dprep, data_praparation

st.title('Stations map')

uploaded_file = st.file_uploader("Choose a file", type="xlsx")
if uploaded_file is not None:
    data = dprep.load_and_prepare_data(uploaded_file)
    st.success('File was successfully uploaded')

else:
    st.warning('First you need to upload excel file')
    data = pd.DataFrame()
try:
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.

    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using st.cache)")

    site = st.multiselect('Select station', data.site.unique())
    d = st.date_input(
         "Select date",
         datetime.date(2022, 1, 1))
    st.write('Selected date id: :', d)

except Exception as e:
    st.error('Something went wrong')
    site = None

if site:
    for s in site:
        t_data = data[data['site'] == s]
        t_data = t_data.set_index('hour')
        t_data = t_data[t_data['date'] == d.strftime('%Y-%m-%d')]
        st.bar_chart(t_data[['forecast', 'yeild', 'error']])
        if st.checkbox(f'Show table for {s}'):
            st.table(t_data[['hour', 'forecast', 'yeild', 'error']])
else:
    pass