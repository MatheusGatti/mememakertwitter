<div align="center">

# Meme Maker Twitter

Meme Maker é um robô desenvolvido em Python com o intuito de publicar diversos vídeos e imagens engraçadas no Twitter.

[![GitHub issues](https://img.shields.io/github/issues/MatheusGatti/mememakertwitter)](https://github.com/MatheusGatti/mememakertwitter/issues) [![GitHub forks](https://img.shields.io/github/forks/MatheusGatti/mememakertwitter)](https://github.com/MatheusGatti/mememakertwitter/network) [![GitHub stars](https://img.shields.io/github/stars/MatheusGatti/mememakertwitter)](https://github.com/MatheusGatti/mememakertwitter/stargazers) [![GitHub license](https://img.shields.io/github/license/MatheusGatti/mememakertwitter)](https://github.com/MatheusGatti/mememakertwitter/blob/master/LICENSE)

</div>


### Como usar

Passos para utilizar o robô:

> Utilize o Python 3.7.5

- Clone este repositório ([passo a passo para clonar um repositório](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository "passo a passo para clonar um repositório"))

- Instale as dependências necessárias com os seguintes comandos:

```
pip install pytz
pip install requests
pip install git+https://github.com/conversocial/tweepy.git@video_upload2
```

- Abra o arquivo `Robo.py` e configure as seguintes entradas de acordo com seu gosto e suas chaves do Twitter:

```
nome="NOME DO SEU ROBÔ" (str)
versao=1.0 (int)
consumer_key="TWITTER CONSUMER KEY" (str)
consumer_secret_key="TWITTER CONSUMER SECRET KEY" (str)
access_token="TWITTER APP ACCESS TOKEN" (str)
access_token_secret="TWITTER APP TOKEN SECRET" (str)
```

- Não sabe onde encontrar suas chaves do Twitter? Crie uma conta de desenvolvedor no Twitter e depois crie um app clicando [aqui](https://developer.twitter.com/en/apps "aqui"), em seguida irão disponibilizar as suas chaves.

- Finalmente o último passo, basta executar o script.

`python Robo.py`


### Como funciona

- Quando o robô for iniciado irá ser criado uma pasta chamada `Memes` - não apague-a pois faz parte do robô - onde será salvo imagens e vídeos engraçados capturados do site [iFunny](https://br.ifunny.co/ "iFunny") em determinados horários - esses horários são horários de atualização das postagens do site - e a cada 6 minutos será selecionado uma imagem ou um vídeo aleatório para ser postado no Twitter.


### Erros e problemas

- Caso ocorra algum erro não hesite em alertar, abra uma "questão" clicando [aqui](https://github.com/MatheusGatti/mememakertwitter/issues/new "aqui").


### Contribuições

- Caso você tenha alguma ideia, deposite-a [aqui](https://github.com/MatheusGatti/mememakertwitter/issues/new "aqui").
- Caso deseja corrigir algum erro/bug, você pode encontrar questões abertas [aqui](https://github.com/MatheusGatti/mememakertwitter/issues "aqui").
