#!/usr/bin/python
import sys
sys.path.insert(1, './python_scripts/')
import import_csv as I
import pandas as pd

pp = I.pp_df


def get_stat_dir(name):
    return "src/" + name + "/stats/"


def get_df_aggregate_pht(directory, files):
    # Get the dataframe
    stat_dir = get_stat_dir(directory)
    df = I.get_df_from_files(stat_dir, files)
    pht = I.aggregate_spectre_pht(df, dyn="Full")
    pht = I.total_sum_spectre_pht(pht)
    pht['label'] = directory
    return pht
    

def get_df_aggregate_stl(directory, files):
    # Get the dataframe
    stat_dir = get_stat_dir(directory)
    df = I.get_df_from_files(stat_dir, files)
    stl = I.aggregate_spectre_stl(df)
    # pp(stl, I.PROJ_FULL_STL)
    stl = I.total_sum_spectre_stl(stl)
    stl['label'] = directory
    return stl


def pp_pht(df):
    pp(df, I.PROJ_FULL_PHT)


def pp_stl(df):
    pp(df, I.PROJ_FULL_STL)


def pp_total_pht(df_list):
    df = pd.concat(df_list, sort=False)
    df = I.total_sum_spectre_pht(df)
    pp_pht(df)


def pp_total_stl(df_list):
    df = pd.concat(df_list, sort=False)
    df = I.total_sum_spectre_stl(df)
    pp_stl(df)

    
# ------------ Get STAT files
directory = "litmus-pht"
files = ["results"]
litmus_pht = get_df_aggregate_pht(directory, files)

directory = "litmus-pht-masked"
files = ["results"]
litmus_pht_masked = get_df_aggregate_pht(directory, files)

directory = "litmus-stl"
files = ["results"]
litmus_stl = get_df_aggregate_stl(directory, files)

directory = "tea"
files = ["results"]
tea_pht = get_df_aggregate_pht(directory, files)
tea_stl = get_df_aggregate_stl(directory, files)

directory = "donna"
files = ["results"]
donna_pht  = get_df_aggregate_pht(directory, files)
donna_stl  = get_df_aggregate_stl(directory, files)

directory = "secretbox"
files = ["results"]
secretbox_pht  = get_df_aggregate_pht(directory, files)
secretbox_stl  = get_df_aggregate_stl(directory, files)

directory = "openssl-ssl3"
files = ["results"]
ssl3_pht = get_df_aggregate_pht(directory, files)
ssl3_stl = get_df_aggregate_stl(directory, files)

directory = "openssl-mee-cbc"
files = ["results"]
mee_pht = get_df_aggregate_pht(directory, files)
mee_stl = get_df_aggregate_stl(directory, files)

total_pht = [ litmus_pht, litmus_pht_masked, tea_pht, secretbox_pht,
              donna_pht, ssl3_pht, mee_pht ]
total_stl = [ litmus_stl, tea_stl, donna_stl, secretbox_stl, ssl3_stl,
              mee_stl ]
# ------------


def main():
    print("\n" + "#" * 35 + " Spectre-PHT " + "#" * 35)
    print("\n### Litmus-pht")
    pp_pht(litmus_pht)
    print("\n### Litmus-pht-masked")
    pp_pht(litmus_pht_masked)
    print("\n### Tea")
    pp_pht(tea_pht)
    print("\n### Donna")
    pp_pht(donna_pht)
    print("\n### Secretbox")
    pp_pht(secretbox_pht)
    print("\n### OpenSSL ssl3")
    pp_pht(ssl3_pht)
    print("\n### OpenSSL mee-cbc")
    pp_pht(mee_pht)
    print("\n### Total")
    pp_total_pht(total_pht)
    
    print("\n" + "#" * 35 + " Spectre-STL " + "#" * 35)
    print("\n### Litmus-stl")
    pp_stl(litmus_stl)
    print("\n### Tea")
    pp_stl(tea_stl)
    print("\n### Donna")
    pp_stl(donna_stl)
    print("\n### Secretbox")
    pp_stl(secretbox_stl)
    print("\n### OpenSSL ssl3")
    pp_stl(ssl3_stl)
    print("\n### OpenSSL mee-cbc")
    pp_stl(mee_stl)
    print("\n### Total")
    pp_total_stl(total_stl)

    
main()
