# Built-in imports
import logging, os, sys, traceback, json, time
from typing import List, Optional, Tuple, Any, Dict
from getpass import getpass

# Third-party imports
import pandas as pd

# Local imports
from Transformer import *
from Database import Database
from GUI import HomeGUI, ProcessingGUI
from User import User

logging.basicConfig(level=logging.INFO)

def authenticate_user(max_retries: int = 3) -> None:
    print("Por favor insira suas credenciais para acessar o sistema.")
    
    for retry in range(max_retries):
        try:
            username: str = input("Usuário (e-mail institucional): ")
            password: str = getpass("Senha: ")
            
            user: User = User(username, password)
            
        except Exception as e:
            print(''.join(traceback.format_exception(*sys.exc_info())))
            print("\n")
            print(f"Falha na autenticação. Tentativa {retry + 1} de {max_retries}.")
            
            if retry < max_retries - 1:
                print("Tente novamente.\n")
            else:
                print("\nNúmero máximo de tentativas atingido. Encerrando o programa.")
                sys.exit(1)
        
        else:
            return

def main() -> None:
    # authenticate_user()
    # print("\nAutenticação bem-sucedida. Iniciando o sistema...")
    
    # h: HomeGUI = HomeGUI()
    # h.run()
    # FILE_PATH = h.selected_file_path
    FILE_PATH = r"C:\Users\Arklok\Documents\Projetos\FACULDADE\anamnese\repository\data\tbl\dados_reais.xlsx"
    
    print(FILE_PATH)
    if FILE_PATH:
        main_dataframe: pd.DataFrame = pd.read_excel(FILE_PATH, engine='openpyxl')
        
        p1: ProcessingGUI = ProcessingGUI(
            transformer=PacienteTransformer(main_dataframe.copy(deep=True)),
            step="Pacientes"
        )
        p1.run()
        ...
    

if __name__ == '__main__':
    main()