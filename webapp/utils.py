def get_id_by_name(name, table):
    for row in table:
        if row.name == name:
            return row.id
    return None
