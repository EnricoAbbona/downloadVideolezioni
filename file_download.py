import os
import requests
from typing import Dict

def download_mp4_files(data: Dict[str, str], target_folder: str):
    """
    Scarica file MP4 da un dizionario {titolo: url}.
    
    Args:
        data (dict): Dizionario con titoli come chiavi e URL MP4 come valori.
        target_folder (str): Directory di destinazione.
    """
    
    # Creazione della cartella di destinazione se non esiste
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Cartella '{target_folder}' creata.")

    for title, url in data.items():
        # Sanitizzazione del titolo per evitare errori nel file system
        filename = f"{title.replace(' ', '_')}.mp4"
        file_path = os.path.join(target_folder, filename)
        
        print(f"Inizio download: {title}...")
        
        try:
            # Utilizzo di stream=True per non caricare l'intero file in memoria
            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status() # Controllo errori HTTP (es. 404, 500)
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
            print(f"Completato: {filename} salvato in {target_folder}.")
            
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il download di {title}: {e}")

if __name__ == "__main__":
    video_dict = dict()
    with open("elenco_download.txt", "r", encoding = "utf-8") as inf:
        for riga in inf:
            nome, link = riga.split("->")
            video_dict[nome.strip()]=link.strip()
    
    download_mp4_files(video_dict, "UrFilePath")