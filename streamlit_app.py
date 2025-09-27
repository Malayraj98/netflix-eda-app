import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# 1. Load data
# -------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/KIIT/netflix-eda/data/netflix_titles.csv")
    
    # Basic cleaning
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['country'] = df['country'].fillna('Unknown')
    df['genres'] = df['listed_in'].fillna('').apply(lambda s: [g.strip() for g in s.split(',')] if s else [])
    return df

df = load_data()

st.set_page_config(page_title="Netflix EDA Dashboard", layout="wide")

st.title("📊 Netflix EDA Dashboard")
st.markdown("Explore Netflix dataset interactively.")

# -------------------------------------------------------
# 2. Sidebar Filters
# -------------------------------------------------------
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

year_range = st.sidebar.slider(
    "Filter by Release Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2010, 2021)
)

df_filtered = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].between(year_range[0], year_range[1]))
]

st.sidebar.markdown(f"**Filtered Titles:** {df_filtered.shape[0]}")

# -------------------------------------------------------
# 3. Charts
# -------------------------------------------------------

# Movies vs TV Shows
st.subheader("Movies vs TV Shows")
type_counts = df_filtered['type'].value_counts()
fig1 = px.bar(
    type_counts,
    x=type_counts.index,
    y=type_counts.values,
    labels={'x': 'Type', 'y': 'Count'},
    color=type_counts.index
)
st.plotly_chart(fig1, use_container_width=True)

# Titles Added by Year
st.subheader("Titles Added to Netflix by Year")
year_counts = df_filtered['year_added'].value_counts().sort_index()
fig2 = px.bar(
    x=year_counts.index,
    y=year_counts.values,
    labels={'x': 'Year Added', 'y': 'Number of Titles'},
    color=year_counts.values
)
st.plotly_chart(fig2, use_container_width=True)

# Top Genres
st.subheader("Top 10 Genres")
g = df_filtered.explode('genres')
genre_counts = g['genres'].value_counts().head(10)
fig3 = px.bar(
    x=genre_counts.index,
    y=genre_counts.values,
    labels={'x': 'Genre', 'y': 'Count'},
    color=genre_counts.values
)
st.plotly_chart(fig3, use_container_width=True)

# Top Countries
st.subheader("Top 10 Countries")
country_counts = df_filtered['country'].value_counts().head(10)
fig4 = px.bar(
    x=country_counts.values,
    y=country_counts.index,
    orientation='h',
    labels={'x': 'Number of Titles', 'y': 'Country'},
    color=country_counts.values
)
st.plotly_chart(fig4, use_container_width=True)

# Show raw data toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(df_filtered.head(50))
