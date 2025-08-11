# Importação das bibliotecas de análise e visualização
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# (IMPORTANTE!) Importa funções personalizadas do arquivo de utilitários
from utils import carregar_dados, decodificar_dados

# --- FUNÇÕES DE ANÁLISE E VISUALIZAÇÃO ---

def exibir_tabela_perfil(df, titulo, pasta_tabelas=None, nome_arquivo=None):
    """
    Gera uma tabela formatada do perfil dos participantes e a salva opcionalmente.
    """
    print(f"\n--- {titulo} ---")
    contagem = df['SITUACAO_CONCLUSAO'].value_counts(dropna=False)
    tabela = contagem.reset_index()
    tabela.columns = ['Situação de Conclusão', 'Quantidade']
    total = tabela['Quantidade'].sum()
    tabela['Percentual (%)'] = ((tabela['Quantidade'] / total) * 100).round(2)
    
    print(tabulate(tabela, headers='keys', tablefmt='grid', showindex=False))

    if pasta_tabelas and nome_arquivo:
        os.makedirs(pasta_tabelas, exist_ok=True)
        caminho_csv = os.path.join(pasta_tabelas, f"{nome_arquivo}.csv")
        caminho_excel = os.path.join(pasta_tabelas, f"{nome_arquivo}.xlsx")
        try:
            tabela.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
            tabela.to_excel(caminho_excel, index=False)
            print(f"(OK) Tabela '{nome_arquivo}' exportada para CSV e Excel.")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar tabela '{nome_arquivo}': {e}")


def gerar_graficos_comparativos(df, pasta_imagens):
    """
    Gera e salva os gráficos de boxplot para cada área do conhecimento.
    """
    print("\nIniciando geração dos gráficos comparativos (com base nos dados gerais)...")
    os.makedirs(pasta_imagens, exist_ok=True) 
    sns.set_theme(style="whitegrid") 
    
    mapa_notas_graficos = {
        'NU_NOTA_MT': 'Matemática', 'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas', 'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_REDACAO': 'Redação'
    }
    cor_mapa = {
        'Concluintes': '#1f77b4', 'Treineiros': '#2ca02c',
        'Egressos (Já concluí)': '#ff7f0e', 'Não concluí/cursando': '#d62728'
    }
    ordem_situacao = ['Concluintes', 'Treineiros', 'Egressos (Já concluí)', 'Não concluí/cursando']
    ordem_existente = [s for s in ordem_situacao if s in df['SITUACAO_CONCLUSAO'].unique()]

    for coluna_nota, nome_materia in mapa_notas_graficos.items():
        print(f"  > Criando gráfico para: {nome_materia}...")
        plt.figure(figsize=(12, 8))
        
        sns.boxplot(
            data=df, x='SITUACAO_CONCLUSAO', y=coluna_nota,
            order=ordem_existente, hue='SITUACAO_CONCLUSAO',
            palette=cor_mapa, legend=False
        )
        
        plt.title(f'Distribuição de Notas em {nome_materia} por Situação de Conclusão (Geral)', fontsize=16, pad=15)
        plt.xlabel('Situação de Conclusão do Ensino Médio', fontsize=12)
        plt.ylabel(f'Nota de {nome_materia}', fontsize=12)
        plt.xticks(rotation=10, ha='right')
        
        caminho_grafico = os.path.join(pasta_imagens, f'grafico_boxplot_situacao_{coluna_nota}.png')
        plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    - Gráfico salvo: {caminho_grafico}")
    print("\n(OK) Todos os gráficos foram gerados com sucesso.")


# --- EXECUÇÃO PRINCIPAL (MAIN) ---

def main():
    """
    Função principal que orquestra o fluxo da ANÁLISE EXPLORATÓRIA.
    """
    # Configurações do projeto
    pasta_dados = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\dados_filtrados_campo_belo_mg"
    pasta_imagens = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\imagens"
    pasta_tabelas = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\tabelas"
    anos = ['2019', '2020', '2021', '2022', '2023']

    # Etapa 1: Carregar e decodificar os dados usando as funções do 'utils.py'
    df_total = carregar_dados(pasta_dados, anos)

    if df_total is not None:
        df_total = decodificar_dados(df_total)

        # Etapa 2: Exibir e salvar perfil para cada ano
        print("\n" + "="*50)
        print("INICIANDO ANÁLISE INDIVIDUAL POR ANO")
        print("="*50)
        for ano in sorted(df_total['NU_ANO'].unique()):
            df_ano = df_total[df_total['NU_ANO'] == ano]
            exibir_tabela_perfil(
                df_ano, 
                f"Perfil dos Participantes - Ano {ano}", 
                pasta_tabelas,
                f"perfil_participantes_{ano}"
            )
        
        # Etapa 3: Exibir e salvar perfil geral consolidado
        print("\n" + "="*50)
        print("INICIANDO ANÁLISE GERAL CONSOLIDADA")
        print("="*50)
        exibir_tabela_perfil(df_total, "Perfil Geral dos Participantes (2019-2023)", pasta_tabelas, "perfil_geral_consolidado")

        # Etapa 4: Gerar gráficos com base nos dados gerais
        gerar_graficos_comparativos(df_total, pasta_imagens)

        print("\n(SUCESSO) Análise exploratória finalizada.")
    else:
        print("\n(FALHA) Não foi possível realizar a análise.")

# Ponto de entrada do script
if __name__ == "__main__":
    main()