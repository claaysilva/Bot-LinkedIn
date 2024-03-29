from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from time import sleep
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from asyncio import wait
import pyperclip
from funcoes import *

label_status = None  # Variável global para a etiqueta de status
def iniciar_bot(email, senha, limite_conexoes, pesquisa, mensagem):
    global label_status  # Indica que a variável será acessada globalmente
        
    # Configuração das opções do Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Maximizar a janela ao iniciar
    
    # Inicializa o serviço do Chrome e o navegador
    service = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=service, options=options)
    nav.get("https://www.linkedin.com/login/")
    
    label_status.config(text="Limite de conexões atingido", fg="green")  # Alterando a cor do texto para verde

    # Insere o email e a senha
    email_input = WebDriverWait(nav, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
    email_input.send_keys(email)
    
    senha_input = WebDriverWait(nav, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
    senha_input.send_keys(senha)
    
    # Localiza e clica no botão de login
    login_button = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')))
    login_button.click()

    
    # pesquisa = ('Analista de Sistema')
    # mensagem = ('Olá, tudo bem ? Sou o Clayton! \nEstou me conectando para aumentar minha rede e também o meu networking!')
    conexoes_feitas = 0  # Inicializando o contador de conexões feitas


    espera_aleatoria()
    nav.find_element('xpath', '//*[@id="global-nav-typeahead"]/input').click()
    espera_aleatoria()
    pyperclip.copy(pesquisa)
    espera_aleatoria()
    nav.find_element('xpath', '//*[@id="global-nav-typeahead"]/input').send_keys(Keys.CONTROL + "V")
    espera_aleatoria()
    nav.find_element('xpath', '//*[@id="global-nav-typeahead"]/input').send_keys(Keys.ENTER)
    espera_aleatoria()


    espera_aleatoria()
    # Localizar o botão pelo texto "Pessoas" dentro do elemento <ul> com o ID específico
    botao_pessoas = nav.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li//button[text()="Pessoas"]')
    botao_pessoas.click()
    espera_aleatoria()
    nav.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    espera_aleatoria()
    botao_avancar = nav.find_element(By.XPATH, '//button//span[text()="Avançar"]')
    espera_aleatoria()
    # testar a ultima pagina
    # nav.find_element('xpath', '//button[@aria-label="Página 100"]').click() 
    # espera_aleatoria()
    nav.execute_script('window.scrollTo(0, 0)')
    espera_aleatoria()


    while True:
        espera_aleatoria()
        # Verificar a presença dos botões "Conectar"
        botoes_conectar = nav.find_elements(By.XPATH, '//span[@class="artdeco-button__text" and text()="Conectar"]')
        if not botoes_conectar:
            # Se não houver botões "Conectar", clique no botão "Avançar" e continue
            nav.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            espera_aleatoria()
            botao_avancar = nav.find_element(By.XPATH, '//button//span[text()="Avançar"]')
            espera_aleatoria()
            nav.execute_script('arguments[0].click()', botao_avancar)
        else:
             # Se houver botões "Conectar", clique em cada um deles até atingir o limite
            for botao in botoes_conectar:
                # Verificar se o limite de conexões foi atingido
                if conexoes_feitas >= limite_conexoes:
                    label_status.config(text="Limite de conexões atingido.")
                    return
                espera_aleatoria()
                botao.click()
                espera_aleatoria()
                if mensagem:
                    botao_add_nota = nav.find_element(By.XPATH, '//button[@aria-label="Adicionar nota"]')
                    espera_aleatoria()
                    botao_add_nota.click()
                    espera_aleatoria()

                    campo_notas = nav.find_element(By.ID, 'custom-message')
                    digitar_devagar(campo_notas, mensagem)

                    enviar_conexao = nav.find_element(By.XPATH, '//button[@aria-label="Enviar agora"]')
                    espera_aleatoria()
                    enviar_conexao.click()
                else:
                    enviar_conexao = nav.find_element(By.XPATH, '//button[@aria-label="Enviar agora"]')
                    espera_aleatoria()
                    enviar_conexao.click()
                
                # Incrementar o contador de conexões feitas    
                conexoes_feitas += 1

# Função para criar a interface gráfica
def criar_interface():
    global label_status  # Indica que a variável será acessada globalmente
    # Função para iniciar o bot quando o botão for pressionado
    def iniciar_bot_interface():
      email = entry_email.get()
      senha = entry_senha.get()
      limite_conexoes = int(entry_limite_conexoes.get())  # Converter para inteiro
      pesquisa = entry_pesquisa.get()  # Obtendo a pesquisa do campo de entrada
      mensagem = entry_mensagem.get("1.0", "end-1c")  # Obtendo o texto da caixa de entrada de textoy
      iniciar_bot(email, senha, limite_conexoes, pesquisa, mensagem)

    # Criar janela
    janela = tk.Tk()
    janela.title("Bot do LinkedIn")
    janela.geometry("600x500")  # Definindo o tamanho da janela
    
    # Criar um frame para organizar os elementos
    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    # Criar rótulo e entrada para o e-mail
    label_email = tk.Label(frame, text="Email:", font=("Helvetica", 12))  
    label_email.pack(anchor="center", padx=20, pady=5)  

    entry_email = tk.Entry(frame, font=("Helvetica", 12), width=40)  # Definindo a largura
    entry_email.pack(anchor="center", padx=20, pady=5)  

    # Criar rótulo e entrada para a senha
    label_senha = tk.Label(frame, text="Senha:", font=("Helvetica", 12))  
    label_senha.pack(anchor="center", padx=20, pady=5)  

    entry_senha = tk.Entry(frame, show="*", font=("Helvetica", 12), width=40)  # Definindo a largura
    entry_senha.pack(anchor="center", padx=20, pady=5)  

    # Criar rótulo e entrada para o limite de conexões
    label_limite_conexoes = tk.Label(frame, text="Limite de Conexões:", font=("Helvetica", 12))  
    label_limite_conexoes.pack(anchor="center", padx=20, pady=5)  

    entry_limite_conexoes = tk.Entry(frame, font=("Helvetica", 12), width=40)  # Definindo a largura
    entry_limite_conexoes.pack(anchor="center", padx=20, pady=5)  

    # Criar rótulo e entrada para a pesquisa
    label_pesquisa = tk.Label(frame, text="Pesquisa:", font=("Helvetica", 12))  
    label_pesquisa.pack(anchor="center", padx=20, pady=5)  

    entry_pesquisa = tk.Entry(frame, font=("Helvetica", 12), width=40)  # Definindo a largura
    entry_pesquisa.pack(anchor="center", padx=20, pady=5)  


    # Criar caixa de texto para a mensagem
    label_mensagem = tk.Label(frame, text="Mensagem:", font=("Helvetica", 12))  
    label_mensagem.pack(anchor="center", padx=20, pady=5)  

    entry_mensagem = tk.Text(frame, font=("Helvetica", 12), wrap="word", width=30, height=5)  # Definindo a largura e altura
    entry_mensagem.pack(anchor="center", padx=20, pady=5)  


    # Botão para iniciar o bot
    botao_iniciar = tk.Button(frame, text="Iniciar Bot", font=("Helvetica", 12), command=iniciar_bot_interface)  # Alterando a fonte
    botao_iniciar.pack(pady=10)  # Adicionando espaço vertical

    # Etiqueta para exibir o status
    label_status = tk.Label(frame, text="", font=("Helvetica", 12))  # Alterando a fonte
    label_status.pack(anchor="center", padx=20, pady=5)  # Centralizando horizontalmente e adicionando espaços

    # Executar a janela
    janela.mainloop()

# Chamar a função para criar a interface
criar_interface()
