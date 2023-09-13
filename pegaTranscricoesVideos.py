import nltk
import unidecode
nltk.download('stopwords')
from nltk.corpus import stopwords
from youtube_transcript_api import YouTubeTranscriptApi

def remover_acentos_caracteres_especiais(texto):
    texto_sem_acentos = unidecode.unidecode(texto)
    return ''.join(e for e in texto_sem_acentos if (e.isalnum() or e.isspace()))

def obter_transcricao_sem_stopwords(video_id):
    data = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    stopwords_lista = set(stopwords.words('portuguese'))
    resultado = []

    for index in data:
        palavras = index['text'].split()
        for palavra in palavras:
            palavra_sem_acentos = remover_acentos_caracteres_especiais(palavra)
            resultado.append(palavra_sem_acentos)
            
    resultado = [palavra for palavra in resultado if palavra.lower() not in stopwords_lista]
    return resultado
