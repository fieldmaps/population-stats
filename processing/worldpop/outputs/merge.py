import pandas as pd
from processing.worldpop.outputs.utils import logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../../data'
outputs = cwd / '../../../outputs'


def get_ids(l):
    return [f'adm{x}_id' for x in range(l, -1, -1)] + ['iso_3', 'wld_update']


def export_factor(df):
    df1 = pd.read_excel(data / 'un_wpp.xlsx')
    dfx = df.groupby(get_ids(-1), dropna=False).sum(min_count=1).reset_index()
    dfx = dfx.merge(df1, on='iso_3', how='left')
    dfx['factor'] = dfx['t_y'] / dfx['t_x']
    dfx['factor'] = dfx['factor'].fillna(1)
    dfx = dfx[get_ids(-1) + ['factor']]
    dfx.to_excel(outputs / 'worldpop_factor.xlsx', index=False)
    dfx.to_csv(outputs / 'worldpop_factor.csv', index=False)
    dfx.to_json(outputs / 'worldpop_factor.json', orient='records')
    return dfx


def main():
    df = pd.read_excel(data / 'worldpop.xlsx')
    dfx = export_factor(df)
    df = df.merge(dfx, on=get_ids(-1))
    df['t'] = df['t'] * df['factor']
    df['t'] = df['t'].round(0).fillna(0)
    df = df.drop(['count', 'factor'], axis=1)
    with pd.ExcelWriter(outputs / 'worldpop.xlsx') as writer:
        for l in range(4, -2, -1):
            df = df.groupby(get_ids(l), dropna=False).sum(
                min_count=1).reset_index()
            sheet_name = f'adm{l}_id' if l >= 0 else 'iso_3'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    logger.info('finished')
