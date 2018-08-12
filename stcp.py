import os, sys
import requests

link = "www.stcp.pt/pt/widget/post.php?"
uid = "d72242190a22274321cacf9eadc7ec5f"
submete = "Mostrar"

# Retorna apenas os números das linhas
def getLinhas():
    request_url = "http://www.stcp.pt/pt/itinerarium/callservice.php?action=lineslist&service=1" 
    r = requests.get(request_url)
    response = r.content.decode()

    linhas = []
    num_linhas = int(response.split('"recordsReturned": ')[1][:2])
    for i in range(0, num_linhas-1):
        linha = response.split('"code": ')[i+1]
        linhas.append(linha[:4].strip('"').strip(","))
    
    return linhas

linhas = getLinhas()

def getParagens(linha):
    request_url = "http://www.stcp.pt/pt/itinerarium/callservice.php?action=linestops&lcode="+ linha + "&ldir=1"
    r = requests.get(request_url)
    response = r.content.decode()

    num_paragens = int(response.split('"recordsReturned": ')[1][:2])

    paragens = []
    for i in range(0, num_paragens-1):

        paragem = response.split('"code": ')[i+1]
        np = response.split('"name": ')[i+1].split('"')[1]
        paragem = paragem[:5].strip('"').strip(",")
        paragem_duo = [paragem, np]
        paragens.append(paragem_duo)

    return paragens

paragens = getParagens("203")

# Obter página relativa a uma paragem
def getTempos(paragem_duo):
    paragem = paragem_duo[0]
    np = paragem_duo[1]

    request = "http://" + link + "uid=" + uid + "&" + "np=" + np + "&" + "paragem=" + paragem + "&" + "submete=" + submete
    
    print(request)
    r = requests.get(request)
 
    response = r.content.decode().rstrip().split()
    response = ' '.join(response)

    passagens = response.split('"floatLeft Linha')
    autocarros = []
    numero_passagens = int((len(passagens) - 4) / 3)
    for i in range (0, numero_passagens):
        linha = passagens[3*(i+2)-2].split('class="linha_')[1][:3]
        destino = passagens[3*(i+2)-1].split('"> <i>')[0].split("</i>")[0][6:]
        tempo = passagens[3*(i+2)][3:15]
        if "a passar" in tempo:
            tempo = 0 
        else:
            tempo = int(tempo.split("-")[1].split("min")[0][1:3])

        linha_trio = [linha, destino, tempo]
        autocarros.append(linha_trio)
    
    # If response: <div class="msgBox warning"> <span>Nao ha autocarros previstos para a paragem indicada nos proximos 60 minutos.</span> </div>
    if '<div class="msgBox warning"> <span>Nao ha autocarros previstos para a paragem indicada nos proximos 60 minutos.</span> </div>' in response:
        response = False
    
    return autocarros

TOKEN = "593680653:AAFCCNuwh_ECOxjzygcqLw-MGbIwu6hAtDE"
bot = telegram.Bot(token = TOKEN)
updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

def message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

def comandos(bot, update):
    chat_id = update.message.chat_id
