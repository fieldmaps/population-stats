import subprocess
import requests
from multiprocessing import Pool
from processing.worldpop.inputs.utils import YEAR, cwd, logging, adm0_list

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/worldpop'


def run_process():
    results = []
    pool = Pool()
    for row in adm0_list:
        args = [row['id']]
        result = pool.apply_async(get_tif, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


def get_tif(id):
    url = f'https://data.worldpop.org/GIS/Population/Global_2000_{YEAR}/{YEAR}/{id.upper()}/{id}_ppp_{YEAR}.tif'
    file = f'unconstrained/{id}_ppp_{YEAR}.tif'
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(data / file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info(id)


def build_vrt():
    subprocess.run([
        'gdalbuildvrt',
        '-q',
        data / 'unconstrained.vrt',
        *sorted((data / 'unconstrained').rglob('*.tif')),
    ])


def main():
    if not (data / f'ppp_{YEAR}_unconstrained.tif').is_file():
        (data / 'unconstrained').mkdir(parents=True, exist_ok=True)
        run_process()
        build_vrt()
    logger.info('finished')
