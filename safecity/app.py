import streamlit as st
import pandas as pd

st.title("AI Crime Prediction Dashboard")

df = pd.read_csv("data/crdata.csv")
st.map(df[["latitude", "longitude"]])

st.subheader("Crime Data")
st.dataframe(df)
