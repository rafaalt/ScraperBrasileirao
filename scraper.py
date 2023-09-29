import requests
from bs4 import BeautifulSoup
import pandas as pd
class Scraper:
    def __init__(self, ano, serie):
        self.url = f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-{serie.lower()}/{ano}'
        self.ano = ano

    def pegaLinkJogos(self):
        site = requests.get(self.url)
        soup = BeautifulSoup(site.text, 'html.parser')
        retornoJogos = []

        #Retorna a div de cada jogo do campeonato
        linksJogos = soup.find_all('a', class_='btn btn-xs btn-success m-t-5')

        #Salva o link dos jogos no array
        for x in linksJogos:
            retornoJogos.append(x['href']+"#arbitros")
        return retornoJogos
    
    def pegaInformacaoJogo(self,urlJogo):
        site = requests.get(urlJogo)
        soup = BeautifulSoup(site.text, 'html.parser')

        idJogo = soup.find_all(class_='color-white block text-1')[0].text.strip().split(':')[1]
        campeonato = soup.find_all(class_='color-white block')[0].text.strip().split('-')[1]
        timeMandante = soup.find_all(class_='time-nome color-white')[0].text.strip()
        timeVisitante = soup.find_all(class_='time-nome color-white')[1].text.strip()
        golsMandante = soup.find_all(class_='time-gols block')[0].text.strip()
        golsVisitante = soup.find_all(class_='time-gols block')[1].text.strip()
        arbitros = soup.find_all(rel='noopener')[0].text.replace('\n', '').strip().split('(')
        arbitro = arbitros[0].strip()
        if len(arbitros) > 1:
            arbitro += ' (FIFA)'
        estadio = soup.find_all(class_='text-2 p-r-20')[0].text.strip().split('-')[0]
        cidade = soup.find_all(class_='text-2 p-r-20')[0].text.strip().split('-')[1]
        estado = soup.find_all(class_='text-2 p-r-20')[0].text.strip().split('-')[2]
        data = soup.find_all(class_='text-2 p-r-20')[1].text.strip().split('de')
        dia = data[0].split(',')[1]
        mes = data[1]
        ano = data[2]
        rodada = int((int(idJogo)-1)/10)+1
        horario = soup.find_all(class_='text-2 p-r-20')[2].text.strip()
        pontosMandante, pontosVisitante = self.resultadoJogo(golsMandante, golsVisitante)
        informacoes_jogo = {
            'idJogo': (self.ano + '0' + idJogo).replace(' ',''),
            'campeonato': campeonato,
            'ano': ano,
            'rodada': rodada,
            'timeMandante': timeMandante,
            'timeVisitante': timeVisitante,
            'golsMandante': golsMandante,
            'golsVisitante': golsVisitante,
            'arbitro': arbitro,
            'arbitroVAR': '',
            'estadio': estadio,
            'cidade': cidade,
            'estado': estado,
            'dia': dia,
            'mes': mes,
            'horario': horario,
            'pontosMandante': pontosMandante,
            'pontosVisitante': pontosVisitante,
        }
        return informacoes_jogo
    
    def resultadoJogo(self,golsMandante, golsVisitante):
        ptsMandante = 0
        ptsVisitante = 0
        if(golsMandante > golsVisitante):
            ptsMandante = 3
        elif(golsVisitante > golsMandante):
            ptsVisitante = 3
        else:
            ptsVisitante = 1
            ptsMandante = 1
        return ptsMandante, ptsVisitante
    
#for ANO in range(2016,2018):
ANO = 2015
SERIE = 'A'
scrap = Scraper(str(ANO), SERIE)
linkJogos = scrap.pegaLinkJogos()
todasInfo = []
contador = 1
for link in linkJogos:
    informacoes = scrap.pegaInformacaoJogo(link)
    todasInfo.append(informacoes)
    #Salva os dados em um arquivo xlsx
    df = pd.DataFrame.from_dict(todasInfo)
    df.to_excel(f'Serie {SERIE} - {str(ANO)}.xlsx')
    print(f'{contador}/380')
    contador+=1