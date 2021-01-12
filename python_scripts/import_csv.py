import numpy as np
import pandas as pd
import sys
from scipy import stats

############
# Useful projections
############
PROJ_FULL = ['x86instructions', 'paths', 'transient_paths_pht',
             'transient_paths_stl', 'Explor total', 'Insec total',
             'Total total', 'Explor time', 'Insec time', 'wall time',
             'violations', 'timeouts']
PROJ_MINIMAL = ['paths', 'Total total', 'wall time', 'secure',
                'insecure', 'unknown', 'violations', 'timeouts']
# PROJ_FULL_STL = ['x86instructions', 'paths',
#                  'transient_paths_stl', 'Explor total', 'Insec total',
#                  'Total total', 'Explor time', 'Insec time',
#                  'wall time', 'violations', 'timeouts', 'secure',
#                  'insecure', 'unknown']
# PROJ_FULL_STL = ['addresses', 'x86instructions', 'paths', 'Total total',
#                  'wall time', 'violations', 'timeouts',
#                  'secure', 'insecure']
# PROJ_FULL_PHT = ['addresses', 'x86instructions', 'paths', 'Total total',
#                  'wall time', 'violations', 'timeouts',
#                  'secure', 'insecure']
PROJ_FULL_STL = ['addresses', 'paths', 'wall time',
                 'violations', 'timeouts', 'secure', 'insecure']
PROJ_FULL_PHT = ['addresses', 'paths', 'wall time',
                 'violations', 'timeouts', 'secure', 'insecure']
# factor_attributes = ['paths', 'Total total', 'wall time']


def embellish_df(df, attributes):
    df = df.round({'x86instructions': 0, 'Total total': 0,
                   'Explor total': 0, 'Insec total': 0, 'Explor time': 3,
                   'Insec time': 3, 'wall time': 3, 'paths': 0,
                   'transient_paths_pht': 0, 'transient_paths_stl': 0,
                   'secure': 0, 'insecure': 0, 'unknown': 0,
                   'violations': 0, 'timeouts': 0})
    cols_to_int = ['x86instructions', 'Total total', 'Explor total',
                   'Insec total', 'paths', 'transient_paths_pht',
                   'transient_paths_stl', 'timeouts',
                   'violations', 'secure', 'insecure', 'unknown']
    df[cols_to_int] = df[cols_to_int].astype('Int64')
    return df[attributes]


def pp_df(df, attributes):
    print(embellish_df(df, attributes).to_string())


def pp_df_tolatex(df, attributes):
    print(embellish_df(df, attributes).to_latex())


############
# Store type category
############
def store_type(store, mem_type, canonical, untaint, fp, bopt):
    # Sse
    if (store == 'sse' and mem_type == 'std' and bopt != 1):
        return "0-sse"
    elif (store == 'sse' and mem_type == 'std' and bopt == 1):
        return "0-sse-bopt"
    elif (store == 'sse' and mem_type == 'row-map' and bopt != 1):
        return "1-bin-sse"
    # Self-comp
    elif (store == 'self-comp' and mem_type == "std" and canonical == 0 and
          untaint == 0 and fp == 1 and bopt != 1):
        return "2-sc"
    elif (store == 'self-comp' and mem_type == "std" and canonical == 0 and
          fp == 0 and bopt != 1):
        return "2-sc-no-check"
    # RelSE
    elif (store == 'relational' and mem_type == "std" and canonical == 0 and
          untaint == 0 and fp == 1 and bopt != 1):
        return "3-relse"
    elif (store == 'relational' and mem_type == "std" and canonical == 0 and
          untaint == 0 and fp == 1 and bopt == 1):
        return "3-relse-bopt"
    elif (store == 'relational' and mem_type == "std" and canonical == 0 and
          untaint == 1 and fp == 1 and bopt != 1):
        return "3-relse-unt"
    elif (store == 'relational' and mem_type == "std" and canonical == 0 and
          untaint == 1 and fp == 2 and bopt != 1):
        return "3-relse-unt-fp"
    elif (store == 'relational' and mem_type == "std" and canonical == 0 and
          fp == 0 and bopt != 1):
        return "3-relse-no-check"
    # BinRelSE
    elif (store == 'relational' and mem_type == "row-map" and
          canonical == 1 and untaint == 0 and fp == 1 and bopt != 1):
        return "4-bin-relse"
    elif (store == 'relational' and mem_type == "row-map" and
          canonical == 1 and untaint == 1 and fp == 1 and bopt != 1):
        return "4-bin-relse-unt"
    elif (store == 'relational' and mem_type == "row-map" and
          canonical == 1 and untaint == 1 and fp == 2 and bopt != 1):
        return "4-bin-relse-unt-fp"
    elif (store == 'relational' and mem_type == "row-map" and
          canonical == 1 and fp == 0 and bopt != 1):
        return "4-bin-relse-no-check"
    else:
        return "undef"


def add_store_type(df):
    if not ('bopt' in df.columns):
        df['bopt'] = 0
    df['store_type'] = np.vectorize(store_type)(df['store'],
                                                df['mem_type'],
                                                df['canonical'],
                                                df['untainting'],
                                                df['fp'],
                                                df['bopt'])
    return df


############
# Compute status
############
def add_status(df):
    df['timeouts'] = np.vectorize(lambda x, y, z:
                                  (0 if x == 0 and y == 0 and z == 0
                                   else 1))(df['timeout_reached'],
                                            df['interrupted'],
                                            df['out_of_memory'])
    df['secure'] = df['exit_code'].apply(lambda x: 1 if x == "Secure" else 0)
    df['insecure'] = df['exit_code'].apply(lambda x: 1 if x ==
                                           "Insecure" else 0)
    df['unknown'] = df['exit_code'].apply(lambda x: 1 if x == "Unknown" else 0)
    return df


pht_status_categories = ["NoPHT", "ExplicitSmarter", "Haunted"]
pht_status_categories_no_ct = ["ExplicitSmarter", "Haunted"]
pht_dyn_categories = ["Static", "Hybrid_20", "Hybrid_0", "Full"]
stl_status_categories = ["NoSTL", "ExplicitSTL", "HauntedIteSTL"]


############
# Restrict dataset to category
############
def no_pht(df):
    return df[df.pht_status.eq("NoPHT")]


def no_stl(df):
    return df[df.stl_status.eq("NoSTL")]


def no_dyn(df):
    return df[df.pht_dynamic.eq("Static")]


def dyn_proj(df, dyn):
    return df[df.pht_dynamic.eq(dyn) | df.pht_status.eq("NoPHT")]


def no_ct(df):
    df['pht_status'] = pd.Categorical(df['pht_status'],
                                      pht_status_categories_no_ct)
    return df[~(df['pht_status'].eq("NoPHT") & df['stl_status'].eq("NoSTL"))]


def assert_unique_value(df, column_name):
    result_column = df[column_name] == df[column_name].iloc[0]
    if (not result_column.all()):
        raise ValueError('Value in column ' + column_name + ' sould be \
        unique.')


def make_categories(df):
    df['pht_status'] = pd.Categorical(df['pht_status'], pht_status_categories)
    df['pht_dynamic'] = pd.Categorical(df['pht_dynamic'], pht_dyn_categories)
    df['stl_status'] = pd.Categorical(df['stl_status'], stl_status_categories)
    return df


############
# DFs from files
############
def get_df_from_files(path, file_list):
    df_list = []
    for file_name in file_list:
        target = path + file_name + '.csv'
        df = pd.read_csv(target)
        # Compute new store_type column
        df = add_store_type(df)
        # Check if all store elements are equal
        assert_unique_value(df, "store_type")
        # Compute status
        df = add_status(df)
        # Make categories
        df = make_categories(df)
        # Add to df_list
        df_list.append(df)

    return pd.concat(df_list)


############
# Useful aggregates
############
def aggregate_spectre_pht(df, dyn="Static"):
    # Removing STL and Dynamic
    df = no_stl(df)
    df = dyn_proj(df, dyn)
    # Check if STL status is none
    assert_unique_value(df, 'stl_status')
    # Compute mean per label and store_type
    return df.groupby(['label', 'pht_status', 'max_spec_depth']).mean()
    # TOTO Add total number of programs


def aggregate_spectre_pht_dyn(df):
    # Removing STL and CT
    df = no_stl(df)
    df = no_ct(df)
    # Check if STL status is none
    assert_unique_value(df, 'stl_status')
    assert_unique_value(df, 'max_spec_depth')
    # Compute mean per label and store_type
    return df.groupby(['label', 'pht_status', 'pht_dynamic']).mean()
    # TOTO Add total number of programs


def aggregate_spectre_stl(df):
    # Removing PHT
    df = no_pht(df)
    # Check if STL status is none
    assert_unique_value(df, 'pht_status')
    assert_unique_value(df, 'max_spec_depth')
    # Compute mean per label and store_type
    return df.groupby(['label', 'stl_status']).mean()
    # TOTO Add total number of programs


def total_sum_spectre_stl(df):
    df.reset_index()
    return df.groupby(['stl_status']).sum()
    # TOTO Add total number of programs


def total_sum_spectre_pht(df):
    df.reset_index()
    return df.groupby(['pht_status']).sum()


def total_sum_spectre_pht_dyn(df):
    df.reset_index()
    return df.groupby(['pht_status', 'pht_dynamic']).sum()

def compute_time_overhead(df):
    explicit = df.loc[df.index.isin(["ExplicitSmarter"], level="pht_status")].reset_index()
    haunted = df.loc[df.index.isin(["Haunted"], level="pht_status")].reset_index()
    explicit_total = explicit.sum()
    haunted_total = haunted.sum()
    
    overhead = pd.DataFrame()
    overhead['label'] = explicit['label'] 
    overhead['speedup (factor)'] = explicit['wall time'] / haunted['wall time']
    overhead_total = explicit_total['wall time'] / haunted_total['wall time']
    
    print("(Speedup compared to explicit)")
    print(overhead.to_string())

    print("\n\nMin: " + str(overhead['speedup (factor)'].min()))
    print("Max: " + str(overhead['speedup (factor)'].max()))
    print("GeoMean: " + str(stats.gmean(overhead['speedup (factor)'])))
    print("Mean: " + str(overhead['speedup (factor)'].mean()))
    print("Median: " + str(overhead['speedup (factor)'].median()))
    print("Total: " + str(overhead_total))
    

