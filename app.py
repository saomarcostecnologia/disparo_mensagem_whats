from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pandas as pd
import os

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.whatsapp.com")
    time.sleep(30)
    print('Iniciando')

    Sheet1_df = pd.read_excel("Clientes.xlsx")
    for i, DADOS in enumerate(Sheet1_df['Nome Completo']):
        Nome = Sheet1_df.loc[i, "Nome Completo"]
        Telefone = Sheet1_df.loc[i, "Telefone"]
        Ativo = Sheet1_df.loc[i, "Ativo"]
        arquivo = Sheet1_df.loc[i, "Arquivo"]

        print(Nome, Telefone)

        text = "&text="
        msgg = "Olá " + str(Nome) + ", tudo bem?"

        if Ativo == "S":
            msg = "Segue link de feedback: www.google.com.br"
            link = "https://web.whatsapp.com/send?phone=" + str(Telefone) + str(text) + str(msgg) + str(msg)
            try:
                page.goto(link)
                with page.expect_navigation():
                    page.locator("div[role=\"textbox\"]")

                with page.expect_navigation():
                    page.locator("//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span").click()
                    time.sleep(10)

            except:
                continue 
        else:
            caminho_img = os.path.abspath(f"Arquivo/{arquivo}")
            print(caminho_img)

            msg = " Seu cadastro não está ativo no momento."
            link = "https://web.whatsapp.com/send?phone=" + str(Telefone) + str(text) + str(msgg) + str(msg)
            try:
                page.goto(link)
                with page.expect_navigation():
                    page.locator("div[role=\"textbox\"]")

                with page.expect_navigation():
                    page.locator("//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span").click()
                    time.sleep(2)

                # Clicar no ícone de anexo
                attachment_button = page.locator("//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span")
                attachment_button.click()
                time.sleep(5)

                 # Selecionar o arquivo e enviar (imagem)
                file_input = page.locator("//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[2]/li/div/input")
                file_input.set_input_files(caminho_img)  # Substitua pelo caminho da imagem
                page.locator("//*[@id=\"main\"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span").click()
                time.sleep(5)


            except:
                continue 
            time.sleep(10)

        #link = "https://web.whatsapp.com/send?phone=" + str(Telefone) + str(text) + str(msgg) + str(msg)

        

with sync_playwright() as playwright:
    run(playwright)

print('Acabou')
