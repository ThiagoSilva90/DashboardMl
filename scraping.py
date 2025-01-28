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

def analise_full_geral(df):   
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

def scraping(produto):
    # Divide o nome do produto em palavras para filtros e formata a URL.
    palavras_filtro = produto.lower().split()
    produto_join = "-".join(palavras_filtro)
    produto_urllib = urllib.parse.quote(produto)
    
    base_url = f"https://lista.mercadolivre.com.br/{produto_join}#D[A:{produto_urllib}]"

    try:
        os.system("cls")  # Limpa o terminal.

        # Variáveis para armazenar os resultados
        nomes = []
        precos = []
        fulls = [] 
        urls = []
        reviews = []

        pagina = 1

        while len(nomes) < 50:
            # Constrói a URL com paginação
            url = f"{base_url}&page={pagina}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            products = soup.find_all('li', {'class': 'ui-search-layout__item'})

            if not products:
                print("Nenhum produto encontrado ou fim das páginas.")
                break

            for product in products:
                # Extrai as informações dos produtos
                name_tag = product.find('a', {'class': 'poly-component__title'})
                link_tag = product.find('a', {'class': 'poly-component__title'})
                price_tag = product.find('span', {'class': 'andes-money-amount__fraction'})
                review_tag = product.find('span', {'class': 'poly-reviews__total'})
                full_tag = product.find('span', {'class': 'poly-component__shipped-from'})

                # Obtém os dados, garantindo que existam
                nome = name_tag.text.strip().lower() if name_tag else 0
                preco = price_tag.text.strip() if price_tag else 0
                review = review_tag.text.strip() if review_tag else 0
                full = 'full' if full_tag else 0
                url = link_tag['href'] if link_tag else 0

                # Verifica se todas as palavras do filtro estão no título
                if all(palavra in nome for palavra in palavras_filtro):
                    nomes.append(nome)
                    precos.append(preco)
                    fulls.append(full)
                    urls.append(url)
                    reviews.append(review)

                # Sai do loop se já houver 50 produtos relevantes
                if len(nomes) >= 50 or pagina == 4:
                    break

            # Avança para a próxima página
            pagina += 1

        # Criar DataFrame
        df = pd.DataFrame({
            'Nome do Produto': nomes,
            'Preço': precos,
            'Full': fulls,
            'Url': urls,
            'Reviews': reviews,
        })

        # Salva o DataFrame em um arquivo CSV
        csv_path = 'pesquisa.csv'
        if os.path.exists(csv_path):
            os.remove(csv_path)

        df.to_csv(csv_path, index=False)

        return csv_path  # Retorna o caminho do CSV

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
   
    df = pd.read_csv(csv, sep=',', thousands='.', decimal=',')
    df['Reviews'] = df['Reviews'].str.replace(r'[()]', '', regex=True)
    df['Reviews'] = df['Reviews'].astype(int)

    df_crescente = df.sort_values(by='Reviews', ascending=False).reset_index(drop=True)

    nomes_exibidos = set()
    links_exibidos = []

    for idx, row in df_crescente.iterrows():
        nome_produto = row['Nome do Produto'].lower()  
        url_produto = row['Url']

        if nome_produto not in nomes_exibidos:
            st.markdown(f"""
            <div style='background-color: #1b202b; padding: 10px; border-radius: 8px; margin-bottom: 8px;'>
                <p style='font-size: 16px; font-weight: bold; color: #333;'> 
                    <span style='color: #ef8d2d;'>{links_exibidos.__len__() + 1}.</span> 
                    <a href='{url_produto}' target='_blank' style='color: #1E88E5; text-decoration: none;'> 
                        {row['Nome do Produto']}
                    </a>
                </p>
            </div>
            """, unsafe_allow_html=True)

            nomes_exibidos.add(nome_produto)
            links_exibidos.append(url_produto)

        if len(links_exibidos) >= 10:
            break

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

media_geral, max_geral, min_geral = analise_preco_geral(df_tratado)

with preco:
    st.subheader('Análise Preço e Full')
    st.markdown(f'''
    - Anúncios Coletados: {df_tratado.shape[0]} anúncios
    - Quantidade Anúncios no Full:  {analise_full_geral(df_tratado)} anúncios
    - Média De Preço Geral:  R${media_geral:.2f}
    - Preço Mais alto:  R${max_geral:.2f}
    - Preço Mais baixo:  R${min_geral:.2f}
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

media_top, max_top, min_top = analise_preco_geral(df_top10)

with preco_top:
    st.subheader('Análise Preço e Full')
    st.markdown(f'''
    - Quantidade Anúncios Pesquisados: 10 
    - Quantidade Anúncios no Full:  {analise_full_geral(df_top10)}
    - Média De Preço Geral:  R${media_top:.2f}
    - Preço Mais alto Geral:  R${max_top:.2f}
    - Preço Mais baixo Geral:  R${min_top:.2f}
    ''')

with faixa_top:
    st.subheader('Faixa de Preço:')
    faixa_contagem = analise_faixa_geral(df_top10)
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
    vendas_gerais = analise_vendas_gerais(df_top10)
    st.markdown(f'''
    - Média de Vendas Por Anúncio: { vendas_gerais["media_geral_vendas"]:.0f}
    - Anúncio com mais vendas:  {vendas_gerais["max_geral_vendas"]:.0f}
    - Anúncio com menos vendas:  {vendas_gerais["min_geral_venda"]:.0f}
    - Anúncio com mais vendas Full:  {vendas_gerais["max_full_vendas"]:.0f}
    - Total de vendas da Páginas:  {vendas_gerais["min_full_venda"]:.0f}
    ''')

if preco_pesquisa:
    st.markdown(f'''
    ## {getAnuncioPreco(df_tratado,produto, preco_pesquisa)}
    ''')
else:
    st.markdown(f'''
    ## Posição do anuncio em relação a Preco: 
    ''')

st.header('Quantidade de Venda por Faixa de Preço')
grafico_vendas_preco(df_tratado)

st.header('Quantidade de Anúncios por Faixa de Preço')
grafico_vendas_anuncios(df_tratado)

st.header('Url dos anúncios melhor rankeados:')
print_links(df_tratado)
