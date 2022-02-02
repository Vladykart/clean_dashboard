import pandas as pd
from settings.settings import LOCAL_DATA_PATH
import streamlit as st


def load_excel_data(filename):
    return pd.read_excel(
        # LOCAL_DATA_PATH.joinpath(filename),
        filename,
        converters={'date': pd.to_datetime},
    )


def prepare_data(df):
    def lowercase(x): return str(x).lower()
    df[['lat', 'long']] = list(
        df['coordinates'].str.replace(r'[()]', '', regex=True).str.split(','))
    df = df.drop(['coordinates'], axis=1)
    df[['lat', 'lon']] = df[['lat', 'long']].astype('float64')
    df.rename(lowercase, axis='columns', inplace=True)
    df['region'] = df['region'].apply(lowercase)
    return df


def group_data(df):
    return df.groupby(by=['region', 'site', 'date'])


@st.cache
def load_and_prepare_data(filename):
    data = load_excel_data(filename)
    data = prepare_data(data)
    # grouped_data = group_data(data)
    return data
