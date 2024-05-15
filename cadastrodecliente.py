import requests

# Importações do Flask
# from flask import Flask, request, jsonify

#Token de autenticação para a API do Pipefy
token = "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MDQyMDIzOTMsImp0aSI6IjAyZmI0MGFmLWYwNGQtNGNjMi05Yjc4LWJkZmQ5YzhhZWM4NCIsInN1YiI6MzA0MTY1MTY2LCJ1c2VyIjp7ImlkIjozMDQxNjUxNjYsImVtYWlsIjoiZGVzYWZpb2ludGVncmFjYW9AcHJvZmVjdHVtLmNvbS5iciIsImFwcGxpY2F0aW9uIjozMDAzMDU3MDEsInNjb3BlcyI6W119LCJpbnRlcmZhY2VfdXVpZCI6bnVsbH0.NDCy-EvEyaQpct5lEeaXRdCCWCuU4K-DRggf2wdZIsVMo8tIwk0kY7bPVPnngajjULE_hF-O0rqqydkyzJiNBA"

#ID do Pipefy
pipe_id = "303843596"

#URL base da API do Pipefy
base_url = "https://developers.pipefy.com/reference/what-is-graphql"

#Iniciando flask
# app = Flask(__name__)

# Endpoint para criar um card no Pipefy de acordo com os campos presentes no cadastro de Pessoa
# @app.route("/")
def criar_card():
#     #Montagem da query
#     query = """
#     mutation {
#       createCard(input: {
#         pipe_id: "%s",
#         title: "%s",
#         fields_attributes: [
#           {field_id: "nome", field_value: "%s"},
#           {field_id: "email", field_value: "%s"},
#           {field_id: "idade", field_value: %d}
#         ]
#       }) {
#         card {
#           id
#         }
#       }
#     }
#     """ % (pipe_id, data['nome'], data['email'], data['idade'])

#     #Solicitação para a API do Pipefy
#     response = requests.post(base_url, json={'query': query}, headers={'Authorization': f'Bearer {token}'})

#     #Verificação
#     if response.status_code == 200:
#         card_id = response.json()['data']['createCard']['card']['id']
#         return jsonify({'message': 'Card criado', 'card_id': card_id}), 200
#     else:
#         return jsonify({'error': 'Erro na criação do card no Pipefy'}), response.status_code

# Endpoint para deletar ID solicitado
# @app.route('/deletar_card/<card_id>', methods=['DELETE'])
def deletar_card(card_id):
    #Montagem da query
    query = """
    mutation {
      deleteCard(input: {
        id: "%s"
      }) {
        success
      }
    }
    """ % card_id

    #Solicitando a API
    response = requests.post(base_url, json={'query': query}, headers={'Authorization': f'Bearer {token}'})

    #Verificação
    if response.status_code == 200:
        return jsonify({'message': 'Card deletado'}), 200
    else:
        return jsonify({'error': 'Erro ao deletar o card no Pipefy'}), response.status_code

# Endpoint para atualização da fase
# @app.route('/atualizar_fase/<card_id>', methods=['PUT'])
def atualizar_fase(card_id):
    #Query de atualização
    query = """
    mutation {
      moveCard(input: {
        card_id: "%s",
        phase_id: "nova_fase_id_aqui"
      }) {
        card {
          current_phase {
            name
          }
        }
      }
    }
    """ % card_id

    # Fazendo a solicitação para a API do Pipefy
    response = requests.post(base_url, json={'query': query}, headers={'Authorization': f'Bearer {token}'})

    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        fase_atual = response.json()['data']['moveCard']['card']['current_phase']['name']
        return jsonify({'message': 'Fase atualizada com sucesso', 'fase_atual': fase_atual}), 200
    else:
        return jsonify({'error': 'Erro ao atualizar a fase do card no Pipefy'}), response.status_code

# Rodando o aplicativo Flask
# if __name__ == '__main__':
#     app.run(debug=True)

