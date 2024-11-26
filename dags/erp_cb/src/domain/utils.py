import json
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def extract_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def transform_data(data):
    menu_item_columns = ["guestCheckLineItemId","menuItem_miNum","menuItem_modFlag","menuItem_inclTax","menuItem_activeTaxes","menuItem_prcLvl"]

    guest_checks_df = pd.json_normalize(data["guestChecks"]).drop(["taxes", "detailLines"], axis=1)
    taxes_df = pd.json_normalize(data["guestChecks"], record_path="taxes", meta=["guestCheckId"], errors="ignore")
    detail_lines_df = pd.json_normalize(data["guestChecks"], record_path="detailLines", meta=["guestCheckId"], sep="_", errors="ignore")
    menu_item_df = detail_lines_df.loc[:, menu_item_columns]

    # Formatando detail_lines_df após retirar as colunas para menu_item_df
    detail_lines_df = detail_lines_df.drop(["menuItem_miNum", "menuItem_modFlag", "menuItem_inclTax", "menuItem_activeTaxes", "menuItem_prcLvl"], axis=1)

    return guest_checks_df, taxes_df, detail_lines_df, menu_item_df


def load_to_postgres(df, table_name, postgres_conn_id="postgres_conn_default"):
    postgres_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    engine = postgres_hook.get_sqlalchemy_engine()
    df.to_sql(table_name, engine, if_exists="append", index=False)
