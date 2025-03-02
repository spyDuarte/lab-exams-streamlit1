"""
Default data for laboratory exams, including categories and reference ranges.
"""
from typing import Dict, List, Optional

# Checkup categories and exams
CHECKUP_CATEGORIES: Dict[str, List[str]] = {
    'SAÚDE DO HOMEM': [
        'HEMOGRAMA', 'GLICEMIA', 'PERFIL LIPÍDICO', 'FUNÇÃO RENAL',
        'FUNÇÃO TIREOIDEANA', 'PSA'
    ],
    'SAÚDE DA MULHER': [
        'HEMOGRAMA', 'GLICEMIA', 'FUNÇÃO RENAL',
        'PERFIL LIPÍDICO', 'FUNÇÃO TIREOIDEANA', 'HORMÔNIOS FEMININOS'
    ],
    'ROTINA': [
        'HEMOGRAMA', 'GLICEMIA', 'FUNÇÃO RENAL', 'PERFIL LIPÍDICO'
    ]
}

# Reference ranges for lab exams
REFERENCE_RANGES = {
    'HEMOGRAMA': {
        'Hemoglobina': {'min': 13.5, 'max': 17.5, 'unit': 'g/dL'},
        'Hematócrito': {'min': 41.0, 'max': 53.0, 'unit': '%'},
        'Leucócitos': {'min': 4.0, 'max': 10.0, 'unit': 'x 10³/µL'},
        'Plaquetas': {'min': 150.0, 'max': 450.0, 'unit': 'x 10³/µL'},
        'VCM': {'min': 80.0, 'max': 100.0, 'unit': 'fL'},
        'HCM': {'min': 27.0, 'max': 32.0, 'unit': 'pg'},
        'CHCM': {'min': 32.0, 'max': 36.0, 'unit': 'g/dL'},
        'RDW': {'min': 11.5, 'max': 14.5, 'unit': '%'},
        'VPM': {'min': 7.2, 'max': 11.1, 'unit': 'fL'}
    },
    'GLICEMIA': {
        'Glicose': {'min': 70.0, 'max': 99.0, 'unit': 'mg/dL'},
        'Hemoglobina Glicada': {'min': 4.0, 'max': 5.7, 'unit': '%'},
        'Insulina': {'min': 2.6, 'max': 24.9, 'unit': 'µU/mL'}
    },
    'FUNÇÃO RENAL': {
        'Creatinina': {'min': 0.7, 'max': 1.2, 'unit': 'mg/dL'},
        'Ureia': {'min': 15.0, 'max': 45.0, 'unit': 'mg/dL'}
    },
    'PERFIL LIPÍDICO': {
        'Colesterol Total': {'min': 0, 'max': 200.0, 'unit': 'mg/dL'},
        'HDL': {'min': 40.0, 'max': 60.0, 'unit': 'mg/dL'},
        'LDL': {'min': 0, 'max': 130.0, 'unit': 'mg/dL'},
        'Triglicerídeos': {'min': 0, 'max': 150.0, 'unit': 'mg/dL'}
    },
    'FUNÇÃO TIREOIDEANA': {
        'TSH': {'min': 0.4, 'max': 4.0, 'unit': 'mUI/L'},
        'T4 Livre': {'min': 0.8, 'max': 1.8, 'unit': 'ng/dL'},
        'T3': {'min': 80.0, 'max': 200.0, 'unit': 'ng/dL'}
    },
    'PSA': {
        'PSA Total': {'min': 0, 'max': 4.0, 'unit': 'ng/mL'},
        'PSA Livre': {'min': 0, 'max': 1.0, 'unit': 'ng/mL'},
    },
    'HORMÔNIOS FEMININOS': {
        'Estradiol': {'min': 30.0, 'max': 400.0, 'unit': 'pg/mL'},
        'FSH': {'min': 4.0, 'max': 13.0, 'unit': 'mUI/mL'},
        'LH': {'min': 1.0, 'max': 18.0, 'unit': 'mUI/mL'},
        'Progesterona': {'min': 0.3, 'max': 1.5, 'unit': 'ng/mL'}
    }
}

# Default descriptions for profiles
DEFAULT_DESCRIPTIONS = {
    'SAÚDE DO HOMEM': "Checkup voltado à saúde masculina",
    'SAÚDE DA MULHER': "Checkup voltado à saúde feminina",
    'ROTINA': "Checkup de rotina básico"
}