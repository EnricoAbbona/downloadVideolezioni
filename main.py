import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

driver = webdriver.Chrome()

def estrai_video_corso():
    try:
        driver.get("") #PER USER: inserisci qui l'URL della pagina di login (es https://didattica.polito.it/login)
        wait = WebDriverWait(driver, 80) #PER USER: cambia per avere più tempo di effettuare il login

        print("Ricerca del menu lezioni...")
        navbar_ul = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul[id^='navbar_left_menu_']")
        ))
        
        id_corso = navbar_ul.get_attribute("id").split("_")[-1]
        print(f"Rilevato ID Corso: {id_corso}")

        lezioni_li = navbar_ul.find_elements(By.TAG_NAME, "li")
        print(f"Trovate {len(lezioni_li)} lezioni.")

        video_sources = []

        for index in range(len(lezioni_li)):
            navbar_ul = driver.find_element(By.ID, f"navbar_left_menu_{id_corso}")
            current_li = navbar_ul.find_elements(By.TAG_NAME, "li")[index]
            
            link = current_li.find_element(By.TAG_NAME, "a")
            titolo = link.text
            
            print(f"Analizzando: {titolo}")
            
            driver.execute_script("arguments[0].click();", link)
            
            try:
                video_xpath = f"//video[contains(@id, 'videoPlayer_')]"
                wait.until(EC.presence_of_element_located((By.XPATH, video_xpath)))
                
                time.sleep(2)
                
                video_element = driver.find_element(By.XPATH, video_xpath)
                source_element = video_element.find_element(By.TAG_NAME, "source")
                
                src = source_element.get_attribute("src")
                print(f"Successo! URL: {src}")
                video_sources.append({"titolo": titolo, "url": src})
                
            except Exception as e:
                print(f"Non è stato possibile recuperare il video per questa lezione: {e}")

        print("\n--- ELENCO DOWNLOAD ---")
        with open("elenco_download.txt", "w", encoding="utf-8") as f:
            for v in video_sources:
                f.write(f"{v['titolo']} -> {v['url']}\n")
                print(f"{v['titolo']} -> {v['url']}")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    estrai_video_corso()