import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import SearchVideos
import youtube_dl


scope = "user-library-read"

print()
print("SpotifyMP3Tube by")

print("   ___  ___       __  ____ ____")
print("  / _ \/ _ \__ __/ /_/ __// __/")
print(" / , _/ // / // / __/ _ \/ _ \ ")
print("/_/|_|\___/\_,_/\__/\___/\___/ ")
print()

print("Digite o seu nome de usuário do Spotify: ")
user = input(">> ")

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope, client_id='SEU_CLIENT_ID_AQUI', client_secret='SEU_CLIENT_SECRET_AQUI',  redirect_uri='http://127.0.0.1:9090', username=user))

playlists = sp.user_playlists(user)
lista_playlists=[] #nome, uri

while playlists:
    print()
    print("Playlists disponíveis: ")
    print()
    print("   ID  |  Nome")
    for i, playlist in enumerate(playlists['items']):
        print(f"   {str(i).zfill(2)} ....{playlist['name']}") #playlist['uri']

        lista_playlists.append([playlist['name'], playlist['uri']])


    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
print()
id_desejado = int(input("Digite o ID da playlist desejada: "))
print()
print(f"Efetuando o download de \"{lista_playlists[id_desejado][0]}\" ...")
print()

uri_playlist = lista_playlists[id_desejado][1]

playlist = sp.user_playlist(user, uri_playlist)
tracks = playlist['tracks']
songs = tracks['items']

nome_musicas = []

for i in range (len(songs)):
    try:
        if songs[i]['track']['id'] != None:
            nome_musicas.append(f"{songs[i]['track']['album']['artists'][0]['name']} {songs[i]['track']['name']} audio")
    except:
        None

links_musicas = []
for i in range(len(nome_musicas)):
    links_musicas.append(SearchVideos(nome_musicas[i], offset = 1, mode = "json", max_results = 1).result().split('link": "')[1].split('"')[0])

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{lista_playlists[id_desejado][0]}/%(title)s.%(etx)s',
    'quiet': False,
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(links_musicas)




