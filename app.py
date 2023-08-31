from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pandas as pd
import os


#Inicia no navegador
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Abre a guia
    page = context.new_page()
    page.goto("https://web.whatsapp.com")
    time.sleep(30)

    print('iniciando')
    
    #Ler a planilha
    Sheet1_df = pd.read_excel("Clientes.xlsx")
    for i, DADOS in enumerate(Sheet1_df['Nome Completo']):
        Nome = Sheet1_df.loc[i,"Nome Completo"]
        Telefone = Sheet1_df.loc[i,"Telefone"]
        #Arquivo = Sheet1_df.loc[i,"Arquivo"]

        print(Nome,Telefone)

        #variavel para envio da mensagem
        text = "&text="
        
        #Saudação + nome da planilha
        msgg = "Olá "+str(Nome)+", tudo bem?"
        
        #Mensagem após saudação + nome
        msg =  "Segue link de feedback: /n www.google.com.br"

        #Arquivo caso tenha anexo 
        #caminho_completo = os.path.abspath(f"arquivos/{Arquivo}")

        #Link já com o número e mensagens prontas pra envio (unifica todas as variaveis anteriores
        link = "https://web.whatsapp.com/send?phone="+str(Telefone)+str(text)+str(msgg)+str(msg)
              

        #Aqui é um ponto importante, ele vai tentar realizar o envio, caso não consegui vai para o proximo caso da planilha.         
        try:

            #aqui ele irá usar a guia já existente indo de item a item até finalizar planilha
            page.goto(link)

            #Aqui ele aguarda o elemento da barra de pesquisa, para ter certeza que a tela carregou. (se der erro vai para o proximo caso)
            with page.expect_navigation():# aguarda o elemento por 30 segundos por padrão
                page.locator("div[role=\"textbox\"]")

            # Se tudo der certo nas etapas anteriores, ele vai aguardar o botão de envio ficar disponivel e pertar para enviar. 
            with page.expect_navigation():# aguarda o elemento por 30 segundos por padrão
                page.locator("//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span").click()
                #page.locator("[data-testid=\"conversation-panel-wrapper\"] button").nth(4).click() 
            
            #Após o envio aguarda 10 segundos para ter certeza que a mensagem foi enviada. 
            time.sleep(10)

        #Caso as etapas anteriores do Try (Tente) derem errado ele vai para o proximo item da planilha, mas você pode colocar a saida que achar melhor.     
        except:
            continue 
                    
    # ---------------------
    #context.close()
    #browser.close()
with sync_playwright() as playwright:
    run(playwright)

print('acabou')

        

      