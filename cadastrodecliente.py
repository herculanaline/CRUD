#Importação das requests referentes ao Flask
import requests
#Importação padrão do Flask
from flask import Flask, request, jsonify

# Token de autenticação para a API do Pipefy
token = "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MDQyMDIzOTMsImp0aSI6IjAyZmI0MGFmLWYwNGQtNGNjMi05Yjc4LWJkZmQ5YzhhZWM4NCIsInN1YiI6MzA0MTY1MTY2LCJ1c2VyIjp7ImlkIjozMDQxNjUxNjYsImVtYWlsIjoiZGVzYWZpb2ludGVncmFjYW9AcHJvZmVjdHVtLmNvbS5iciIsImFwcGxpY2F0aW9uIjozMDAzMDU3MDEsInNjb3BlcyI6W119LCJpbnRlcmZhY2VfdXVpZCI6bnVsbH0.NDCy-EvEyaQpct5lEeaXRdCCWCuU4K-DRggf2wdZIsVMo8tIwk0kY7bPVPnngajjULE_hF-O0rqqydkyzJiNBA"

# ID do Pipefy
pipe_id = "303843596"

# Iniciando Flask
app = Flask(__name__)

# URL base da API do Pipefy
base_url = "https://api.pipefy.com/graphql"

# Definindo a página inicial da aplicação, onde exibirá uma mensagem
@app.route("/")
def index():
    return "Flask API to interact with Pipefy"

# Criação de uma nova rota, onde se cria um novo card no Pipefy ao enviar via método Post
@app.route("/create_card", methods=['POST'])
def criar_card():
    # Criação de um método onde pegamos os dados enviados na solicitação Post
    data = request.get_json()
    # Consulta enviada ao Pipefy para criar um novo card, código padrão segundo a documentação do Pipefy
    query = """
    mutation {
      createCard(input: {
        pipe_id: "%s",
        title: "%s",
        fields_attributes: [
          {field_id: "role_name", field_value: "%s"},
          {field_id: "email", field_value: "%s"},
        ]
      }) {
        card {
          id
        }
      }
    }
    """ % (pipe_id, data['title'], data['role_name'], data['email'])

# Aqui é enviado uma consulta para o Pipefy usando o método Post da biblioteca requests
    response = requests.post(base_url, json={'query': query}, headers={'Authorization': 'Bearer ' + token})

# Então verificamos a presença ou não de erros
    if response.status_code == 200:
        card_id = response.json()['data']['createCard']['card']['id']
        return jsonify({'message': 'Card created!', 'card_id': card_id}), 200
    else:
        return jsonify({'error': 'Error when creating card in Pipefy'}), response.status_code

# É criada uma rota responsável por deletar um card anteriormente criado no Pipefy ao enviar o método Delete
@app.route('/delete_card/<card_id>', methods=['DELETE'])
def deletar_card(card_id):
    # primeiro ele consulta o card a ser deletado e então deleta o card no Pipefy,código padrão da documentação do pipefy
    query = """
    mutation {
      deleteCard(input: {
        id: "%s"
      }) {
        success
      }
    }
    """ % card_id

#Enviamos então uma consulta para o Pipefy usando o método Delete da biblioteca requests
    response = requests.post(base_url, json={'query': query}, headers={'Authorization': 'Bearer ' + token})

# E então verificamos se a autorização foi bem sucedida ou não
    if response.status_code == 200:
        return jsonify({'message': 'Card deleted'}), 200
    else:
        return jsonify({'error': 'Error when deleting card in Pipefy'}), response.status_code

# Nesse ponto criamos uma rota para atualização de um usuário no Pipefy utilizando o método Put
@app.route('/update_user/<card_id>', methods=['PUT'])
def update_user(card_id):
    
    #Nesse ponto pegamos os dados enviados
    data = request.get_json()
    #E então consultamos para fazer a alteração e enviar para o Pipefy
    query = """
    mutation {
      updateCard(input: {
        id: "%s",
        fields_attributes: [
          {field_id: "role_name", field_value: "%s"},
          {field_id: "email", field_value: "%s"}
        ]
      }) {
        card {
          id
          title
        }
      }
    }
    """ % (card_id, data['role_name'], data['email'])

#Enviamos então uma consulta para o Pipefy usando o método Put da biblioteca requests
    response = requests.post(base_url, json={'query': query}, headers={'Authorization': 'Bearer ' + token})

#E então verificamos se a solicitação foi bem sucedida ou não
    if response.status_code == 200:
        authorized_user = response.json()['data']['updateCard']['card']
        return jsonify({'message': 'User updated successfully!', 'authorized_user': authorized_user}), 200
    else:
        return jsonify({'error': 'Error updating user in Pipefy'}), response.status_code


#Iniciando a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
