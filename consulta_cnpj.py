from time import sleep
from selenium.webdriver.common.by import By
import captcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def consultar_cnpj(navegador, url, dataframe):
        navegador.get(url)

        campo_cnpj = navegador.find_element(By.XPATH, "//input[@id='cnpj']")
        for num_cnpj in dataframe[0]:
            campo_cnpj.send_keys(num_cnpj)
            sleep(0.1)
        sleep(0.5)

        campo_imagem_captcha = navegador.find_element(By.XPATH, "//img[@id='imgCaptcha']")
        campo_texto_captcha = navegador.find_element(By.XPATH, "//input[@id='txtTexto_captcha_serpro_gov_br']")
        caminho_arquivo_imagem = 'captcha.png'
        with open(caminho_arquivo_imagem, 'wb') as arquivo_img:arquivo_img.write(campo_imagem_captcha.screenshot_as_png)
        resposta_captcha = captcha.resolver_captcha_imagem('captcha.png')
        campo_texto_captcha.send_keys(resposta_captcha.get('code', ''))
        print(resposta_captcha.get('code', ''))  

        navegador.find_element(By.XPATH, "//button[normalize-space()='Consultar']").click()
        sleep(2)

def validar_busca_cnpj(navegador):
    try:
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='principal']/table[1]/tbody")))
        return True
    except TimeoutException:
        erro_busca = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-danger']")))
        erro_cnpj_invalido = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'O número do CNPJ não é válido. Verifique se o mesm')]")))
    if erro_busca:
        print(erro_busca.text)
        raise ValueError(f'Erro esperado ao tentar consultar CNPJ - {erro_busca.text}')
    if erro_cnpj_invalido:
        print(erro_cnpj_invalido.text)
        raise ValueError(f'Erro esperado ao tentar consultar CNPJ  - {erro_cnpj_invalido.text}')
    return None

def obter_dados_cnpj(navegador):
    dados_cnpj = []
    
    numero_cnpj = navegador.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[2]/tbody[1]/tr[1]/td[1]").text.split('\n')[1]
    nome_empresarial = navegador.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[3]/tbody[1]/tr[1]").text.split('\n')[1]
    atividade_economica = navegador.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[5]/tbody[1]/tr[1]").text.split('\n')[1]
    natureza_juridica = navegador.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[7]/tbody[1]/tr[1]/td[1]").text.split('\n')[1]

    dados_cnpj.append({
                'CNPJ': numero_cnpj,
                'NOME EMPRESARIAL': nome_empresarial,
                'CODIGO E DESCRICAO DA ATIVIDADE ECONOMICA PRINCIPAL': atividade_economica,
                'CODIGO E DESCRICAO DA NATUREZA JURIDICA': natureza_juridica
            })

    return dados_cnpj

