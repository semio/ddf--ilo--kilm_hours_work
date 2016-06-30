# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file

# configuration of file path
source = '../source/kilm07.xlsx'
out_dir = '../../'


def extract_entities_country(data):
    country = data[['Country (code)', 'Country']].drop_duplicates().copy()
    country.columns = ['country', 'name']
    country['country'] = country['country'].map(to_concept_id)
    return country


def extract_concepts(data):
    discs = ['Name', 'Year', 'Country']
    conc = ['Annual number of hours actually worked per person']

    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['name'] = [*discs, *conc]
    cdf['concept'] = cdf['name'].map(to_concept_id)

    cdf.loc[3, 'concept_type'] = 'measure'
    cdf.loc[0, 'concept_type'] = 'string'
    cdf.loc[1, 'concept_type'] = 'time'
    cdf.loc[2, 'concept_type'] = 'entity_domain'

    return cdf


def extract_datapoints(data):
    conc = 'Annual number of hours actually worked per person'

    dps = data[['Country (code)','Year', conc]].copy()
    dps.columns = ['country', 'year', to_concept_id(conc)]
    dps['country'] = dps['country'].map(to_concept_id)

    return to_concept_id(conc), dps.dropna()


if __name__ == '__main__':
    print('reading source files...')
    data = pd.read_excel(source, skiprows=2, sheetname='KILM 07b')

    print('creating concept files...')
    cdf = extract_concepts(data)
    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf.to_csv(path, index=False)

    print('creating entities files...')
    country = extract_entities_country(data)
    path = os.path.join(out_dir, 'ddf--entities--country.csv')
    country.to_csv(path, index=False)

    print('creating datapoints files...')
    k, datapoints = extract_datapoints(data)
    path = os.path.join(out_dir, 'ddf--datapoints--{}--by--country--year.csv'.format(k))
    datapoints.to_csv(path, index=False)

    print('creating index file...')
    create_index_file(out_dir)

    print('Done.')
