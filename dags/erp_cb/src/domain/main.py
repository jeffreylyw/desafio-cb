from erp_cb.src.domain.utils import *

def etl_erp_cb(**kwargs):
    file_path = kwargs['file_path']
    postgres_conn_id = kwargs['postgres_conn']

    data = extract_json(file_path)
    df_guest_checks, df_taxes, df_detail_lines, df_menu_item = transform_data(data)

    load_to_postgres(df_guest_checks, 'guest_checks', postgres_conn_id)
    load_to_postgres(df_taxes, 'taxes', postgres_conn_id)
    load_to_postgres(df_detail_lines, 'detail_lines', postgres_conn_id)
    load_to_postgres(df_menu_item, 'menu_items', postgres_conn_id)