# dims_requests

## TODO
fazer um dict com os chipsets e ids

mudar a forma que o dado é enviado, desse jeito tem 2 ints um sendo a bateria e outro a distância sem padronização
padronizar para o envio do cássio também, dessa forma temos que extrair cada um de um jeito

limpar os dados
ver como atualizar de tempos
configurar o data studio: quais gráficos vão ser mostrados,
layout 

# data goal
[id,date,battery level, filling percentual]
id -> linkink id with the chipset (future can be a key sent to dims)
from millis (https://currentmillis.com/) to ISO
data received + "%"
data received converted to % 



# infra
alguns dos devices manda um post pro heroku e as vezes manda a aplicação serveless rodar

conductor: evolução do cron, além de setar o tempo
conductor workflow definition
ele espera alguem dar um get no condutctor local host com o id da arvore criada
entende como start e roda todo o diagrama
no front define o q é um sucesso, um erro

serveless é um transistor, ele so liga quando alguem manda
no serveless coloca uma inteligencia
qual foi a ultima hora q rodou 

linux tem o cron

criar um codigo que consulta o dado do dims e joga num google sheets
dps começa a pensar em expor uma porta pra engatilhar

concentrador no meio, fica olhando o heroku, usa o conector externo 

vantagem do google sheets: manutenção, nome do google, plataforma gerenciada

hardware sua responsabilidade, software tb como laboratorio
tudo paas ou saas
n tem responsabilidade como responsabilidade