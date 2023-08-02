import os
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import consulta_cnpj


INPUT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input', 'input-cnpj.csv')
OUTPUT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

input_cnpj_df = pd.read_csv(INPUT)
print(input_cnpj_df)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
navegador = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
url = 'https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao_CS.asp'

cnpjs_obtidos = []
max_tentativas = 2
for cnpj in input_cnpj_df['CNPJs']:
    for tentativa in range(max_tentativas):
        try:
            consulta_cnpj.consultar_cnpj(navegador, url, [cnpj])
            consulta_cnpj.validar_busca_cnpj(navegador)
            print(f'CNPJ encontrado!')
            dados_obtidos = consulta_cnpj.obter_dados_cnpj(navegador)
            print(dados_obtidos)
            cnpjs_obtidos.extend(dados_obtidos)
            break  # Se a consulta foi bem-sucedida, saia do loop de tentativas
        except ValueError as e:
            print(f'CNPJ não encontrado!')
        except Exception as e:
            print(f'Erro: {e}')
    else:
        print(f'Não foi possível obter os dados para o CNPJ {cnpj} após {max_tentativas} tentativas.')
        
output_cnpj_df = pd.DataFrame(cnpjs_obtidos)
output_cnpj_df.drop_duplicates(subset=['CNPJ'], inplace=True)
output_cnpj_df.to_excel(f'{OUTPUT}\\output-cnpj.xlsx', index=False)
print('Output gerado com sucesso!')
navegador.quit()

