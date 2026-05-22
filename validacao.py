import pandas as pd
from utilitarios import limpar
from utilitarios import inclui_log_faturamento, inclui_log_saude, str_para_list, tempo_execucao



@tempo_execucao
def valida_exames(dados_cruzados):

    df_padrao = pd.read_excel("data/padrao.xlsx")
    log_faturamento = []
    log_saude = []
    #OBJETIVO:
    #Identificar na tabela padrao a linha do exame
    #Coletar a chave numerica
    #Inserir no log respectivo
    for _, linha in dados_cruzados.iterrows():  
        #para cada linha dos dados cruzados
        lista_exames_clinica = str_para_list(linha["Exames_Clinica"])
        lista_exames_saude = str_para_list(linha["Exames_Saude"])

        for item in lista_exames_clinica: #item da lista de exames encontrados no pdf com o nome do paciente
            encontrou = False
            #para cada linha dos dados_cruzados
            #verificar em cada linha de padrao se encontra o exame para pegar a chaver
            for _, line1 in df_padrao.iterrows():
                linha_clinica = str_para_list(limpar(line1["CLINICA"]))
                if limpar(item) in linha_clinica: #linha clinica é uma lista motivo: (pfr 1, pfr2)
                    inclui_log_faturamento(log_faturamento, linha["Data"], linha["Solicitacao"], linha["Nome"], line1["CHAVE"])
                    encontrou = True
                    break
            if not encontrou:
                inclui_log_faturamento(
                    log_faturamento, 
                    linha["Data"], 
                    linha["Nome"], 
                    linha["Solicitacao"],
                    item
                    )
        df_f = pd.DataFrame(log_faturamento)
        df_f.to_excel("output/log_faturamento.xlsx", engine="openpyxl")

        for i, item in enumerate(lista_exames_saude):
            encontrou = False
            if limpar(item) == limpar("DOSAGEM DE TSH E T4 LIVRE (CONTROLE / DIAGNOSTICO TARDIO)"):
                    tsh = int(df_padrao.loc[df_padrao["SIS_1"] == "DOSAGEM DE HORMONIO TIREOESTIMULANTE (TSH)",  "CHAVE"].iloc[0])
                    t4 = int(df_padrao.loc[df_padrao["SIS_1"] == "DOSAGEM DE TIROXINA LIVRE (T4 LIVRE)",  "CHAVE"].iloc[0])

                    log_saude = inclui_log_saude( 
                        log_saude, 
                        linha["Data"], 
                        linha["Nome"], 
                        tsh
                        )
                    log_saude = inclui_log_saude( 
                        log_saude, 
                        linha["Data"], 
                        linha["Nome"], 
                        t4
                        )
                    continue

            elif limpar(item) == limpar("DOSAGEM DE PROTEINAS TOTAIS E FRACOES"):
                    proteina_total = int(df_padrao.loc[df_padrao["SIS_1"] == "DOSAGEM DE PROTEINAS TOTAIS", "CHAVE"].iloc[0])
                    proteina_fracao = int(df_padrao.loc[df_padrao["SIS_1"] == "DOSAGEM DE PROTEINAS FRACOES", "CHAVE"].iloc[0])

                    log_saude = inclui_log_saude( 
                        log_saude, 
                        linha["Data"], 
                        linha["Nome"],
                        proteina_fracao
                        )
                    log_saude = inclui_log_saude( 
                        log_saude, 
                        linha["Data"], 
                        linha["Nome"], 
                        proteina_total
                        )
                    continue
            
            for _, line2 in df_padrao.iterrows():
                if any( limpar(item) == limpar(str(line2[col])) for col in ["SIS_1", "SIS_2"] ):
                    log_saude = inclui_log_saude( 
                        log_saude, 
                        linha["Data"], 
                        linha["Nome"], 
                        line2["CHAVE"] 
                        )
                    encontrou = True
                    break
            if not encontrou:
                log_saude = inclui_log_saude( 
                    log_saude, 
                    linha["Data"], 
                    linha["Nome"], 
                    item 
                    )

    df_s = pd.DataFrame(log_saude)
    df_s.to_excel("output/log_saude.xlsx", engine="openpyxl")     

@tempo_execucao   
def compara_exames():
    dados_saude = pd.read_excel("output/log_saude.xlsx")
    dados_clinica = pd.read_excel("output/log_faturamento.xlsx")
    log_final = []

    for _, linha_saude in dados_saude.iterrows():
        
        aux_nome = linha_saude["Nome"]
        for _, linha_clinica in dados_clinica.iterrows():
            
            if linha_saude["Nome"] == linha_clinica["Nome"]:
                exames_clinica = str_para_list(linha_clinica["Exames"])
                exames_saude = str_para_list(linha_saude["Exames"])

                exames_nao_solicitados = [elem for elem in exames_clinica if elem not in exames_saude]

                
                if exames_nao_solicitados:
                    log_final.append({
                        "Nome": linha_clinica["Nome"],
                        "Status": "Faturamento Errado",
                        "Exames_Nao_Solicitados": exames_nao_solicitados
                    })
                else:
                    log_final.append({
                        "Nome": linha_clinica["Nome"],
                        "Status": "OK",
                        "Exames_Nao_Solicitados": []
                    })

                break  

    log = pd.DataFrame(log_final)
    log.to_excel("output/log_final.xlsx", index=False)
