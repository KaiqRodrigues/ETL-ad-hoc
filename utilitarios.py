import ast
from functools import wraps
import re
import time
import unicodedata


def limpar(linha_og):   
    linha_tratada = unicodedata.normalize("NFKD", linha_og)
    linha_tratada = linha_tratada.encode("ASCII", "ignore").decode("utf-8")  
    linha_tratada = linha_tratada.lower().strip()
    linha_tratada = linha_tratada.replace('\ufeff', '').replace('\u200b', '')
    linha_tratada = re.sub(r'\s+', ' ', linha_tratada)
    return linha_tratada    




def tempo_execucao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        print(f"[TEMPO] {func.__name__} levou {fim - inicio:.4f} segundos")
        
        if resultado is None:
            return  # não retorna nada
        return resultado
    return wrapper


def inclui_log_faturamento(lista, data, solicitacao, paciente, novo_exame):
    for d in lista:
        if limpar(d["Nome"]) == limpar(paciente) and d["Data"] == data:
            d["Exames"].append(novo_exame)
            return 

    lista.append({
        "Data": data,
        "Nome": paciente,
        "Solicitacao": solicitacao,
        "Exames": [novo_exame]
    })

def inclui_log_saude(lista,data, paciente, novo_exame):
    
    for d in lista:
        if limpar(d["Nome"]) == limpar(paciente) and d["Data"] == data:
            d["Exames"].append(novo_exame)
            return lista
    lista.append({
        "Data": data,
        "Nome": paciente,
        "Exames": [novo_exame]
    })
    return lista

def str_para_list(valor):
    if isinstance(valor, list):
        return valor  # já é lista
    if isinstance(valor, str):
        try:
            return ast.literal_eval(valor)
        except (ValueError, SyntaxError):
            return []
    return []
