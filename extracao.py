import re
from utilitarios import tempo_execucao

alergias = []
@tempo_execucao
def extract_saude(pdf):
    linhas_df = []
    data, nome, exame = "","",""
    for pagina in pdf:

        texto = pagina.get_text("text")
        linhas = texto.splitlines()

        for linha in linhas[16:-3]:
            if linha[2] == "/":
                data = linha[:10]
                nome = linha[10:]
            elif linha[0].isalpha():
                exame = linha
                linhas_df.append({"Data": data, "Nome": nome, "Exame": exame})
    return linhas_df

@tempo_execucao
def extract_clinica(pdf):
    data, nome = "",""
    captura_exames = False
    paciente = []
    cabecalhos = ("QTD", "TOTAL", "UBS", "--", "LAB", "RELAT", "CONVE", "PERI", "UNID", "PAG")

    padrao_data = re.compile(r"\d{2}/\d{2}/\d{4}")
    for i,pagina in enumerate(pdf):
        texto = pagina.get_text("text")
        linhas = texto.splitlines()

        for i,linha in enumerate(linhas): 
            if padrao_data.fullmatch(linha):
                data = linha  #se a data esta duas linhas acima, e não começa um Valor R$
            elif padrao_data.fullmatch(linhas[i-2]):
                nome = linha
            elif linha.upper().startswith("VALOR R$"):
                captura_exames = True #ativa captura de exames
                exames = []
                continue   # pula a linha no loop
            
            elif linha.startswith("--") and captura_exames:  #acabou os exames do paciente, entao finaliza e desativa captura
                captura_exames = False
                paciente.append({"Data": data, "Nome": nome, "Exame": exames})
            
            elif captura_exames:   #se não é o valor nem os textos da tupla, entao é nome de exame
                if linha[0].isdecimal() and linha == "10,53":
                    alergias.append(linhas[i-1])
                elif not ( linha[0].isdecimal() or linha.upper().startswith(cabecalhos) ):
                    exames.append(linha)

    return paciente