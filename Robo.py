import datetime
import os
import random
import re
import shutil
import time

import pytz
import requests
import tweepy


class Robo:
    """
    Este é o robô com suas funções pré-determinadas para efetuar a autenticação e publicação de Tweets com imagens e vídeos.
    """

    def __init__(self, nome, versao):
        """
        Função chamada ao iniciar o robô, aqui será definido seu nome e sua versão.
        """
        super().__init__()
        self.nome = nome
        self.versao = versao
        print("{} ligando na versão {}!".format(self.nome, str(self.versao)))

    def __del__(self):
        """
        Quando o robô for "deletado" aparecerá uma mensagem.
        """
        print("{} desligando...".format(self.nome))

    def __repr__(self):
        """
        Quando o objeto classe Robo for chamado retornará seu nome e sua versão.
        """
        return "{} ({})".format(self.nome, str(self.versao))

    def configurar_autenticacao(
        self, consumer_key, consumer_secret_key, access_token, access_token_secret
    ):
        """
        Receberá as chaves de autenticação para realizar a autenticação no Twitter.
        """
        self.consumer_key = consumer_key
        self.consumer_secret_key = consumer_secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        print("Chaves configuradas com sucesso.")

    def iniciar_robo(self):
        """
        Irá iniciar o robô com as chaves recebidas, caso ocorra algum erro será mostrado.
        """
        autenticacao = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret_key)
        autenticacao.set_access_token(self.access_token, self.access_token_secret)
        try:
            self.api = tweepy.API(autenticacao)
            print("Robô iniciado!")
        except Exception as e:
            print("Ocorreu um erro ao iniciar o robô.")
            print("Erro: {}".format(str(e)))

    def postar_meme(self):
        """
        Ao ser chamada irá selecionar randomicamente algum meme da pasta Memes e irá enviar ao Twitter, em seguida apagará da pasta Memes.
        """
        trends = [
            trend["name"] for trend in self.api.trends_place(23424768)[0]["trends"][0:5]
        ]
        while True:
            memes = os.listdir("Memes")
            if len(memes) <= 0:
                print("Não há memes para ser postado.")
                break
            else:
                meme_arquivo = random.choice(memes)
                try:
                    twitter_meme_id = self.api.media_upload("Memes/" + meme_arquivo)
                    self.api.update_status(
                        status=" ".join(trends),
                        media_ids=[twitter_meme_id.media_id_string],
                    )
                    print("Um meme foi postado.")
                    os.remove("Memes/" + meme_arquivo)
                    break
                except Exception as e:
                    print("Não foi possível postar o meme.")
                    print("Erro: {}".format(str(e)))
                    os.remove("Memes/" + meme_arquivo)

    def mecanismo(self):
        """
        Ao ser chamada irá iniciar um evento infinito que irá verificar o horário de acordo com a postagem de memes do iFunny.
        Caso o horário bata com a postagem de novos memes no iFunny (08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00) irá baixar os 20 novos memes e de 6 em 6 minutos irá postá-los no Twitter.
        Por que 6 minutos? Pois no intervalo de 2 horas o iFunny posta 20 memes, ou seja, 2 horas são 120 minutos, 20 memes para serem postados em 2 horas são 120/20 = 6 minutos a cada meme.
        """
        self.ifunny = iFunny()
        while True:
            tempo = datetime.datetime.now()
            timezone = pytz.timezone("America/Sao_Paulo")
            tempo = tempo.astimezone(timezone)
            horarios_ifunny = [8, 10, 12, 14, 16, 18, 20, 22]
            minutos_postar = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54]
            if (
                tempo.hour in horarios_ifunny
                and tempo.minute == 0
                and tempo.second == 0
            ):
                self.ifunny.pegar_memes()
            if tempo.minute in minutos_postar and tempo.second == 0:
                self.postar_meme()


class iFunny:
    """
    Esta classe está determinada para criar a pasta onde salvar os últimos 20 memes (imagens/vídeos).
    """

    def __init__(self):
        """
        Ao criar o objeto será verificado a existência da pasta de memes, caso não exista irá cria-la.
        Caso a pasta exista, irá deleta-la e apagar todo seu conteúdo.
        """
        super().__init__()
        if not os.path.exists("Memes"):
            os.mkdir("Memes")
        else:
            shutil.rmtree("Memes")
            time.sleep(0.5)
            os.mkdir("Memes")

    def pegar_memes(self):
        """
        Chamando este método irá salvar os últimos 20 memes postados no iFunny BR dentro da pasta Memes.
        Caso ocorra algum erro, retornará False, caso contrário, retornará True.
        """
        pagina = requests.get(
            url="https://br.ifunny.co/",
            headers={
                "Host": "br.ifunny.co",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://br.ifunny.co/",
            },
        )
        if pagina.status_code == 200:
            print("Pegando memes no iFunny.")
            memes_id = re.findall(
                '<div class="post" data-id="(.*)"  data-test', pagina.text
            )[0:20]
            for meme_id in memes_id:
                meme_pagina = requests.get(
                    url="https://br.ifunny.co/picture/" + meme_id,
                    headers={
                        "Host": "br.ifunny.co",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Referer": "https://br.ifunny.co/",
                    },
                )
                if meme_pagina.status_code == 200:
                    meme_imagem_nome = re.search(
                        '<meta property="og:image" content="https://imageproxy.ifunny.co/crop:x-20,resize:320x,crop:x800,quality:90x75/images/(\w+.jpg)"/>',
                        meme_pagina.text,
                    ).group(1)
                    meme_imagem = requests.get(
                        "https://imageproxy.ifunny.co/crop:x-20/images/"
                        + meme_imagem_nome,
                        stream=True,
                    )
                    meme_salvar = open("Memes/" + meme_imagem_nome, "wb")
                    meme_imagem.raw.decode_content = True
                    shutil.copyfileobj(meme_imagem.raw, meme_salvar)
                    meme_salvar.close()
                elif meme_pagina.status_code == 404:
                    try:
                        meme_pagina = requests.get(
                            url="https://br.ifunny.co/video/" + meme_id,
                            headers={
                                "Host": "br.ifunny.co",
                                "Upgrade-Insecure-Requests": "1",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                "Sec-Fetch-Site": "same-origin",
                                "Sec-Fetch-Mode": "navigate",
                                "Sec-Fetch-User": "?1",
                                "Sec-Fetch-Dest": "document",
                                "Referer": "https://br.ifunny.co/",
                            },
                        )
                        meme_video_nome = re.search(
                            '<meta property="og:video:url" content="https://img.ifunny.co/videos/(\w+.mp4)"/>',
                            meme_pagina.text,
                        ).group(1)
                        meme_video = requests.get(
                            "https://img.ifunny.co/videos/" + meme_video_nome,
                            stream=True,
                        )
                        meme_salvar = open("Memes/" + meme_video_nome, "wb")
                        meme_video.raw.decode_content = True
                        shutil.copyfileobj(meme_video.raw, meme_salvar)
                        meme_salvar.close()
                    except:
                        pass
        else:
            print("Ocorreu algum erro ao acessar o iFunny.")
            return False


if __name__ == "__main__":
    mememaker = Robo(nome="Meme Maker", versao=1.0)
    mememaker.configurar_autenticacao(
        consumer_key="",
        consumer_secret_key="",
        access_token="",
        access_token_secret="",
    )
    mememaker.iniciar_robo()
    mememaker.mecanismo()
