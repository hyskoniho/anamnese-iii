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
        return dataframe.loc[[index]].copy(deep=True)
    
    def add_i_row(self, index: int, dataframe: pd.DataFrame = None) -> None:
        dataframe: pd.DataFrame = dataframe if dataframe is not None else self.dataframe
        self.i_dataframe = pd.concat([self.i_dataframe, self.select_row(dataframe=dataframe, index=index)], ignore_index=False)
        
    def remove_i_row(self, index: int) -> None:
        self.i_dataframe = self.i_dataframe[self.i_dataframe.index != index]
        
    def add_n_row(self, index: int, dataframe: pd.DataFrame = None) -> None:
        dataframe: pd.DataFrame = dataframe if dataframe is not None else self.dataframe
        self.n_dataframe = pd.concat([self.n_dataframe, self.select_row(dataframe=dataframe, index=index)], ignore_index=False)
    
    def remove_n_row(self, index: int) -> None:
        self.n_dataframe = self.n_dataframe[self.n_dataframe.index != index]
        
    def list_inserted_indexes(self) -> list[int]:
        return self.i_dataframe.index.tolist()

class AnamneseTransformer(GeneralTransformer):
    def __init__(self, dataframe: pd.DataFrame, inserted: list[int]) -> None:
        
        #! pd column: sql column
        self.sql_mapping: dict = {
            "Nome": "nome_paciente",
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
            'Faz uso de medicamentos contínuos? ': 'medicamentos_continuos',
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
            'Verduras e legumes [Beterraba]': 'legumes_beterraba', #*
            'Verduras e legumes [Berinjela]': 'legumes_berinjela',
            'Verduras e legumes [Pepino]': 'legumes_pepino',
            'Verduras e legumes [Abobrinha]': 'legumes_abobrinha',
            'Verduras e legumes [Chuchu]': 'legumes_chuchu',
            'Verduras [Acelga]': 'verduras_acelga',
            'Verduras [Agrião]': 'verduras_agriao',
            'Verduras [Alface]': 'verduras_alface',
            'Verduras [Brócolis]': 'verduras_brocolis',
            'Verduras [Chicória]': 'verduras_chicoria',
            'Verduras [Couve Manteiga]': 'verduras_couve_manteiga',
            'Verduras [Couve-flor]': 'verduras_couve_flor',
            'Verduras [Espinafre]': 'verduras_espinafre',
            'Verduras [Rúcula]': 'verduras_rucula',
            'Frutas cítricas [Laranja]': 'frutas_c_laranja',
            'Frutas cítricas [Tangerina/Mexerica/Bergamota]': 'frutas_c_tangerina',
            'Frutas cítricas [Limão]': 'frutas_c_limao',
            'Frutas cítricas [Abacaxi]': 'frutas_c_abacaxi',
            'Frutas cítricas [Acerola]': 'frutas_c_acerola',
            'Frutas cítricas [Morango]': 'frutas_c_morango',
            'Frutas cítricas [Kiwi]': 'frutas_c_kiwi',
            'Frutas cítricas [Maracujá]': 'frutas_c_maracuja',
            'Outras frutas [Banana Nanica/Prata/Ouro/Maçã]': 'demais_frutas_banana',
            'Outras frutas [Goiaba]': 'demais_frutas_goiaba',
            'Outras frutas [Maçã]': 'demais_frutas_maca',
            'Outras frutas [Mamão]': 'demais_frutas_mamao',
            'Outras frutas [Manga]': 'demais_frutas_manga',
            'Outras frutas [Melancia]': 'demais_frutas_melancia',
            'Outras frutas [Melão]': 'demais_frutas_melao',
            'Outras frutas [Pera]': 'demais_frutas_pera',
            'Outras frutas [Pêssego]': 'demais_frutas_pessego',
            'Outras frutas [Uva]': 'demais_frutas_uva',
            'Leguminosas [Feijões em geral (preto, carioca, branco)]': 'leguminosas_feijao',
            'Leguminosas [Lentilha]': 'leguminosas_lentilha',
            'Leguminosas [Ervilha]': 'leguminosas_ervilha',
            'Leguminosas [Soja]': 'leguminosas_soja',
            'Leguminosas [Grão-de-bico]': 'leguminosas_grao_de_bico',
            'Leguminosas [Vagem]': 'leguminosas_vagem',
            'Carnes/ovos/peixes/aves [Carne vermelha]': 'carnes_bovina',
            'Carnes/ovos/peixe [Suína]': 'carnes_suina',
            'Carnes/ovos/peixe [Aves]': 'carnes_aves',
            'Carnes/ovos/peixe [Peixes]': 'carnes_peixe',
            'Carnes/ovos/peixe [Frutos do mar]': 'frutos_do_mar',
            'Carnes/ovos/peixe [Ovo]': 'ovo',
            'Arroz  [Branco Polido]': 'arroz_branco_polido',
            'Arroz  [Integral]': 'arroz_integral',
            'Lácteos [Leite ]': 'lacteos_leite_integral_desnatado_semi',
            'Lácteos [Leite sem lactose]': 'lacteos_leite_sem_lactose',
            'Lácteos [Queijos ]': 'lacteos_queijos',
            'Lácteos [Iogurtes]': 'lacteos_iogurtes',
            'Cereais [Aveia]': 'cereais_aveia',
            'Cereais [Granola in natura]': 'cereais_granola_in_natura',
            'Cereais [Quinoa]': 'cereais_quinoa',
            'Cereais [Linhaça]': 'cereais_linhaca',
            'Cereais [Chia]': 'cereais_chia',
            'Pães [Francês]': 'paes_frances_media_normal',
            'Pães [Forma]': 'paes_forma',
            'Pães [Forma Integral]': 'paes_forma_integral',
            'Pães [Cará]': 'paes_cara',
            'Pastas para passar no pão [Requeijão]': 'pastas_requeijao',
            'Pastas para passar no pão [Margarina]': 'pastas_margarina',
            'Pastas para passar no pão [Manteiga]': 'pastas_manteiga',
            'Pastas para passar no pão [Ricota]': 'pastas_ricota',
            'Pastas para passar no pão [Cottage]': 'pastas_cottage',
            'Pastas para passar no pão [Doce de leite]': 'pastas_doce_de_leite',
            'Pastas para passar no pão [Creme de avelã]': 'pastas_creme_de_avela',
            'Pastas para passar no pão [Geleia]': 'pastas_geleia',
            'Salgados [Mistinho/esfiha]': 'salgados_mistinho_esfiha',
            'Salgados [Coxinha/croquete]': 'salgados_coxinha_croquete',
            'Salgados [Empadas]': 'salgados_empadas',
            'Salgados [Pão de queijo]': 'salgados_pao_de_queijo',
            'Processados/ultraprocessados em geral [Salgadinho de pacote]': 'ultraprocessados_salgadinho_de_pacote',
            'Processados/ultraprocessados em geral [Biscoito Salgado]': 'ultraprocessados_biscoito_salgado',
            'Processados/ultraprocessados em geral [Biscoito doce/bolacha recheada]': 'ultraprocessados_biscoito_doce',
            'Processados/ultraprocessados em geral [Chocolate]': 'ultraprocessados_chocolate',
            'Processados/ultraprocessados em geral [Refrigerante]': 'ultraprocessados_refrigerante',
            'Processados/ultraprocessados em geral [Suco em pó/caixinha]': 'ultraprocessados_suco_em_po_caixinha',
            'Processados/ultraprocessados em geral [Pratos prontos congelados (lasanha)]': 'ultraprocessados_pratos_prontos_congelados',
            'Processados/ultraprocessados em geral [Macarrão instantâneo]': 'ultraprocessados_macarrao_instantaneo',
            'Processados/ultraprocessados em geral [Bolinho (anamaria)]': 'ultraprocessados_bolinho',
            'Processados/ultraprocessados em geral [Fast food]': 'ultraprocessados_fast_food',
            'Embutidos [Salame]': 'embutidos_salame',
            'Embutidos [Presunto (Cozido/Di Parma)]': 'embutidos_presunto',
            'Embutidos [Apresuntado, mortadela]': 'embutidos_apresuntado_mortadela',
            'Embutidos [Linguiça Toscana/calabresa]': 'embutidos_linguica_toscana_calabresa',
            'Embutidos [Salsicha]': 'embutidos_salsicha',
            'Embutidos [Peito de Peru]': 'embutidos_peito_de_peru',
            'Embutidos [Rosbife]': 'embutidos_rosbife',
            'Embutidos [Nuggets]': 'embutidos_nuggets',
            'Embutidos [Hambúrguer tradicional]': 'embutidos_hamburguer_tradicional',
            'Açúcares e doces em geral [Açúcar (cristal, demerara, mascavo)]': 'acucares_acucar',
            'Açúcares e doces em geral [Adoçante]': 'acucares_adocante',
            'Açúcares e doces em geral [Mel/melado]': 'acucares_mel_melado',
            'Açúcares e doces em geral [Produtos confeitaria (sonho, pão doce, bolo)]': 'acucares_produtos_confeitaria',
            'Açúcares e doces em geral [Guloseimas (doces, balas)]': 'acucares_guloseimas',
            'Açúcares e doces em geral [Achocolatados]': 'acucares_achocolatados',
            'Molhos e temperos prontos [Catchup]': 'molhos_ketchup',
            'Molhos e temperos prontos [Mostarda]': 'molhos_mostarda',
            'Molhos e temperos prontos [Shoyu]': 'molhos_shoyu',
            'Molhos e temperos prontos [Tarê]': 'molhos_tare',
            'Molhos e temperos prontos [Maionese]': 'molhos_maionese', #*
            'Quem cozinha sua comida?': 'quem_cozinha',
            'Costuma ter a necessidade de comer quando está estressado(a), ansioso(a) ou triste?': 'necessidade_comer_estressado_ansioso_triste',
            'Costuma realizar as refeições sozinho(a) ou acompanhado(a)?': 'realiza_refeicoes_sozinho_acompanhado',
            'Como se sente ao exagerar em alimentos \"não saudáveis\"? (sintomas físicos e/ou emocionais)': 'excesso_alimentos_nao_saudaveis_sintomas',
            'Tem alguma dificuldade para manter uma rotina alimentar saudável?': 'dificuldade_rotina_alimentar_saudavel',
            'Sente que precisa \"se consolar\" comendo algo após um acontecimento ruim/estressante?': 'necessidade_consolo_alimentar',
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
            r'% gordura corporal ': 'porcentagem_gordura_corporal_somatoria_4_dobras',
            'Peso gordura (kg)': 'peso_gordura',
            'Peso massa magra (kg)': 'peso_massa_magra',
            'Total água (L)': 'total_agua',
            'Resistência (ohms)': 'resistencia',
            'Reactância (ohms)': 'reactancia',
            r'Ângulo de fase (g°)': 'angulo_de_fase',
            'Circunferência da cintura (cm)': 'circunferencia_cintura',
            'Circunferência do quadril (cm)': 'circunferencia_quadril',
            'Circunferência da panturrilha (cm)': 'circunferencia_panturrilha',
            'EMAP direita (mm)': 'emap_direita',
            'EMAP esquerda (mm)': 'emap_esquerda',
            'Força de preensão manual DIREITA (kgf)': 'forca_preencao_manual_direita',
            'Força de preensão manual ESQUERDA (Kgf)': 'forca_preencao_manual_esquerda',
            'Descrever as metas:': 'metas',
        }
        
        self.sql_enum_mapping: list[str] = ["legumes_cenoura",
            "legumes_beterraba",
            "legumes_berinjela",
            "legumes_pepino",
            "legumes_abobrinha",
            "legumes_chuchu",
            "legumes_tomate",
            "verduras_acelga",
            "verduras_agriao",
            "verduras_alface",
            "verduras_brocolis",
            "verduras_chicoria",
            "verduras_couve_manteiga",
            "verduras_couve_flor",
            "verduras_espinafre",
            "verduras_rucula",
            "frutas_c_laranja",
            "frutas_c_tangerina",
            "frutas_c_limao",
            "frutas_c_abacaxi",
            "frutas_c_acerola",
            "frutas_c_morango",
            "frutas_c_kiwi",
            "frutas_c_maracuja",
            "demais_frutas_banana",
            "demais_frutas_goiaba",
            "demais_frutas_maca",
            "demais_frutas_mamao",
            "demais_frutas_manga",
            "demais_frutas_melancia",
            "demais_frutas_melao",
            "demais_frutas_pera",
            "demais_frutas_pessego",
            "demais_frutas_uva",
            "leguminosas_feijao",
            "leguminosas_lentilha",
            "leguminosas_ervilha",
            "leguminosas_soja",
            "leguminosas_grao_de_bico",
            "leguminosas_vagem",
            "carnes_bovina",
            "carnes_suina",
            "carnes_aves",
            "carnes_peixe",
            "frutos_do_mar",
            "ovo",
            "arroz_branco_polido",
            "arroz_integral",
            "lacteos_leite_integral_desnatado_semi",
            "lacteos_leite_sem_lactose",
            "lacteos_queijos",
            "lacteos_iogurtes",
            "cereais_aveia",
            "cereais_granola_in_natura",
            "cereais_quinoa",
            "cereais_linhaca",
            "cereais_chia",
            "paes_frances_media_normal",
            "paes_frances_media_integral",
            "paes_forma",
            "paes_forma_integral",
            "paes_cara",
            "pastas_requeijao",
            "pastas_margarina",
            "pastas_manteiga",
            "pastas_ricota",
            "pastas_cottage",
            "pastas_doce_de_leite",
            "pastas_creme_de_avela",
            "pastas_geleia",
            "salgados_mistinho_esfiha",
            "salgados_coxinha_croquete",
            "salgados_empadas",
            "salgados_pao_de_queijo",
            "ultraprocessados_salgadinho_de_pacote",
            "ultraprocessados_biscoito_salgado",
            "ultraprocessados_biscoito_doce",
            "ultraprocessados_chocolate",
            "ultraprocessados_refrigerante",
            "ultraprocessados_suco_em_po_caixinha",
            "ultraprocessados_pratos_prontos_congelados",
            "ultraprocessados_macarrao_instantaneo",
            "ultraprocessados_bolinho",
            "ultraprocessados_fast_food",
            "embutidos_salame",
            "embutidos_presunto",
            "embutidos_apresuntado_mortadela",
            "embutidos_linguica_toscana_calabresa",
            "embutidos_salsicha",
            "embutidos_peito_de_peru",
            "embutidos_rosbife",
            "embutidos_nuggets",
            "embutidos_hamburguer_tradicional",
            "acucares_acucar",
            "acucares_adocante",
            "acucares_mel_melado",
            "acucares_produtos_confeitaria",
            "acucares_guloseimas",
            "acucares_achocolatados",
            "molhos_ketchup",
            "molhos_mostarda",
            "molhos_shoyu",
            "molhos_tare",
            "molhos_maionese",
        ]
        
        self.basis_dataframe: pd.DataFrame = dataframe[list(self.sql_mapping.keys())]
        self.dataframe: pd.DataFrame = self.basis_dataframe.copy(deep=True)
        
        self.format_enum_columns()
        self.select_valid_anamneses(index_list=inserted)
    
    @staticmethod
    def normalize_text(text: str) -> str:
        if pd.isna(text) or text == "":
            return ""
        return unidecode(str(text).strip().lower())
        
    def format_enum_columns(self) -> None:
        for k, v in self.sql_mapping.items():
            if v in self.sql_enum_mapping:
                self.dataframe[k] = self.dataframe[k].apply(lambda x: self.normalize_text(x) if not pd.isna(x) else "")
    
    def select_valid_anamneses(self, index_list: list[int]) -> pd.DataFrame:
        self.i_dataframe: pd.DataFrame = self.dataframe.loc[index_list].copy(deep=True)
        self.n_dataframe: pd.DataFrame = self.basis_dataframe[~self.basis_dataframe.index.isin(index_list)]
    
class RetornoTransformer(GeneralTransformer):
    def __init__(self, dataframe: pd.DataFrame, ids_pacientes: dict) -> None:
        
        #! pd column: sql column
        self.sql_mapping: dict = {
            
        }
        
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
    
    @staticmethod
    def match_sexo(sexo: str) -> str:
        if pd.isna(sexo) or sexo == '':
            return 'nao_informado'
        
        sexo: str = unidecode(str(sexo).strip().lower())
        
        if sexo in ['masculino', 'm', 'masc']:
            return 'masculino'
        elif sexo in ['feminino', 'f', 'fem']:
            return 'feminino'
        else:
            return ''
    
    def format_values(self) -> None:
        self.dataframe['Nome'] = self.dataframe['Nome'].apply(lambda x: unidecode(x).replace('.', '').strip().title())
        self.dataframe['Data de nascimento'] = self.dataframe['Data de nascimento'].apply(lambda x: self.format_date_nasc(self=self, date=x))
        self.dataframe['Sexo'] = self.dataframe['Sexo'].apply(lambda x: self.match_sexo(sexo=x))
        
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
        