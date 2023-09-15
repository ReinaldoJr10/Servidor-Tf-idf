import concurrent.futures
from pytube import YouTube, contrib
import json
import pegaTranscricoesVideos
from functools import partial

def get_video_ids_playlist(playlist_id):
    try:
        playlist = f"https://www.youtube.com/playlist?list={playlist_id}"
        videos = contrib.playlist.Playlist(playlist)
        video_urls = videos.video_urls
        return video_urls
    except Exception as e:
        print("Ocorreu um erro:", e)
        return []

def video_info_id_transcricao(playlist,video_id):
    try:
        video_url = f"{video_id}"
        yt = YouTube(video_url)

        lista = pegaTranscricoesVideos.obter_transcricao_sem_stopwords(yt.video_id) 
        if(lista==None):
            print("aqui"+video_id)
        video_info = {
            "Autor":yt.author,
            "Data de publicacao": str(yt.publish_date),
            "Duracao": yt.length,
            "Id da Playlist": playlist,
            "Id do video": yt.video_id,
            "Palvras-chave":yt.keywords,
            "Titulo": yt.title,
            "URL da miniatura": yt.thumbnail_url,
            "URL do video": video_url,
            "Visualizacoes": yt.views,
            "Transcricao": lista
        }
        print(len(lista))
        return video_info
    except Exception as e:
        print("Ocorreu um erro:", e)
        video_info = {
            "Autor":yt.author,
            "Data de publicacao": str(yt.publish_date),
            "Duracao": yt.length,
            "Id da Playlist": playlist,
            "Id do video": yt.video_id,
            "Palvras-chave":yt.keywords,
            "Titulo": yt.title,
            "URL da miniatura": yt.thumbnail_url,
            "URL do video": video_url,
            "Visualizacoes": yt.views,
            "Transcricao": " "
        }
        return video_info

def video_info_id(playlist,video_id):
    try:
        video_url = f"{video_id}"
        yt = YouTube(video_url)

        video_info = {
            "Autor":yt.author,
            "Data de publicacao": str(yt.publish_date),
            "Duracao": yt.length,
            "Id da Playlist": playlist,
            "Id do video": yt.video_id,
            "Palvras-chave":yt.keywords,
            "Titulo": yt.title,
            "URL da miniatura": yt.thumbnail_url,
            "URL do video": video_url,
            "Visualizacoes": yt.views,
        }
        return video_info
    except Exception as e:
        print("Ocorreu um erro:", e)
        video_info = {
            "Autor":yt.author,
            "Data de publicacao": str(yt.publish_date),
            "Duracao": yt.length,
            "Id da Playlist": playlist,
            "Id do video": yt.video_id,
            "Palvras-chave":yt.keywords,
            "Titulo": yt.title,
            "URL da miniatura": yt.thumbnail_url,
            "URL do video": video_url,
            "Visualizacoes": yt.views,
        }
        return video_info


def processa_video_transcricao(playlist,video_id):
    try:
        video_data = video_info_id_transcricao(playlist,video_id)
        print(f'Vídeo processado e salvo no banco de dados {video_id}')    
        return video_data   
    except Exception as e:
            print("Ocorreu um erro na conexão com o banco de dados:", e)

def processa_video(playlist, video_id):
    try:
        video_data = video_info_id(playlist, video_id)
        print(f'Vídeo processado e salvo no banco de dados {video_id}')
        return video_data
    except Exception as e:
        print("Ocorreu um erro na conexão com o banco de dados:", e)

def processa_dados_transcricao():
    lista_playlist_id = ["PLvE-ZAFRgX8hnECDn1v9HNTI71veL3oW0",
                     "PLpaKFn4Q4GMOBAeqC1S5_Fna_Y5XaOQS2",
                     "PLHz_AreHm4dkBs-795Dsgvau_ekxg8g1r"]  
    lista_videos_playlist=[]

    for playlist_id in lista_playlist_id:
        video_urls = get_video_ids_playlist(playlist_id)
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            resultados = list(executor.map(partial(processa_video_transcricao, playlist_id), video_urls))

        print("Processamento concluído!"+str(playlist_id))

        objeto_json = {playlist_id: resultados}
        lista_videos_playlist.append(objeto_json)

    with open("BancoBusca.json", "w") as arquivo_json:
        json.dump(lista_videos_playlist, arquivo_json, indent=4)
    print("Arquivo 'BancoBusca.json' criado com sucesso!")


def processa_dados():
    lista_playlist_id = ["PLvE-ZAFRgX8hnECDn1v9HNTI71veL3oW0",
                         "PLpaKFn4Q4GMOBAeqC1S5_Fna_Y5XaOQS2",
                         "PLHz_AreHm4dkBs-795Dsgvau_ekxg8g1r"]
    lista_playlist_nome = ["Curso Python",
                           "Curso C",
                           "Curso Mysql"]
    lista_videos_playlist = []

    cont=0

    for playlist_id in lista_playlist_id:
        video_urls = get_video_ids_playlist(playlist_id)
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            resultados = list(executor.map(partial(processa_video, playlist_id), video_urls))

        print("Processamento concluído!" + str(playlist_id))

        objeto_json = {
            playlist_id: resultados,
            "nome": lista_playlist_nome[cont]
                       }
        lista_videos_playlist.append(objeto_json)
        cont+=1

    with open("playlist.json", "w") as arquivo_json:
        json.dump(lista_videos_playlist, arquivo_json, indent=4)
    print("Arquivo 'playlist.json' criado com sucesso!")

processa_dados()