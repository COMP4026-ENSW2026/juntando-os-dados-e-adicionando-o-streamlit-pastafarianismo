import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import csv

def display_data():

    if os.path.exists("imoveis.csv"):
        os.remove("imoveis.csv")
    
    # Site 1 
    url1 = "http://imobiliariavenus.com.br/"
    page1 = requests.get(url1)
    soup1 = BeautifulSoup(page1.content, "html.parser")

    imoveis1 = soup1.find_all("div", class_="offer")

    # Site 2 
    url2 = "https://www.veneza.com.br/imoveis/apartamento-venda"
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.content, "html.parser")

    imoveis2 = soup2.find_all("div", class_="list__hover")

    # Progress bar
    progress_bar = st.progress(0)
    progress_text = st.empty()

    total_items = len(imoveis1) + len(imoveis2)

    # Save a CSV file
    with open("imoveis.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Site", "Título", "Endereço", "Preço", "Link"])
        
        # Site 1
        for i, imovel in enumerate(imoveis1):
            title = imovel.find("div", class_="txt1")
            other_info = imovel.find("div", class_="txt2")
            price = imovel.find("div", class_="txt3")
            link = imovel.find("a")
            
            title_text = title.text.strip() if title else ""
            other_info_text = other_info.text.strip() if other_info else ""
            price_text = price.text.strip() if price else ""
            link_text = "http://imobiliariavenus.com.br/" + link["href"] if link else ""
            
            writer.writerow([url1, title_text, other_info_text, price_text, link_text])
            
            # Update progress bar
            progress_percent = (i + 1) / total_items
            progress_bar.progress(progress_percent)
            progress_text.text(f"Progress: {int(progress_percent * 100)}%")

            time.sleep(0.1)

        # Site 2
        for i, imovel in enumerate(imoveis2):
            title = imovel.find("p", class_="list__building")
            rua = imovel.find("p", class_="list__address")
            price = imovel.find("p", class_="list__value")
            link = imovel.find("a", class_="list__link")
            
            title_text = title.text.strip() if title else ""
            rua_text = rua.text.strip() if rua else ""
            price_text = price.text.strip().replace("Comprar:", "") if price else ""
            link_text = "https://www.veneza.com.br/imoveis/apartamento-venda" + link["href"] if link else ""
            
            writer.writerow([url2, title_text, rua_text, price_text, link_text])
            
            # Update progress bar
            progress_percent = (len(imoveis1) + i + 1) / total_items
            progress_bar.progress(progress_percent)
            progress_text.text(f"Progress: {int(progress_percent * 100)}%")

    print("Informações salvas com sucesso em imoveis.csv")

    # Read the CSV file into a dataframe
    df = pd.read_csv("imoveis.csv")
    # Display the dataframe 
    st.write(df)

# Display text
st.title("My Streamlit App")
st.write("Welcome to my app!")

# Create a button
showData = st.button("Show property catalog")

# Handle button click event

if showData:
    display_data()
    st.write("Task completed!")
