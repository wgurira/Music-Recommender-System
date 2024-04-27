import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend_songs(song_title, data, cosine_sim, top_n=10):
    song_title = song_title.strip()
    if song_title not in data['song'].values:
        return f"No recommendations found: '{song_title}' is not in the dataset."
    song_data = data[data['song'] == song_title]
    if song_data.empty:
        return f"No recommendations found: '{song_title}' is not properly indexed."
    idx = song_data.index[0]
    if idx >= len(cosine_sim):
        return f"Index error: Index {idx} out of range for cosine similarity matrix."
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    song_indices = [i[0] for i in sim_scores]
    recommended_songs = data.iloc[song_indices]
    return recommended_songs[['song', 'artist']]

# Load data and cosine similarity matrix
data = pickle.load(open('df.pkl','rb'))
cosine_sim = pickle.load(open('similarity.pkl','rb'))

def main():
    st.write("""
Members:
- Ahe's My Kind Of Girl
- Back In Love Again
- At Seventeen
- Look At Me
- Abide With Me
""")
    st.title('Music Recommendation System')
    st.write("""
Suggested Songs:
- Gurira Wesley P R204433P HAI
- Sendekera Cousins R207642E HAI
- Ryan Kembo R205723E HAI
- Cyprian Masvikeni R205537V HDSC
""")
    song = st.text_input("Enter a song title:")
    if st.button('See Recommendations'):
        recommendations = recommend_songs(song, data, cosine_sim)
        if isinstance(recommendations, str):
            st.write(recommendations)
        else:
            st.write('Top 10 recommendations:')
            cols_per_row = 4
            rows = [recommendations.iloc[i:i + cols_per_row] for i in range(0, len(recommendations), cols_per_row)]
            for row in rows:
                cols = st.columns(cols_per_row)
                for idx, (col, (index, data_row)) in enumerate(zip(cols, row.iterrows())):
                    with col:
                        album_cover_url = get_song_album_cover_url(data_row['song'], data_row['artist'])
                        st.image(album_cover_url, width=100)
                        st.write(f"{data_row['song']} by {data_row['artist']}")

if __name__ == '__main__':
    main()
