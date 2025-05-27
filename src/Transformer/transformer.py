import pandas as pd
from unidecode import unidecode
from .utility import Utils

class GeneralTransformer:
    def __init__(self, i_dataframe: pd.DataFrame, n_dataframe: pd.DataFrame, dataframe: pd.DataFrame) -> None:
        self.i_dataframe: pd.DataFrame = i_dataframe
        self.n_dataframe: pd.DataFrame = n_dataframe
        self.dataframe: pd.DataFrame = dataframe
    
    @staticmethod
    def select_row(dataframe: pd.DataFrame, index: int) -> pd.DataFrame:
        return dataframe.iloc[[index]].copy(deep=True)
    
    def add_i_row(self, index: int, dataframe: pd.DataFrame = None) -> None:
        dataframe: pd.DataFrame = dataframe if dataframe is not None else self.dataframe
        self.i_dataframe = pd.concat([self.i_dataframe, self.select_row(dataframe=dataframe, index=index)], ignore_index=True)
        
    def remove_i_row(self, index: int) -> None:
        self.i_dataframe = self.i_dataframe[self.i_dataframe.index != index]
        
    def add_n_row(self, index: int, dataframe: pd.DataFrame) -> None:
        dataframe: pd.DataFrame = dataframe if dataframe is not None else self.dataframe
        self.n_dataframe = pd.concat([self.n_dataframe, self.select_row(dataframe=dataframe, index=index)], ignore_index=True)
    
    def remove_n_row(self, index: int) -> None:
        self.n_dataframe = self.n_dataframe[self.n_dataframe.index != index]

class AnamneseTransformer(GeneralTransformer):
    def __init__(self, dataframe: pd.DataFrame) -> None:
        
        #! pd column: sql column
        self.sql_mapping: dict = {
            'Escolaridade': 'escolaridade',
            'Período em que trabalha/estuda': 'periodo_estudo',
            'Há possibilidade de realizar lanches no local de estudo?': 'lanche_estudo',
            'Período em que trabalha': 'periodo_trabalho',
            'Há a possibilidade de realizar lanches no local de trabalho?': 'lanche_trabalho',
            'Profissão': 'profissao',
            'Renda familiar': 'renda_familiar',
            'Quantas pessoas moram no domicílio (contando com você)': 'num_pessoas_domicilio',
            'Motivo pela procura do ambulatório': 'motivo',
            'Apresenta alguma doença?': 'apresenta_doenca',
            'Apresenta antecedentes familiares de alguma doença crônica? (DM, HAS, dislipidemia...)': 'antecedentes_familiares',
            'Faz uso de medicamentos contínuos?': 'medicamentos_continuos',
            'Faz uso de suplementos ou complementos alimentares?': 'suplementos_complementos',
            'Frequência de evacuação': 'frequencia_evacuacao',
            'Consistência da evacuação:': 'consistencia_evacuacao',
            'Pratica atividade física regularmente?': 'pratica_atv_fisica',
            'Se sim: qual atividade, frequência semanal e duração? (intensidade,peso)': 'atv_fisica',
            'Café da manhã:': 'cafe_da_manha',
            'Lanche da manhã (se houver):': 'lanche_da_manha',
            'Almoço:': 'almoco',
            'Lanche da tarde:': 'lanche_da_tarde',
            'Jantar:': 'jantar',
            'Ceia (se houver):': 'ceia',
            #? ...
            'Quem cozinha sua comida?': 'quem_cozinha',
            'Costuma ter a necessidade de comer quando está estressado(a), ansioso(a) ou triste?': 'necessidade_comer_estressado_ansioso_triste',
            'Costuma realizar as refeições sozinho(a) ou acompanhado(a)?': 'realiza_refeicoes_sozinho_acompanhado',
            'Como se sente ao exagerar em alimentos \"não saudáveis\"? (sintomas físicos e/ou emocionais)': 'excesso_alimentos_nao_saudaveis_sintomas',
            'Tem alguma dificuldade para manter uma rotina alimentar saudável?': 'dificuldade_rotina_alimentar_saudavel',
            'Sente que \"precisa\" comendo algo após um acontecimento ruim/estressante?': 'necessidade_consolo_alimentar',
            'É difícil para você parar de comer o que restou no prato, mesmo estando saciado?': 'dificuldade_parar_de_comer',
            'Qual a frequência da sua fome fisiológica?': 'frequencia_fome_fisiologica',
            'Qual a frequência da sua necessidade emocional de comer alguma coisa?': 'frequencia_necessidade_emocional_comer',
            'O que você gostaria que não fosse modificado no seu plano alimentar?': 'nao_modificar_plano_alimentar',
            'Você tem alguma aversão alimentar? (alimentos que não come de jeito nenhum)': 'aversao_alimentar',
            'Tolera igualmente os alimentos fonte de proteína animal? (carne bovina, frango, suínos, peixe, frutos do mar...)': 'tolera_alimentos_proteina_animal',
            'Apresenta alergias e /ou intolerâncias alimentares? Se sim, quais?': 'alergia_intolerancias_alimentares',
            'Dê uma nota à sua saciedade após as refeições': 'nota_saciedade_pos_refeicoes',
            'Como você classifica a sua satisfação pessoal (qualidade e quantidade da refeição) após realizar as refeições': 'nota_humor_pos_refeicoes',
            'Peso atual (kg)': 'peso_atual',
            'Estatura (m)': 'estatura',
            'IMC (kg/m²)': 'imc',
            'CB (cm)': 'cb',
            'DCT (mm)': 'dct',
            'DCB (mm)': 'dcb',
            'DCSE (mm)': 'dcse',
            'DCSI (mm)': 'dcsi',
            'Somatória 4 dobras': 'somatoria_4_dobras',
            r'% gordura corporal': 'porcentagem_gordura_corporal_somatoria_4_dobras',
            'Peso gordura (kg)': 'peso_gordura',
            'Peso massa magra (kg)': 'peso_massa_magra',
            'Total água (L)': 'total_agua',
            'Resistência (ohms)': 'resistencia',
            'Reactância (ohms)': 'reactancia',
            'Ângulo de fase (gº)': 'angulo_de_fase',
            'Circunferência da cintura (cm)': 'circunferencia_cintura',
            'Circunferência do quadril (cm)': 'circunferencia_quadril',
            'Circunferência da panturrilha (cm)': 'circunferencia_panturrilha',
            'EMAP direita (mm)': 'emap_direita',
            'EMAP esquerda (mm)': 'emap_esquerda',
            'Força de preensão manual DIREITA (kgf)': 'forca_preencao_manual_direita',
            'Força de preensão manual ESQUERDA (kgf)': 'forca_preencao_manual_esquerda',
            'Descrever as metas:': 'metas'
        }
    
class RetornoTransformer(GeneralTransformer):
    def __init__(self, dataframe: pd.DataFrame, ids_pacientes: dict) -> None:
        
        #! pd column: sql column
        self.sql_mapping: dict = {
            
        }
        
        
    
    
# CREATE TABLE retorno (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     paciente_id INT NOT NULL,
#     paciente_nome VARCHAR(60) NOT NULL,
#     usuario_id INT NOT NULL,
#     usuario_nome VARCHAR(60) NOT NULL,
#     tipo_formulario VARCHAR(10) DEFAULT 'Retorno' NOT NULL,
#     retorno INT NOT NULL,
#     metas_ultima_consulta TEXT NULL,
#     comentarios_observacao TEXT NULL,
#     metas_foram_cumpridas ENUM('sim', 'nao', 'mais_ou_menos') NULL,
#     desempenho_cumprimento_metas TINYINT NULL,
#     motivo_assinalado_cumprimento_metas TEXT NULL,
#     como_sentiu_mudanca_habitos TEXT NULL,
#     adaptacao_mudanca_habitos TEXT NULL,
#     motivos_dificuldade_adaptacao TEXT NULL,
#     sente_precisa_melhorar_alimentacao TEXT NULL,
#     habito_intestinal TEXT NULL,
#     atv_fisica ENUM('manteve_o_que_ja_fazia', 'aumentei_a_frequencia_intensidade', 'ainda_nao_consegui_praticar', 'nao_iniciei_e_nao_pretendo_iniciar') NULL,
#     metas_proximo_retorno TEXT NULL,
#     peso_atual FLOAT NULL,
#     imc FLOAT NULL,
#     circunferencia_abdominal FLOAT NULL,
#     valores_bioimpedancia TEXT NULL,
#     observacoes_bioimpedancia TEXT NULL,
#     criado_em DATETIME DEFAULT (CURRENT_TIMESTAMP) NULL,
#     FOREIGN KEY (paciente_id) REFERENCES paciente(id),
#     FOREIGN KEY (usuario_id) REFERENCES usuario(id)
# );
    
class PacienteTransformer(GeneralTransformer):
    def __init__(self, dataframe: pd.DataFrame) -> None:
        #! pd column: sql column
        self.sql_mapping: dict = {
            'Nome': 'nome',
            'Sexo': 'sexo',
            'Data de nascimento': 'data_nascimento'
        }
        
        self.basis_dataframe: pd.DataFrame = dataframe[list(self.sql_mapping.keys()) + ['Carimbo de data/hora']]
        self.dataframe: pd.DataFrame = self.basis_dataframe.copy(deep=True)
        
        self.format_values()
        self.filter_rows()
        
        super().__init__(i_dataframe=self.i_dataframe, n_dataframe=self.n_dataframe, dataframe=self.dataframe)
    
    @staticmethod
    def format_date_nasc(self, date: str) -> str:
        if pd.isna(date):
            return ''
        
        try:
            date: str = str(date).replace('-', '/').replace('.', '').replace(' ', '').replace('?', '/').replace('//', '/').strip()
            
            if len(date) == 8 and '/' not in date: date: str = f'{date[:2]}/{date[2:4]}/{date[4:]}'
                
            if len(date) == 8 and '/' in date: date: str = f'{date[:6]}/{"19" if int(date[6:]) > 25 else "20"}{date[6:]}'    
            
            elif len(date) == 6: date: str = f'{date[:2]}/{date[2:4]}/{"19" if int(date[4:]) > 25 else "20"}{date[4:]}'
            
            date: str = str(date).replace('//', '/')
            
        except Exception as e:
            print(e)
        
        return date
    
    def format_values(self) -> None:
        self.dataframe['Nome'] = self.dataframe['Nome'].apply(lambda x: unidecode(x).replace('.', '').strip().title())
        self.dataframe['Data de nascimento'] = self.dataframe['Data de nascimento'].apply(lambda x: self.format_date_nasc(self=self, date=x))
        
        self.dataframe: pd.DataFrame = self.dataframe[
            (~self.dataframe['Nome'].str.contains('Teste')) &
            (~self.dataframe['Nome'].str.contains('Alun')) &
            (self.dataframe['Nome'].str.split(' ').str.len() >= 2) &
            (self.dataframe['Data de nascimento'].str.contains('^([0-2][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)[0-9]{2}$'))
        ]
    
    def filter_rows(self) -> None:
        self.i_dataframe: pd.DataFrame = self.dataframe.dropna(subset=['Sexo', 'Nome', 'Data de nascimento'])\
            .sort_values(by=['Nome', 'Carimbo de data/hora'], ascending=[True, True])\
                .drop_duplicates(subset=['Nome'], keep='first')\
                    .drop(columns=['Carimbo de data/hora'])
        
        self.n_dataframe: pd.DataFrame = self.basis_dataframe[self.basis_dataframe.index.isin(self.i_dataframe.index) == False][['Nome', 'Sexo', 'Data de nascimento']]
        