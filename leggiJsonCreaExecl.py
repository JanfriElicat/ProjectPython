import requests
import pandas as pd
import sys
import os    
import json
from pathlib import Path
# Scarica il file JSON da Swagger
#url = "http://localhost:9080/api/swagger/v2/api-docs"
#response = requests.get(url)
#swagger_data = response.json()
if __name__ == '__main__':
    
    fileList = os.listdir("./input")
    print(" START  ----------------------------------------------------------------\n") 
    file_json = [file for file in fileList if file.endswith('.json')]
    script_dir = Path( __file__ ).parent.absolute()    
    script_dir_parent = Path( __file__ ).parent.absolute().parent
    dir_input = f"{script_dir}\input"
    dir_output = f"{script_dir}\output"
    
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
    
    # Leggo il contenuto di ciascun file JSON in INPUT
    for file_name in file_json:
        percorso_file = os.path.join(dir_input,file_name)
        with open(percorso_file, 'r') as f:
            jsonDataIput = json.load(f)
            #print(jsonDataIput)
            # Creiamo una lista per raccogliere le informazioni
            api_list = []

            # Estraiamo le informazioni principali dagli endpoint
            for path, path_data in jsonDataIput['paths'].items():
                for method, method_data in path_data.items():
                    api_info = {
                        'Path': path,
                        'Method': method.upper(),
                        'Description': method_data.get('description', 'No description'),
                        'Summary': method_data.get('summary', 'No summary')
                    }
                    api_list.append(api_info)

            # Creiamo un DataFrame pandas
            df = pd.DataFrame(api_list)

            # Salviamo il DataFrame in un file Excel
            excelnomefile = "%s.xlsx" % (file_name.replace(".json", ""))
            fileExecl_path = os.path.join(dir_output, excelnomefile)
            print("excelnomefile=" + fileExecl_path)
            df.to_excel(fileExecl_path, index=False)

            print("Il file Excel è stato creato con successo!")
