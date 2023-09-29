import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, ano):
        self.url = f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/{ano}'

    def pegaLinkJogos(self):
        site = requests.get(self.url)
        soup = BeautifulSoup(site.text, 'html.parser')
        retornoJogos = []

        #Retorna a div de cada jogo do campeonato
        linksJogos = soup.find_all('a', class_='btn btn-xs btn-success m-t-5')

        #Salva o link dos jogos no array
        for x in linksJogos:
            retornoJogos.append(x['href'])
        return retornoJogos
    
    def pegaInformacaoJogo(self,urlJogo):
        site = requests.get(urlJogo)
        soup = BeautifulSoup(site.text, 'html.parser')

        idJogo = soup.find_all(class_='color-white block text-1')[0].text.strip()
        campeonato = soup.find_all(class_='color-white block')[0].text.strip()
        timeMandante = soup.find_all(class_='time-nome color-white')[0].text.strip()
        timeVisitante = soup.find_all(class_='time-nome color-white')[1].text.strip()
        golsMandante = soup.find_all(class_='time-gols block')[0].text.strip()
        golsVisitante = soup.find_all(class_='time-gols block')[1].text.strip()
        arbitro = soup.find_all(rel='noopener')[0].text.strip()
        estadio = soup.find_all(class_='text-2 p-r-20')[0].text.strip()
        data = soup.find_all(class_='text-2 p-r-20')[1].text.strip()
        horario = soup.find_all(class_='text-2 p-r-20')[2].text.strip()
        print(f'idJogo: {idJogo}')
        print(f'campeonato: {campeonato}')
        print(f'timeMandante: {timeMandante}')
        print(f'timeVisitante: {timeVisitante}')
        print(f'golsMandante: {golsMandante}')
        print(f'golsVisitante: {golsVisitante}')
        print(f'arbitro: {arbitro}')
        print(f'estadio: {estadio}')
        print(f'data: {data}')
        print(f'horario: {horario}')
        return
    
scrap = Scraper('2013')
ret = scrap.pegaLinkJogos()
scrap.pegaInformacaoJogo(ret[0])