from bs4 import BeautifulSoup  
import requests  
import urllib.parse  
import os  
import pandas as pd  
import streamlit as st

def formata_dados(csv):
    df = pd.read_csv(csv, sep = ',', thousands='.', decimal=',')
    df['Reviews'] = df['Reviews'].str.replace(r'[()]', '', regex=True)
    df['Reviews'] = df['Reviews'].astype(int)

    return df 

def get_top_10(df):
    df = pd.read_csv(csv, sep = ',', thousands='.', decimal=',')
    df['Reviews'] = df['Reviews'].str.replace(r'[()]', '', regex=True)
    df['Reviews'] = df['Reviews'].astype(int)

    df_crescente = df.sort_values(by='Reviews', ascending=False).reset_index(drop=True)
    df_top10 = df_crescente.head(10)

    return df_top10

def analise_full_top(df):
    #? Análise Full
    full_qtd = df_top10[df_top10['Full'] == 'full'].shape[0]
    
    return full_qtd

def vendas_top(df):
    media_top_vendas = df['Reviews'].mean()
    max_top_vendas = df['Reviews'].max()
    min_top_venda = df['Reviews'].min()
    
    df_full = df[df['Full'] == 'full']  # Filtra os produtos que são Full
    media_full_vendas_top = df_full['Reviews'].mean() if not df_full.empty else 0
    max_full_vendas_top = df_full['Reviews'].max() if not df_full.empty else 0
    min_full_venda_top = df_full['Reviews'].min() if not df_full.empty else 'Nenhuma venda'
    soma_total = df['Reviews'].sum()

    # Retorna a análise geral e a análise dos produtos Full
    return {
        "media_top_vendas": media_top_vendas,
        "max_top_vendas": max_top_vendas,
        "min_top_venda": min_top_venda,
        "media_full_vendas": media_full_vendas_top,
        "max_full_vendas": max_full_vendas_top,
        "min_full_venda": soma_total
    }

def analise_faixa_top(df):
    
    faixas = [0, 50, 100, 200, 500, float('inf')]
    rotulos = ['0-50', '51-100', '101-200', '201-500', '501+']
    
    
    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    
   
    df = df.dropna(subset=['Preço'])  

    
    df['Faixa de Preço'] = pd.cut(df['Preço'], bins=faixas, labels=rotulos, right=False)
    
    
    faixa_contagem = df['Faixa de Preço'].value_counts().sort_index()
    
    return faixa_contagem

    return faixa_contagem

def analise_preco_top(df):
    #?  Análise de Preço
    media_top_preco = df_top10['Preço'].mean()
    max_top_preco = df_top10['Preço'].max()
    min_top_preco = df_top10['Preço'].min()
    
    return media_top_preco, max_top_preco, min_top_preco

def analise_preco_geral(df):
    #? - Preço
    media_geral_preco = df['Preço'].mean()
    max_geral_preco = df['Preço'].max()
    min_geral_preco = df['Preço'].min()
    return media_geral_preco, max_geral_preco, min_geral_preco

def analise_faixa_geral(df):
   
    faixas = [0, 50, 100, 200, 500, float('inf')]
    rotulos = ['0-50', '51-100', '101-200', '201-500', '501+']
    
   
    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    
   
    df = df.dropna(subset=['Preço'])  

    
    df['Faixa de Preço'] = pd.cut(df['Preço'], bins=faixas, labels=rotulos, right=False)
    
    
    faixa_contagem = df['Faixa de Preço'].value_counts().sort_index()
    
    return faixa_contagem

def  analise_full_geral(df):   
    #? Análise Full
    full_qtd = df[df['Full'] == 'full'].shape[0]

    return full_qtd

def grafico_vendas_preco(df):
    
    faixas = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, float('inf')]  
    rotulos = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '301-350', '351-400', '401-450', '451-500', '501+']
    
    
    df['Faixa de Preço'] = pd.cut(df['Preço'], bins=faixas, labels=rotulos, right=False)
    
    
    faixa_vendas = df.groupby('Faixa de Preço')['Reviews'].sum().reset_index()

    
    faixa_vendas = faixa_vendas.sort_values('Faixa de Preço')  

    
    st.line_chart(faixa_vendas.set_index('Faixa de Preço')['Reviews'])

def grafico_vendas_anuncios(df):

    faixas = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, float('inf')]  
    rotulos = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '301-350', '351-400', '401-450', '451-500', '501+']
    
    df['Faixa de Preço'] = pd.cut(df['Preço'], bins=faixas, labels=rotulos, right=False)
    
    faixa_anuncios = df.groupby('Faixa de Preço').size().reset_index(name='Quantidade de Anúncios')

    faixa_anuncios = faixa_anuncios.sort_values('Faixa de Preço')  

    st.bar_chart(faixa_anuncios.set_index('Faixa de Preço')['Quantidade de Anúncios'])

def analise_vendas_gerais(df):
    #?  Análise Vendas
    media_geral_vendas = df['Reviews'].mean()
    max_geral_vendas = df['Reviews'].max()
    min_geral_venda = df['Reviews'].min()
    soma_total = df['Reviews'].sum()
    
    # Análise de vendas dos produtos Full
    df_full = df[df['Full'] == 'full']  # Filtra os produtos que são Full
    media_full_vendas = df_full['Reviews'].mean() if not df_full.empty else 0
    max_full_vendas = df_full['Reviews'].max() if not df_full.empty else 0
    min_full_venda = df_full['Reviews'].min() if not df_full.empty else 'Nenhuma venda'

    # Retorna a análise geral e a análise dos produtos Full
    return {
        "media_geral_vendas": media_geral_vendas,
        "max_geral_vendas": max_geral_vendas,
        "min_geral_venda": min_geral_venda,
        "media_full_vendas": media_full_vendas,
        "max_full_vendas": max_full_vendas,
        "min_full_venda": soma_total
    }

def get_tamanho(df):
    df = pd.read_csv(csv, sep = ',', thousands='.', decimal=',')

    n_linhas = df.shape[0]

    return f"Quantidade de anuúncios: {n_linhas}"

def scraping(produto):
    produto_split = produto.split()  # Divide o nome do produto em palavras.
    produto_join = "-".join(produto_split)  # Junta as palavras com hífens para formar a URL.
    produto_urllib = urllib.parse.quote(produto)  # Codifica o nome do produto para a URL.
    url = f"https://lista.mercadolivre.com.br/{produto_join}#D[A:{produto_urllib}]"
        
    try:
        os.system("cls")  # Limpa o terminal.
        response = requests.get(url)  # Realiza a requisição HTTP para a URL do Mercado Livre.
        soup = BeautifulSoup(response.text, 'html.parser')  # Faz o parsing do HTML da página.
        
        products = soup.find_all('li', {'class': 'ui-search-layout__item'})

        nomes = []
        precos = []
        fulls = [] 
        urls = []
        reviews = []
        descricao = []

        for product in products:
            name_tag = product.find('a', {'class': 'poly-component__title'})
            link_tag = product.find('a', {'class': 'poly-component__title'})
            price_tag = product.find('span', {'class': 'andes-money-amount__fraction'})
            review_tag = product.find('span', {'class': 'poly-reviews__total'})
            full_tag = product.find('span', {'class': 'poly-component__shipped-from'})
            


            nome = name_tag.text.strip() if name_tag else 0
            preco = price_tag.text.strip() if price_tag else 0
            review = review_tag.text.strip() if review_tag else 0
            full = 'full' if full_tag else 0  
            url = link_tag['href'] if link_tag else 0  

            
            nomes.append(nome)
            precos.append(preco)
            fulls.append(full)
            urls.append(url)
            reviews.append(review)


        # Criar DataFrame
        df = pd.DataFrame({
                'Nome do Produto': nomes,
                'Preço': precos,
                'Full': fulls,
                'Url': urls,
                'Reviews': reviews,
            })

        csv_path = 'pesquisa.csv'
        if os.path.exists(csv_path):
            os.remove(csv_path)

        df.to_csv(csv_path, index=False)

        return csv_path  

    except Exception as e:
        print(f'Erro: {e}')

def getAnuncioPreco(df, produto, preco):
    df = pd.read_csv(csv, sep = ',', thousands='.', decimal=',')
    df_analise = df[['Nome do Produto', 'Preço']]
    
    df_nosso_produto = pd.DataFrame({'Nome do Produto': [produto], 'Preço':[preco] })

    df_final = pd.concat([df_analise, df_nosso_produto], ignore_index=True)

    df_padronizado = df_final.sort_values(by='Preço', ascending=True).reset_index(drop=True)

    produto_index = df_padronizado[df_padronizado['Nome do Produto'] == produto].index[0]

    produto_index += 1
    
    return f"Posição do anuncio em relação a Preco: {produto_index}"

def print_links(df):
     # Leitura do CSV e processamento dos dados
    df = pd.read_csv(csv, sep=',', thousands='.', decimal=',')
    df['Reviews'] = df['Reviews'].str.replace(r'[()]', '', regex=True)
    df['Reviews'] = df['Reviews'].astype(int)
    
    df_crescente = df.sort_values(by='Reviews', ascending=False).reset_index(drop=True)
    df_top10 = df_crescente.head(10)

    # Exibindo URLs numeradas no Streamlit
    for idx, url in enumerate(df_top10['Url'], 1):
        # Exibindo cada URL com um estilo visual
        st.markdown(f"""
        <div style='background-color: #1b202b; padding: 10px; border-radius: 8px; margin-bottom: 8px;'>
            <p style='font-size: 16px; font-weight: bold; color: #333;'> 
                <span style='color: #ef8d2d;'>{idx}.</span> 
                <a href='{url}' target='_blank' style='color: #1E88E5; text-decoration: none;'> 
                    {url}
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)

def get_descs(df):
    # Garantir que a coluna 'Reviews' seja tratada como string
    df['Reviews'] = df['Reviews'].astype(str)
    
    # Remover os caracteres indesejados usando .str.replace()
    df['Reviews'] = df['Reviews'].str.replace(r'[()]', '', regex=True)
    
    # Converter para inteiro após a limpeza
    df['Reviews'] = df['Reviews'].astype(int)
    
    # Ordenando e pegando os 10 primeiros produtos
    df_crescente = df.sort_values(by='Reviews', ascending=False).reset_index(drop=True)
    df_top10 = df_crescente

    descs = []

    for url in df_top10['Url']:
        response_link = requests.get(url)
        soup_link = BeautifulSoup(response_link.text, 'html.parser')

        # Pega a descrição do produto
        desc_tag = soup_link.find('p', {'class': 'ui-pdp-description__content'})
        desc = desc_tag.text.strip() if desc_tag else "Descrição não encontrada"
        
        descs.append(desc)

    # Agora cria um novo DataFrame com as descrições
    df_top10['Descricao'] = descs

    # Salva em um novo arquivo CSV
    csv_path = 'descs.csv'
    df_top10.to_csv(csv_path, index=False)

    return df_top10

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re

nltk.download('stopwords')
nltk.download('punkt')

def extrair_palavras_chave_nltk(df):
    if isinstance(df, pd.DataFrame) and 'Descricao' in df.columns:
  
        stopwords2 = [
    "mm", "cm", "m", "km", "g", "kg", "t", "lb", "oz", "V", "A", "W", "kW", "kVA", "kWh", "Hz", "rpm", 
    "s", "min", "h", "d", "pol", "inch", "ft", "yd", "l", "ml", "gal", "oz", "°C", "°F", "%", 
    "m²", "cm²", "mm²", "in²", "ft²", "m³", "cm³", "mm³", "in³", "gal/h", "l/h", "dB", "db", 
    "db(A)", "dBA", "dB SPL", "lux", "K", "S", "A", "B", "C", "D", "E", "F", "G", "H", "J", "L", 
    "M", "N", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "v ","Z", "hr", "min", "sec", "pç", "un", "c/", 
    "em", "até", "por", "com", "sem", "cada", "de", "do", "da", "dos", "das", "a", "à", "ou", "para", 
    "ao", "uma", "um", "os", "as", "alt", "largo", "comprimento", "peso", "capacidade", "máximo", 
    "mínimo", "standard", "numero", "tipo", "uso", "utilizado", "classificação", "modelo", "sistema"
]



        descricoes = ' '.join(df['Descricao'].dropna().values)
        descricoes_limpa = re.sub(r'[^a-zA-Z\s]', '', descricoes.lower())
        palavras = nltk.word_tokenize(descricoes_limpa)

        stop_words = set(stopwords.words('portuguese')) 
        palavras_filtradas = [palavra for palavra in palavras if palavra not in stop_words and stopwords2] 


        freq_dist = FreqDist(palavras_filtradas)

        palavras_comuns = freq_dist.most_common(5)

        for idx, (palavra, contagem) in enumerate(palavras_comuns, 1):
            st.markdown(f"""
            <div style='background-color: #1b202b; padding: 10px; border-radius: 8px; margin-bottom: 8px;'>
                <p style='font-size: 16px; font-weight: bold; color: #333;'> 
                    <span style='color: #ef8d2d;'>{idx}.</span> 
                    <span style='color: #1E88E5;'> 
                        {palavra} - {contagem} vezes
                    </span>
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("DataFrame ou coluna 'Descricao' não encontrada!")

def extrair_palavras_chave_nltk2(df):
    if isinstance(df, pd.DataFrame) and 'Nome do Produto' in df.columns:
        
        stopwords2 = [
    "mm", "cm", "m", "km", "g", "kg", "t", "lb", "oz", "V", "A", "W", "kW", "kVA", "kWh", "Hz", "rpm", 
    "s", "min", "h", "d", "pol", "inch", "ft", "yd", "l", "ml", "gal", "oz", "°C", "°F", "%", 
    "m²", "cm²", "mm²", "in²", "ft²", "m³", "cm³", "mm³", "in³", "gal/h", "l/h", "dB", "db", 
    "db(A)", "dBA", "dB SPL", "lux", "K", "S", "A", "B", "C", "D", "E", "F", "G", "H", "J", "L", 
    "M", "N", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "v ","Z", "hr", "min", "sec", "pç", "un", "c/", 
    "em", "até", "por", "com", "sem", "cada", "de", "do", "da", "dos", "das", "a", "à", "ou", "para", 
    "ao", "uma", "um", "os", "as", "alt", "largo", "comprimento", "peso", "capacidade", "máximo", 
    "mínimo", "standard", "numero", "tipo", "uso", "utilizado", "classificação", "modelo", "sistema"
]


        descricoes = ' '.join(df['Nome do Produto'].dropna().values)
        descricoes_limpa = re.sub(r'[^a-zA-Z\s]', '', descricoes.lower())
        palavras = nltk.word_tokenize(descricoes_limpa)

        stop_words = set(stopwords.words('portuguese')) 
        palavras_filtradas = [palavra for palavra in palavras if palavra not in stop_words and stopwords2]


        freq_dist = FreqDist(palavras_filtradas)

        palavras_comuns = freq_dist.most_common(5)

        for idx, (palavra, contagem) in enumerate(palavras_comuns, 1):
            st.markdown(f"""
            <div style='background-color: #1b202b; padding: 10px; border-radius: 8px; margin-bottom: 8px;'>
                <p style='font-size: 16px; font-weight: bold; color: #333;'> 
                    <span style='color: #ef8d2d;'>{idx}.</span> 
                    <span style='color: #1E88E5;'> 
                        {palavra} - {contagem} vezes
                    </span>
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("DataFrame ou coluna 'Nome do Produto' não encontrada!")

import streamlit as st

st.set_page_config(
    page_title="App Marketplace",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('''# Análise de Mercado - Marketplace''')

st.markdown('---')

produto = st.text_input('Produto a ser pesquisado', placeholder="Digite o nome do produto que deseja pesquisar")
preco_pesquisa = st.number_input('Preço do produto sem decimais:', placeholder='R$', value=None)

csv = scraping(produto)
df_tratado = formata_dados(csv)

st.header(f'Análise dos Produtos na Página de Busca: :orange[{produto}]')

preco, faixa, vendas = st.columns(3, vertical_alignment="top", border=True)

with preco:
    st.subheader('Análise Preço e Full')
    st.markdown(f'''
    - {get_tamanho(df_tratado)} 
    - Quantidade Anúncios no Full:  {analise_full_geral(df_tratado)}
    - Média De Preço Geral:  R${analise_preco_geral(df_tratado)[0]:.2f}
    - Preço Mais alto:  R${analise_preco_geral(df_tratado)[1]:.2f}
    - Preço Mais baixo:  R${analise_preco_geral(df_tratado)[2]:.2f}
    ''')

with faixa:
    st.subheader('Faixa de Preço:')
    faixa_contagem = analise_faixa_geral(df_tratado)
    totais_faixas = []
    for faixa, contagem in faixa_contagem.items():
        totais_faixas.append(contagem)
    st.markdown(f'''
    - Valores Até 50 Reais:  {totais_faixas[0]} anúncios
    - Valores De 51 a 100 Reais:  {totais_faixas[1]} anúncios
    - Valores De 101 a 200 Reais:  {totais_faixas[2]} anúncios
    - Valores De 201 a 500 Reais:  {totais_faixas[3]} anúncios
    - Superior a 500 Reais:  {totais_faixas[-1]} anúncios
    ''')

with vendas:
    st.subheader('Vendas:')
    vendas_gerais = analise_vendas_gerais(df_tratado)
    st.markdown(f'''
    - Média de Vendas Por Anúncio: { vendas_gerais["media_geral_vendas"]:.0f}
    - Anúncio com mais vendas:  {vendas_gerais["max_geral_vendas"]:.0f}
    - Anúncio com menos vendas:  {vendas_gerais["min_geral_venda"]:.0f}
    - Anúncio com mais vendas Full:  {vendas_gerais["max_full_vendas"]:.0f}
    - Total de vendas da Páginas:  {vendas_gerais["min_full_venda"]:.0f}
    ''')


st.header(f'Análise dos 10 Produtos Com Maior Qtd Vendas: :orange[{produto}]')

preco_top, faixa_top, vendas_tops = st.columns(3, vertical_alignment="top", border=True)

df_top10 = get_top_10(csv)

with preco_top:
    st.subheader('Análise Preço e Full')
    st.markdown(f'''
    - Quantidade Anúncios Pesquisados: 10 
    - Quantidade Anúncios no Full:  {analise_full_top(df_top10)}
    - Média De Preço Geral:  R${analise_preco_top(df_top10)[0]:.2f}
    - Preço Mais alto Geral:  R${analise_preco_top(df_top10)[1]:.2f}
    - Preço Mais baixo Geral:  R${analise_preco_top(df_top10)[2]:.2f}
    ''')

with faixa_top:
    st.subheader('Faixa de Preço:')
    faixa_contagem = analise_faixa_top(df_top10)
    totais_faixas_top = []
    for faixa, contagem in faixa_contagem.items():
        totais_faixas_top.append(contagem)
    st.markdown(f'''
    - Valores Até 50 Reais:  {totais_faixas_top[0]} anúncios
    - Valores De 51 a 100 Reais:  {totais_faixas_top[1]} anúncios
    - Valores De 101 a 200 Reais:  {totais_faixas_top[2]} anúncios
    - Valores De 201 a 500 Reais:  {totais_faixas_top[3]} anúncios
    - Superior a 500 Reais:  {totais_faixas_top[-1]} anúncios
    ''')

with vendas_tops:
    st.subheader('Vendas:')
    vendas_gerais_top = vendas_top(df_top10)
    st.markdown(f'''
    - Média de Vendas Por Anúncio: { vendas_gerais_top["media_top_vendas"]:.0f}
    - Anúncio com mais vendas:  {vendas_gerais_top["max_top_vendas"]:.0f}
    - Anúncio com menos vendas:  {vendas_gerais_top["min_top_venda"]:.0f}
    - Anúncio com mais vendas Full:  {vendas_gerais_top["max_full_vendas"]:.0f}
    - Total de vendas do Top 10:  {vendas_gerais_top["min_full_venda"]:.0f}
    ''')

if preco_pesquisa:
    st.markdown(f'''
    ## {getAnuncioPreco(df_tratado,produto, preco_pesquisa)}
    ''')
else:
    st.markdown(f'''
    ## Posição do anuncio em relação a Preco: 
    ''')

st.subheader('Palavras Chave Descrição:')
col1, col2 = st.columns(2)

with col1:
    if st.button('Gerar Palavras-chave mais frequentes Descrição'):
        dfs = get_descs(df_tratado)
        extrair_palavras_chave_nltk(dfs)

with col2:
    if st.button('Gerar Palavras-chave mais frequentes Titulo'):
        dfs = get_descs(df_tratado)
        extrair_palavras_chave_nltk2(dfs)

st.header('Quantidade de Venda por Faixa de Preço')
grafico_vendas_preco(df_tratado)

st.header('Quantidade de Anúncios por Faixa de Preço')
grafico_vendas_anuncios(df_tratado)

st.header('Url dos anúncios melhor rankeados:')
print_links(df_top10)
