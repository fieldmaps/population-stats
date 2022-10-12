import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from processing.meta_fb.outputs.utils import logging, cwd, get_attrs

logger = logging.getLogger(__name__)
config = cwd / '../../../config'
data = cwd / '../../../data'
outputs = cwd / '../../../outputs/population/humanitarian/intl/meta-fb'

fields = ['t', 'f', 'm', 't_00_04', 't_15_24', 't_60_plus', 'f_15_49']


def get_ids(l):
    return [f'adm{x}_id' for x in range(l, -1, -1)] + ['iso_3']


def zip_file(name):
    file = outputs / name
    file_zip = outputs / f'{name}.zip'
    file_zip.unlink(missing_ok=True)
    with ZipFile(file_zip, 'w', ZIP_DEFLATED) as z:
        z.write(file, file.name)
    file.unlink(missing_ok=True)


def export_attrs(df):
    for l in range(4, -1, -1):
        df1 = df.groupby(get_ids(l), dropna=False).sum(
            numeric_only=True, min_count=1).reset_index()
        df_attrs = pd.read_excel(get_attrs(l))
        df_attrs['pop_src'] = 'meta-fb'
        df_attrs = df_attrs.merge(df1, on=get_ids(l))
        if l > 0:
            df_attrs['src_date'] = df_attrs['src_date'].dt.date
            df_attrs['src_update'] = df_attrs['src_update'].dt.date
        df_attrs['wld_date'] = df_attrs['wld_date'].dt.date
        df_attrs['wld_update'] = df_attrs['wld_update'].dt.date
        df_attrs.to_excel(outputs / f'adm{l}_population.xlsx', index=False)
        df_attrs.to_csv(outputs / f'adm{l}_population.csv', index=False)
        zip_file(f'adm{l}_population.csv')
        if l > 0:
            df_attrs['src_date'] = pd.to_datetime(df_attrs['src_date'])
            df_attrs['src_date'] = df_attrs['src_date'].dt.strftime('%Y-%m-%d')
            df_attrs['src_update'] = pd.to_datetime(df_attrs['src_update'])
            df_attrs['src_update'] = df_attrs['src_update'].dt.strftime(
                '%Y-%m-%d')
        df_attrs['wld_date'] = pd.to_datetime(df_attrs['wld_date'])
        df_attrs['wld_date'] = df_attrs['wld_date'].dt.strftime('%Y-%m-%d')
        df_attrs['wld_update'] = pd.to_datetime(df_attrs['wld_update'])
        df_attrs['wld_update'] = df_attrs['wld_update'].dt.strftime('%Y-%m-%d')
        df_attrs.to_json(outputs / f'adm{l}_population.json', orient='records')
        zip_file(f'adm{l}_population.json')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(data / 'meta_fb.xlsx')
    df2 = pd.read_csv(config / 'meta_fb.csv')
    df = df.merge(df2, on='iso_3')
    df = df[df['valid'] == 1]
    df = df.drop(columns=['count', 'valid'])
    for field in fields:
        df[field] = df[field].fillna(0).astype(int)
    export_attrs(df)
    logger.info('finished')
