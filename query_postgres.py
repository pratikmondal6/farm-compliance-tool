import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from psycopg2 import sql

url = "postgresql://postgres.tgrpmxrajpgbtxwymrkf:1234@aws-1-eu-north-1.pooler.supabase.com:6543/postgres?sslmode=require"

def query_postgres_url_json(conn_url, query):
    """
    Connects to PostgreSQL using a connection URL and executes a query.
    Returns results as a list of dictionaries (JSON-like).

    Parameters:
        conn_url (str): PostgreSQL connection URL.
        query (str): SQL query to execute.

    Returns:
        list[dict]: Query result as list of dictionaries, or None on failure.
    """
    try:
        conn = psycopg2.connect(conn_url)

        # Use RealDictCursor to get results as dictionaries
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            try:
                results = cur.fetchall()
            except psycopg2.ProgrammingError:
                results = []
            conn.commit()
        dict_rows = [dict(row) for row in results]
        return dict_rows

    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return None

    finally:
        if 'conn' in locals():
            conn.close()

def fetch_items_by_code_list(conn_url, table, code_list):
    """
    Fetch rows from the given table where code is in the provided list.

    Args:
        conn_url (str): PostgreSQL connection URL.
        table (str): Table name.
        code_list (list): List of codes to filter by.

    Returns:
        list[dict]: List of matching rows as dictionaries.
    """
    

    if not code_list:
        return []

    try:
        conn = psycopg2.connect(conn_url)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Dynamically build the SQL with placeholders for the code list
            query = sql.SQL("SELECT * FROM {table} WHERE code IN %s").format(
                table=sql.Identifier(table)
            )
            cur.execute(query, (tuple(code_list),))
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        if 'conn' in locals():
            conn.close()
def get_regulations_associated_with_article(codes):
    # print(codes)
    # query = "SELECT * FROM safety_instructions where code='"+code+"';"
    items = fetch_items_by_code_list(url, "safety_instructions", codes)

    # result=[]
    # result = query_postgres_url_json(url, query)
    return items

def get_constraints_associated_with_article(codes):
    # print(codes)
    # query = "SELECT * FROM safety_instructions where code='"+code+"';"
    items = fetch_items_by_code_list(url, "field_constraints", codes)

    # result=[]
    # result = query_postgres_url_json(url, query)
    return items
