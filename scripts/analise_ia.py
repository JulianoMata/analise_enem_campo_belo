# Importação das bibliotecas necessárias
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder

# (IMPORTANTE!) Importa função personalizada do próprio arquivo de utilitários
from utils import carregar_dados

# --- FUNÇÃO DE ANÁLISE (O coração do script) ---

def treinar_e_avaliar_modelo(df_total, features_colunas, target_coluna, nome_area, mapa_perguntas, salvar_em):
    """
    Prepara os dados, treina um modelo Random Forest e gera um gráfico de importância de fatores.
    """
    print(f"\nIniciando análise da área: {nome_area}...")
    
    # Prepara os dados para o modelo
    df = df_total[features_colunas + [target_coluna]].copy()
    df.dropna(subset=[target_coluna], inplace=True)
    for col in features_colunas:
        df[col].fillna(df[col].mode()[0], inplace=True)
    
    encoder = OrdinalEncoder()
    df[features_colunas] = encoder.fit_transform(df[features_colunas])
    
    X = df[features_colunas]
    y = df[target_coluna]

    # Treina o modelo
    print(f"  - Treinando modelo para {nome_area}...")
    modelo = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    modelo.fit(X, y)

    # Gera e salva o gráfico de resultados
    importancia_df = pd.DataFrame({
        'Fator_Codigo': features_colunas,
        'Importancia': modelo.feature_importances_
    }).sort_values(by='Importancia', ascending=False)
    importancia_df['Fator'] = importancia_df['Fator_Codigo'].map(mapa_perguntas)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importancia', y='Fator', data=importancia_df, palette='viridis', hue='Fator', legend=False)
    
    plt.title(f'Fatores Socioeconômicos que Influenciam a Nota de {nome_area}', fontsize=16, pad=20)
    plt.xlabel('Importância Relativa (calculada pelo modelo)', fontsize=12)
    plt.ylabel('Fator Socioeconômico', fontsize=12)
    
    os.makedirs(salvar_em, exist_ok=True)
    nome_arquivo = f'grafico_importancia_{target_coluna.lower()}.png'
    caminho = os.path.join(salvar_em, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - Gráfico salvo em: {caminho}")

# --- EXECUÇÃO PRINCIPAL (MAIN) ---

def main():
    """
    Função principal que orquestra todo o fluxo da análise de IA.
    """
    # Configurações do projeto
    pasta_dados = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\dados_filtrados_campo_belo_mg"
    pasta_imagens = r"D:\FACULDADE_DOMBOSCO\Disciplinas\6_ MODULAR\02-Estagio_Supervisionado_II_IA\projeto_enem\imagens"
    anos = ['2019', '2020', '2021', '2022', '2023']

    mapa_perguntas = {
        'Q001': 'Escolaridade do Pai', 'Q002': 'Escolaridade da Mãe', 'Q003': 'Ocupação do Pai',
        'Q004': 'Ocupação da Mãe', 'Q005': 'Nº de Pessoas na Família', 'Q006': 'Renda Familiar Mensal',
        'Q022': 'Possui Celular', 'Q024': 'Possui Computador', 'Q025': 'Possui Acesso à Internet'
    }
    features_colunas = list(mapa_perguntas.keys())
    
    target_colunas = {
        'NU_NOTA_MT': 'Matemática', 'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas', 'NU_NOTA_LC': 'Linguagens e Códigos', 'NU_NOTA_REDACAO': 'Redação'
    }

    print("Iniciando análise de fatores de influência nas notas do ENEM...\n")
    # Usa a função importada do utils.py
    df_total = carregar_dados(pasta_dados, anos)

    if df_total is not None:
        for codigo_nota, nome_area in target_colunas.items():
            treinar_e_avaliar_modelo(df_total, features_colunas, codigo_nota, nome_area, mapa_perguntas, pasta_imagens)
        
        print("\n(SUCESSO) Análise de IA concluída para todas as áreas.")
    else:
        print("\n(FALHA) Execução encerrada devido a erro no carregamento dos dados.")

# Ponto de entrada do script
if __name__ == "__main__":
    main()