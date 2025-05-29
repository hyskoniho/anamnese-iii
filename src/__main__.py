# Built-in imports
import logging, os, sys, traceback, json, time, warnings
from typing import List, Optional, Tuple, Any, Dict
from getpass import getpass

# Third-party imports
import pandas as pd
from tkinter import messagebox

# Local imports
from Transformer import *
from Database import Database
from GUI import HomeGUI, ProcessingGUI
from User import User

logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore", category=UserWarning)

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
    try:
        authenticate_user()
        print("\nAutenticação bem-sucedida. Iniciando o sistema...")
        
        h: HomeGUI = HomeGUI()
        h.run()
        FILE_PATH = h.selected_file_path
        # FILE_PATH = r"C:\Users\Arklok\Documents\Projetos\FACULDADE\anamnese\repository\data\tbl\dados_reais.xlsx"
        
        print(f"\nArquivo selecionado: {FILE_PATH}")
        
        if FILE_PATH:
            main_dataframe: pd.DataFrame = pd.read_excel(FILE_PATH, engine='openpyxl')
            
            t1: PacienteTransformer = PacienteTransformer(main_dataframe.copy(deep=True))
            g1: ProcessingGUI = ProcessingGUI(
                transformer=t1,
                step="Pacientes"
            )
            g1.run()
            
            insert_pacientes_queries: List[str] = Utils.generate_sql_insert(
                mapping = t1.sql_mapping, 
                dataframe = t1.i_dataframe, 
                table_name = "paciente", 
                batch_size = 200
            )
            
            # ! Query 1
            insert_pacientes_queries
            
            t2: AnamneseTransformer = AnamneseTransformer(main_dataframe.copy(deep=True), t1.list_inserted_indexes())
            g2: ProcessingGUI = ProcessingGUI(
                transformer=t2,
                step="Anamneses"
            )
            g2.run()
            
            insert_anamneses_queries: List[str] = Utils.generate_sql_insert(
                mapping = t2.sql_mapping, 
                dataframe = t2.i_dataframe, 
                table_name = "anamnese", 
                batch_size = 200
            )
            
            # ! Query 2
            insert_anamneses_queries
            messagebox.showinfo(
                title="Processamento Concluído",
                message="O processamento dos dados foi concluído com sucesso. As consultas SQL foram geradas e estão prontas para serem executadas."
            )
            
            with open("insert_pacientes_queries.sql", "w", encoding="utf-8") as f:
                f.write("\n".join(insert_pacientes_queries))
            
            with open("insert_anamneses_queries.sql", "w", encoding="utf-8") as f:
                f.write("\n".join(insert_anamneses_queries))

        else:
            logging.error("Nenhum arquivo selecionado. Encerrando o programa.")
            messagebox.showerror(
                title="Erro",
                message="Nenhum arquivo foi selecionado. Por favor, selecione um arquivo válido."
            )
            sys.exit(1)

    except KeyboardInterrupt:
        logging.info("Execução interrompida pelo usuário.")
        messagebox.showinfo(
            title="Interrupção",
            message="O programa foi interrompido pelo usuário."
        )
        sys.exit(0)
    
    except Exception as e:
        logging.error("Ocorreu um erro durante a execução do programa.")
        logging.error(''.join(traceback.format_exception(*sys.exc_info())))
        messagebox.showerror(
            title="Erro",
            message="Ocorreu um erro inesperado. Por favor, verifique os logs para mais detalhes."
        )
        sys.exit(1)
    

if __name__ == '__main__':
    main()