from .models import Gist
from datetime import datetime

def search_gists(db_connection, **kwargs):
    query = "SELECT * FROM gists WHERE 1=1"
    params = {}

    for key, value in kwargs.items():
        if key in ['github_id', 'comments_url']:
            query += f" AND {key} = :{key}"
            params[key] = value
        elif 'created_at__' in key or 'updated_at__' in key:
            field, operator = key.split('__')
            if operator == 'gt':
                query += f" AND datetime({field}) > datetime(:{field}_{operator})"
            elif operator == 'gte':
                query += f" AND datetime({field}) >= datetime(:{field}_{operator})"
            elif operator == 'lt':
                query += f" AND datetime({field}) < datetime(:{field}_{operator})"
            elif operator == 'lte':
                query += f" AND datetime({field}) <= datetime(:{field}_{operator})"
            params[f"{field}_{operator}"] = value

    cursor = db_connection.execute(query, params)
    gists = [Gist(row) for row in cursor.fetchall()]
    cursor.close()

    return gists
