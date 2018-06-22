#!/usr/bin/python
# coding: utf-8

import twitter
import time
import sys

api = twitter.Api(consumer_key='consumer_key',
                  consumer_secret='consumer_secret',
                  access_token_key='access_token_key',
                  access_token_secret='access_token_secret')

mentions = api.GetMentions()

print 'Imprimindo mentions'
for m in mentions:
    print m.id, m.user.screen_name, m.text

sys.exit(0)

#ultima_mention = mentions[0].id
# a API dá as 'mentions' como uma lista, na
# qual as 'mentions' mais novas vêm primeiro

# Agora iremos tratar as 'mentions' e respondê-las
while True:
    # Iremos fazer o programa esperar um pouco a
    # cada requisição, pois o Twitter não permite
    # que se faça muitas requisições em um espaço
    # curto de tempo (o intervalo de 20s é suficiente)
    time.sleep(20)

    # Pegando 'mentions' desde a última obtida
    mentions = api.GetMentions(since_id = ultima_mention)
    for m in mentions:
        # O texto, estará em m.text, e primeiramente iremos
        # retirar o nome da nossa aplicação do texto
        texto = m.text.replace('@perfil_da_aplicacao', '')

        # Se houver a hashtag '#calcule', no tuíte...
        if texto.find('#calcule') >= 0:
            #...iremos calcular como um comando comum
            # do Python (usando a função 'eval'
            # (mas antes, retiramos a hashtag,
            # com a função "replace")
            resultado = str(eval(texto.replace('#calcule','')))

            # Respondendo a 'mention':
            # A linha abaixo pega o nome (no perfil)

            # de quem fez a 'mention'
            quem_fez_a_mention = m.user.screen_name
            # A próxima já responde ao tuíte com

            # o resultado do cálculo
            status = api.PostUpdate('@' + quem_fez_a_mention  \
                                    + ': ' + resultado)
        else:
            # Ideias?
            pass # por enquanto, não faz nada

        # Essas linhas abaixo atualizam o id da última
        # 'mention', para que nas próximas requisições<
        # somente as novas 'mentions' sejam obtidas
        if m.id > ultima_mention:
            ultima_mention = m.id
