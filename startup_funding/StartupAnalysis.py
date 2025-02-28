import streamlit as st 
import pandas as pd
import plotly.express as px

df = pd.read_csv("startup_cleaned.csv")
df['investors'] = df['investors'].fillna('Undisclosed')

def load_investor_details(investor):
    investor_df = df[df['investors'].str.contains(investor)]
    # investor_df.head()[['date','startup','vertical','city','round','amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(investor_df.head()[['date','startup','vertical','city','round','amount']])
    st.subheader("Biggest Investments")
    st.dataframe(investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False))
    big_series = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False)
    fig = px.bar(x=big_series.index, y=big_series.values, 
             title="Biggest Investments", 
             labels={'x': 'Startup', 'y': 'Amount'})
    st.plotly_chart(fig)

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One", ["Overall Analysis","StartUp Analysis","Investor Analysis"])

if option == "Overall Analysis":
    st.title("Overall Analysis")
elif option == "StartUp":
    st.sidebar.selectbox("Select One", sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
else:
    selected_investor = st.sidebar.selectbox("Select One", sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        st.title(selected_investor)
        load_investor_details(selected_investor)


