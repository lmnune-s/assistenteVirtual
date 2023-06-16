import os
import sys
import webbrowser
import pywhatkit

import speech_recognition as sr
import webbrowser as browser
from gtts import gTTS
from playsound import playsound
from requests import get
from translate import Translator
from datetime import datetime
from datetime import date
import locale


locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


def cria_audio(audio, mensagem, lang='pt-br'):
    tts = gTTS(mensagem, lang=lang)
    tts.save(audio)
    playsound(audio)
    os.remove(audio)


def monitora_audio():
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print('Diga, o que você precisa?')
            audio = recon.listen(source)
            try:
                mensagem = recon.recognize_google(audio, language='pt-br')
                mensagem = mensagem.lower()
                print('Você disse: ', mensagem)
                executa_comandos(mensagem)
                break
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
        return mensagem


def cotacao(moeda):
    requisicao = get(f'https://economia.awesomeapi.com.br/all/{moeda}-BRL')
    cotacao = requisicao.json()
    nome = cotacao[moeda]['name']
    data = cotacao[moeda]['create_date']
    valor = cotacao[moeda]['bid']
    cria_audio("cotacao.mp3", f"Cotação do {nome} em {data} é {valor}")


def tradutor(traducao):
    if traducao == 'inglês':
        traduz = Translator(from_lang="pt-br", to_lang='english')
        cria_audio("traducao.mp3", "O que você gostaria de traduzir para o inglês?")
        mensagem = monitora_audio()
        traduzido = traduz.translate(mensagem)
        cria_audio("traducao.mp3", f"A tradução de {mensagem} é")
        cria_audio("traducao_eng.mp3", traduzido, lang='en')
    elif traducao == 'português':
        traduz = Translator(from_lang="english", to_lang='pt-br')
        cria_audio("traducao.mp3", "O que você gostaria de traduzir para o português?")
        mensagem = monitora_audio()
        traduzido = traduz.translate(mensagem)
        cria_audio("traducao.mp3", f"A tradução de")
        cria_audio("traducao_eng.mp3", mensagem, lang='en')
        cria_audio('traducao_port.mp3', f"é {traduzido}")


def play_music(music_name):
    url = "https://www.youtube.com/results?search_query=" + music_name
    webbrowser.open(url)
    pywhatkit.playonyt(music_name)


def ask_music():
    cria_audio("musica.mp3", "O que você gostaria de ouvir?")
    mensagem = monitora_audio()
    play_music(mensagem)

def executa_comandos(mensagem):
    # fechar assistente
    if 'fechar assistente' in mensagem:
        sys.exit()

    # hora atual
    elif 'horas' in mensagem:
        hora = datetime.now().strftime('%H:%M')
        frase = f"Agora são {hora}"
        cria_audio('horas.mp3', frase)

    # dta atual
    elif 'dia' in mensagem:
        data = date.today().strftime('%d de %B de %Y')
        frase = f"Hoje é dia {data}"
        cria_audio('data.mp3', frase)

    # desligar o computador
    elif 'desligar computador' in mensagem and 'em um minuto' in mensagem:
        os.system("shutdown -s -t 60")
    elif 'desligar computador' in mensagem and 'em cinco minutos' in mensagem:
        os.system("shutdown -s -t 300")
    elif 'cancelar desligamento' in mensagem:
        os.system("shutdown -a")

    # pesquisa no google
    elif 'pesquisar' in mensagem and 'no google' in mensagem:
        mensagem = mensagem.replace('pesquisar', '')
        mensagem = mensagem.replace('no google', '')
        browser.open(f'https://google.com/search?q={mensagem}')

    # pesquisa no youtube
    elif 'pesquisar' in mensagem and 'no youtube' in mensagem:
        mensagem = mensagem.replace('pesquisar', '')
        mensagem = mensagem.replace('no youtube', '')
        browser.open(f'https://youtube.com/results?search_query={mensagem}')

    # spotify
    # elif 'ouvir' in mensagem and 'música' in mensagem:
    #     browser.open('https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz')

    # ouvir musica no youtube
    elif 'ouvir' in mensagem and 'música' in mensagem:
        ask_music()


    # cotação de moedas
    elif 'dólar' in mensagem:
        cotacao('USD')
    elif 'euro' in mensagem:
        cotacao('EUR')
    elif 'bitcoin' in mensagem:
        cotacao('BTC')


    # abrir programas do computador
    elif 'abrir' in mensagem and 'google chrome' in mensagem:
        os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    elif 'abrir' in mensagem and 'spotify' in mensagem:
        os.startfile("C:\\Users\\lmnun\\AppData\\Local\\Microsoft\\WindowsApps\\spotify.exe")
    elif 'abrir' in mensagem and 'discord' in mensagem:
        os.startfile("C:\\Users\\lmnun\\AppData\\Local\\Discord\\app-1.0.9012\\discord.exe")

    # abrir programas windows
    elif 'abrir' in mensagem and 'bloco de notas' in mensagem:
        os.system("notepad.exe")
    elif 'abrir' in mensagem and 'ferramenta de desenho' in mensagem:
        os.system("mspaint.exe")
    elif 'abrir' in mensagem and 'ferramenta de slides' in mensagem:
        os.system("powerpnt.exe")
    elif 'abrir' in mensagem and 'ferramenta de texto' in mensagem:
        os.system("winword.exe")

    # tradutor
    elif 'traduzir' in mensagem and 'inglês' in mensagem:
        tradutor('inglês')
    elif 'traduzir' in mensagem and 'português' in mensagem:
        tradutor('português')


def main():
    cria_audio("ola.mp3", "Olá sou Aridiene, sua assistente virtual! Em que posso ajudá-lo?")
    while True:
        monitora_audio()


main()
