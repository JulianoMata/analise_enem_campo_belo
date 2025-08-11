import pandas as pd
import time
import os

# --- CONFIGURAÇÕES PARA O ANO DE 2021 ---

# 1. Caminho para o arquivo de dados original de 2021
caminho_dados_originais = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\dados_enem\microdados_enem_2021\DADOS\MICRODADOS_ENEM_2021.csv"

# 2. Pasta de destino para os dados filtrados
pasta_destino = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\dados_filtrados_campo_belo_mg"
nome_arquivo_saida = "enem_2021_campo_belo_prova.csv"
caminho_dados_filtrados = os.path.join(pasta_destino, nome_arquivo_saida)

# 3. Código do município da PROVA para o filtro
codigo_municipio_prova = 3111200

# 4. Lista de colunas para manter (mesma estrutura)
colunas_para_manter = [
    'NU_INSCRICAO', 'NU_ANO', 'TP_ST_CONCLUSAO',
    'CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA',
    'TP_ESCOLA', 'TP_DEPENDENCIA_ADM_ESC',
    'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'SG_UF_ESC',
    'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
    'TP_STATUS_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005',
    'Q006', 'Q022', 'Q024', 'Q025'
]

# --- EXECUÇÃO DO SCRIPT ---
try:
    os.makedirs(pasta_destino, exist_ok=True)
    print(f"Iniciando processamento para 2021...")
    print(f"Lendo de: {caminho_dados_originais}")
    inicio = time.time()
    chunk_size = 50000
    dados_filtrados_lista = []
    with pd.read_csv(
        caminho_dados_originais, chunksize=chunk_size, sep=';',
        encoding='latin-1', usecols=colunas_para_manter, low_memory=False
    ) as leitor_csv:
        print(f"Filtrando pela cidade da PROVA com código: {codigo_municipio_prova}...")
        for chunk in leitor_csv:
            chunk_filtrado = chunk[chunk['CO_MUNICIPIO_PROVA'] == codigo_municipio_prova]
            if not chunk_filtrado.empty:
                dados_filtrados_lista.append(chunk_filtrado)
    if not dados_filtrados_lista:
        print("\nAVISO: Nenhum participante encontrado. Verifique o código do município e o caminho do arquivo.\n")
    else:
        df_final = pd.concat(dados_filtrados_lista)
        df_final.to_csv(caminho_dados_filtrados, index=False, sep=';', encoding='utf-8-sig')
        fim = time.time()
        duracao = round(fim - inicio, 2)
        print("-" * 50)
        print("Processo de 2021 finalizado com sucesso!")
        print(f"Tempo total: {duracao} segundos.")
        print(f"Encontrados {len(df_final)} participantes.")
        print(f"Dados salvos em: {caminho_dados_filtrados}")
        print("-" * 50)
except FileNotFoundError:
    print(f"ERRO: Arquivo não encontrado! Verifique o caminho:\n{caminho_dados_originais}")
except KeyError as e:
    print(f"ERRO: A coluna {e} não foi encontrada no arquivo CSV de 2019.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")