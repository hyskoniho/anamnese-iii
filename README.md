# Projeto de Migração de Dados - Clínica Anamnese

## Descrição Geral

Este projeto acadêmico foi desenvolvido para a Clínica Anamnese da Universidade Católica de Santos, sob orientação do Product Owner Prof. Cezar, coordenador do curso de Nutrição. O objetivo do sistema é facilitar a migração de dados provenientes de relatórios do Google Forms (em formato Excel) para o banco de dados definitivo do sistema da clínica.

O sistema realiza a leitura, processamento, validação e transformação dos dados dos pacientes e anamneses, gerando automaticamente comandos SQL de inserção (INSERT) compatíveis com o banco de dados da clínica. Dessa forma, garante-se a integridade, padronização e agilidade no processo de migração de informações.

## Funcionalidades

- Interface gráfica intuitiva para seleção e processamento dos arquivos Excel.
- Visualização e ajuste dos dados antes da migração, com possibilidade de manipulação de linhas.
- Geração automática de comandos SQL para inserção dos dados no banco definitivo.
- Suporte a múltiplos tipos de banco de dados (SQLite, MySQL, PostgreSQL).
- Validação de credenciais de acesso para maior segurança.
- Logs detalhados e mensagens de erro amigáveis.

## Público-alvo

- Equipe de TI da Clínica Anamnese
- Professores e alunos do curso de Nutrição
- Administradores do sistema da clínica

## Requisitos

- Windows 10 ou superior
- Python 3.10+
- Ambiente virtual (.venv) com dependências instaladas (ver `requirements.txt`)
- Pacotes adicionais para bancos MySQL/PostgreSQL, se necessário:
  - MySQL: `pip install mysql-connector-python`
  - PostgreSQL: `pip install psycopg2-binary`

## Instalação e Execução

1. **Clone o repositório e acesse a pasta do projeto:**

```powershell
cd "caminho/para/a/pasta/anamnese/repository"
```

2. **Crie e ative o ambiente virtual:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Instale as dependências:**

```powershell
pip install -r requirements.txt
```

4. **Execute o sistema:**

Você pode rodar o sistema com duplo clique no arquivo `run_app.bat` ou pelo terminal:

```powershell
./run_app.bat
```

## Como Utilizar

1. **Login:**
   - Insira suas credenciais institucionais para acessar o sistema.

2. **Seleção do Arquivo:**
   - Escolha o arquivo Excel exportado do Google Forms contendo os dados dos pacientes/anamneses.

3. **Processamento:**
   - Visualize, ajuste e confirme os dados nas telas de processamento.
   - O sistema permite mover registros entre tabelas (inclusos/não-inclusos) antes da geração dos comandos SQL.

4. **Geração dos Comandos SQL:**
   - Ao finalizar, o sistema gera dois arquivos: `insert_pacientes_queries.sql` e `insert_anamneses_queries.sql`.
   - Estes arquivos contêm os comandos prontos para inserção no banco de dados definitivo da clínica.

5. **Execução dos Comandos:**
   - Os comandos podem ser executados diretamente no banco de dados pelo administrador do sistema.

## Estrutura do Projeto

- `src/` - Código-fonte principal
  - `GUI/` - Interfaces gráficas (Home e Processamento)
  - `Transformer/` - Lógica de transformação e validação dos dados
  - `Database/` - Conectores e operações com banco de dados
  - `User/` - Autenticação e controle de usuários
  - `__main__.py` - Ponto de entrada do sistema
- `data/` - Arquivos de apoio, exemplos e scripts SQL
- `requirements.txt` - Dependências do projeto
- `run_app.bat` - Script para rodar o sistema no Windows

## Observações Importantes

- O sistema foi desenvolvido para fins acadêmicos e pode ser adaptado conforme as necessidades da clínica.
- O Product Owner deste projeto é o Prof. Cezar, coordenador do curso de Nutrição.
- Em caso de dúvidas, sugestões ou problemas, entre em contato com a equipe de desenvolvimento ou o coordenador.

---

Universidade Católica de Santos - Clínica Anamnese
Projeto Acadêmico de Migração de Dados
