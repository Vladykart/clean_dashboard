import pandas as pd
from settings.settings import LOCAL_DATA_PATH
import streamlit as st


def load_excel_data(filename):
    print(filename)
    return pd.read_csv(
        # LOCAL_DATA_PATH.joinpath(filename),
        filename,
        converters={'date': pd.to_datetime},
    )


def assign_shortage_excess_err(df):
    df = (df.assign(
        error_shortage=lambda x: x['error'].apply(lambda x : x if x < 0 else 0),
        error_excess=lambda x: x['error'].apply(lambda x : x if x > 0 else 0)
            ))
    return df


def prepare_data(df):
    def lowercase(x): return str(x).lower()
    df[['lat', 'lon']] = list(
        df['coordinates'].str.replace(r'[()]', '', regex=True).str.split(','))
    df = df.drop(['coordinates'], axis=1)
    df[['lat', 'lon']] = df[['lat', 'lon']].astype('float64')
    df.rename(lowercase, axis='columns', inplace=True)
    df['region'] = df['region'].apply(lowercase)
    df = assign_shortage_excess_err(df)
    return df


def group_data(df):
    return df.groupby(by=['region', 'site', 'date'])


@st.cache
def aggregate_data(df):
    df_g = df
    df_g = df_g.groupby(by=['site', 'date'])
    df_g = df_g.agg({'forecast': 'sum',
                               'yeild': 'sum',
                               'error_shortage': 'sum',
                               'error_excess': 'sum'})
    return df_g


@st.cache
def load_and_prepare_data(filename):
    data = load_excel_data(filename)
    data = prepare_data(data)
    # grouped_data = group_data(data)
    return data
