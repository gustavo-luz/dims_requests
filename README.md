# dims_requests
clone this repository and enter it
git clone https://github.com/gustavo-luz/dims_requests
cd dims_requests

## create and start a virtualenv

virtualenv venv
source venv/bin/activate # Linux
./venv/Scripts/activate # Windows
pip install the requirements
pip install -r requirements.txt



## deactivate
deactivate


## TODO
Como ainda haverão mais manipulações dos dados recebidos do heroku, uma biblioteca especifica para a classe container e outras que possam vir ajuda a não acumular muito código no arquivo principal.

    Para a parte de indexação usando o chipset ou mac, pode ser interessante fazer um arquivo xlsx e no método construtor do container fazer a parte de checar e/ou editar o arquivo, talvez até fazer uma nova coluna no dataFrame que é gerado pelo container.cointainerToDataFrame() específica pro setor de emissão do dado, como Asa Norte ou Sudoeste. A vantagem do arquivo xlsx é que não precisaria editar no código ".py" caso alguma mudança como modificação ou adição de setores no futuro.

    O formato do arquivo xlsx e csv gerado também precisaria ser definido, como se será preciso uma outra ordem de emissão, ou o que será preciso ser enviado.

    Como as dimensões do container físico são padronizadas, seria interessante colocar as dimensões reais, principalmente depois de terem feito o código que envia os dados simulando o arduino. Da forma atual é fácil geral capacidade negativa.

add more devices according to chipset
create link between chipset and device (chipset x = id y)
split values into columns
prep data: convert cm to %, send only needed fields 
configure final csv
export to google sheets

## future
check json before appending, check if there is every value
add tags to the datasend

# data goal
[id,filling percentual,date,battery level]
id -> linkink id with the chipset (future can be a key sent to dims)
data received + "%"
data received converted to % 



