# ==============================================================================
# SCRIPT DE UTILITÁRIOS (utils.py)
# Contém funções de apoio para carregar e preparar os dados do projeto ENEM.
# ==============================================================================

import pandas as pd
import os

def carregar_dados(caminho_pasta, anos):
    """
    Carrega e concatena arquivos CSV de diferentes anos.
    """
    lista_dataframes = []
    print("Iniciando carregamento dos dados via 'utils'...")
    for ano in anos:
        nome_arquivo = f"enem_{ano}_campo_belo_prova.csv"
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        try:
            print(f"  > Lendo arquivo: {nome_arquivo}...")
            df_ano = pd.read_csv(caminho_completo, sep=';', encoding='utf-8-sig', low_memory=False)
            lista_dataframes.append(df_ano)
            print(f"    - Arquivo de {ano} carregado com sucesso.")
        except FileNotFoundError:
            print(f"    [ERRO] Arquivo para o ano {ano} não encontrado.")
    
    if not lista_dataframes:
        print("[AVISO] Nenhum dado foi carregado.")
        return None
        
    df_total = pd.concat(lista_dataframes, ignore_index=True)
    print(f"\n(OK) Total de {len(df_total)} registros carregados.")
    return df_total

def decodificar_dados(df):
    """
    Decodifica as colunas de códigos para valores textuais, criando novas colunas.
    """
    print("\nDecodificando variáveis...")
    mapa_conclusao = {
        1: 'Egressos (Já concluí)', 2: 'Concluintes',
        3: 'Treineiros', 4: 'Não concluí/cursando'
    }
    df['SITUACAO_CONCLUSAO'] = df['TP_ST_CONCLUSAO'].map(mapa_conclusao)
    return df