from extracao import extract_saude, extract_clinica
from normalizacao import normaliza_saude
from validacao import valida_exames, compara_exames
from busca import busca_paciente
from utilitarios import *
import pymupdf, pandas as pd

              
@tempo_execucao    
def load(dict_clinica, dict_saude):
    base_saude = pd.DataFrame(dict_saude).sort_values(by="Nome")
    base_saude = normaliza_saude(base_saude)
    base_saude.to_excel("output/planilha_saude.xlsx", engine="openpyxl", index=False)
    base_clinica = pd.DataFrame(dict_clinica).sort_values(by="Nome")
    base_clinica.to_excel("output/planilha_clinica.xlsx", engine="openpyxl", index= False)
    busca_paciente(base_clinica, base_saude)


if __name__ == "__main__":


    # doc_saude = pymupdf.open("data/saude.pdf")      #PDFs ORIGINAIS
    # doc_clinica = pymupdf.open("data/clinica.pdf")  #PDFs ORIGINAIS




    # dict_clinica = extract_clinica(doc_clinica)    #EXTRACAO  
    # dict_saude = extract_saude(doc_saude)          #EXTRACAO
 
    # base_saude = pd.DataFrame(dict_saude).sort_values(by="Nome")   #TRANSFORMA EM DF
    # base_saude.to_excel("output/antes_normaliza_saude.xlsx")       #TRANSFORMA EM .XLSX


    base_saude = pd.read_excel("output/antes_normaliza_saude.xlsx")
    base_saude = normaliza_saude(base_saude)
    base_saude.to_excel("output/depois_normaliza_saude.xlsx")

    # base_clinica = pd.DataFrame(dict_clinica).sort_values(by="Nome")  #TRANSFORMA EM DF
    # base_clinica.to_excel("output/planilha_clinica.xlsx")             #TRANSFORMA EM .XLSX


    base_clinica = pd.read_excel("output/planilha_clinica.xlsx")
    busca_paciente(base_clinica, base_saude)
    valida_exames(pd.read_excel("output/dados_cruzados.xlsx"))
    compara_exames()

