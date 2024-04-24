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
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend_songs(song_title, data, cosine_sim, top_n=10):
    # Check if the song is in the dataset
    if song_title not in data['song'].values:
        return f"No recommendations found: '{song_title}' is not in the dataset."

    # Find the index of the song that matches the title
    idx = data[data['song'] == song_title].index[0]

    # Get the pairwise similarity scores of all songs with that song
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the songs based on the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the top-n most similar songs
    sim_scores = sim_scores[1:top_n+1]

    # Get the song indices
    song_indices = [i[0] for i in sim_scores]

    # Return the top-n most similar songs
    return data['song'].iloc[song_indices]

# Load your data and cosine similarity matrix
data = pickle.load(open('df.pkl','rb'))
cosine_sim = pickle.load(open('similarity.pkl','rb'))


# Main Streamlit app
def main():
    st.title('Song Recommender')
    song = st.text_input('Enter a song title:')
    if st.button('Recommend'):
        recommendations = recommend_songs(song, data, cosine_sim)
        if isinstance(recommendations, str):
            st.write(recommendations)
        else:
            st.write('Top recommendations:')
            st.write(recommendations.tolist())

if __name__ == '__main__':
    main()