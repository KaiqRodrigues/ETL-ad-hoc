import re
import unicodedata
import pandas as pd

from utilitarios import tempo_execucao




@tempo_execucao
def normaliza_saude(doc):
    pacientes = {}
    contadores = {} 

    for _, linha in doc.iterrows():
        nome = linha["Nome"]
        data = linha["Data"]
        exame = linha["Exame"]

        if nome not in contadores:
            contadores[nome] = 0

        chave_paciente = nome
        chave_final = (nome, data)

        if chave_final not in pacientes:
            contadores[chave_paciente] += 1
            solicitacao = contadores[chave_paciente]

            pacientes[chave_final] = {
                "Data": data,
                "Nome": nome,
                "Solicitacao": solicitacao,   #caso exista mais de uma solicitação por paciente
                "Exames": []
            }

        pacientes[chave_final]["Exames"].append(exame)

    
    df = pd.DataFrame(pacientes.values())  
    return df
   