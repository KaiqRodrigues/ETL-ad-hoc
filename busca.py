import bisect

import pandas as pd
from utilitarios import limpar
from utilitarios import tempo_execucao

@tempo_execucao
def busca_paciente(base_clinica, base_saude):

    #Para cada paciente faturado, iterar na lista da Saude para encontrar as solicitações. 
    #Parametro: Nome
    base_saude["nome_limpo"] = base_saude["Nome"].apply(limpar)
 
    log = []
    for _, linha_clinica in base_clinica.iterrows():
        nome_clinica = limpar(linha_clinica["Nome"])
        nomes_organizados_saude = sorted([limpar(nome) for nome in base_saude["Nome"].tolist()])

        #bisect retorna onde o nome deveria estar, com isso é possivel verificar se o nome existe com uma comparação
        indice = bisect.bisect_left(nomes_organizados_saude, nome_clinica)
        if indice < len(nomes_organizados_saude) and nomes_organizados_saude[indice] == nome_clinica:

            #pegar todas as linhas do paciente cujo encontrado no pdf da saude 
            linha_saude = base_saude.loc[base_saude["nome_limpo"] == nome_clinica]

            #para cada correspondencia do nome na saude: adicionar no log 
            #garante que todas solciitações da pessoa sejam salvas
            for _,item in linha_saude.iterrows():
                # if any(solicitacao_individual["Nome"] == nome_clinica for solicitacao_individual in log):
                    
                log.append(
                    {"Data": item["Data"],
                     "Nome": limpar(item["Nome"]),
                     "Solicitacao": int(item["Solicitacao"]), #devido retorno "np.int64"
                     "Exames_Saude": item["Exames"],
                     "Exames_Clinica": linha_clinica["Exame"],
                     "Status": "Encontrado"}
                )
        else:
            log.append(
                {"Data": linha_clinica["Data"],
                    "Nome": linha_clinica["Nome"],
                    "Solicitacao": None,
                    "Exames_Saude": None,
                    "Exames_Clinica": linha_clinica["Exame"],
                    "Status": "Não Encontrado"}
            )   

    df_temp = pd.DataFrame(log)
    df_temp.to_excel("output/dados_cruzados.xlsx")
    return df_temp


