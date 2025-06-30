import enum

class TipoNutriEcoScoreDB(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

class TipoNovaScoreDB(enum.Enum):
    UM = '1'
    DOIS = '2'
    TRES = '3'
    QUATRO = '4'

class TipoTagDB(enum.Enum):
    allergen = 'allergen'
    additive = 'additive'