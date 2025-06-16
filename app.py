import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("🎶 Songlist Dashboard")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("processed_cleandata.csv")

df = load_data()

st.write("## Preview Data")
st.dataframe(df.head())

# Sidebar filter
st.sidebar.header("Filter Data")
genres = df["playlist_genre"].dropna().unique().tolist()
selected_genre = st.sidebar.multiselect("Select Genre", genres, default=genres)

filtered_df = df[df["playlist_genre"].isin(selected_genre)]

# Show filtered data
st.write(f"### Filtered Data: {len(filtered_df)} Songs")
st.dataframe(filtered_df)

# Summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

# Plotting Top 10 Track Based on Popularity
st.subheader("Top 10 Track Based on Popularity")
top_tracks = filtered_df.sort_values(by='track_popularity', ascending=False).head(10)
st.write(top_tracks[['track_name', 'track_artist', 'track_popularity']])

# Plot: Distribution of Popularity
st.write("### Popularity Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df["track_popularity"], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# Plot: Average Popularity by Genre
st.write("### Average Popularity by Genre")
avg_popularity = filtered_df.groupby("playlist_genre")["track_popularity"].mean().sort_values(ascending=False)
st.bar_chart(avg_popularity)

# Plotting Track Popularity by Artist
st.subheader("Popularity by Artist")
popularity = filtered_df.groupby('track_artist')['track_popularity'].mean().sort_values(ascending=False).head(10)
st.bar_chart(popularity)

# Plotting Energy Distribution
st.subheader("Energy Distribution")
fig, ax = plt.subplots()
ax.hist(filtered_df['energy'], bins=20, color='skyblue', edgecolor='black')
ax.set_xlabel("Energy")
ax.set_ylabel("Count")
ax.set_title("Distribusi Energy pada Playlist")
st.pyplot(fig)

# Correlation Analysis
st.subheader("Correlation Analysis")
corr = filtered_df.corr(numeric_only=True)
fig, ax = plt.subplots()
sns.heatmap(corr, cmap='coolwarm', annot=False, ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)