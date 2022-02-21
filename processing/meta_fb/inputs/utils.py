import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'
cwd = Path(__file__).parent

data_types = {
    'general': 't',
    'women': 'f',
    'men': 'm',
    'children_under_five': 't_00_04',
    'youth_15_24': 't_15_24',
    'elderly_60_plus': 't_60_plus',
    'women_of_reproductive_age_15_49': 'f_15_49',
}


def get_land_date():
    cwd = Path(__file__).parent
    with open(cwd / '../../../../adm0-generator/data/land/README.txt') as f:
        return f.readlines()[21][25:35]


land_date = get_land_date()
