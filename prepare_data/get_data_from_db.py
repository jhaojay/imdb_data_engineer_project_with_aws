import mydb


def get_movie_info():
    psdb = mydb.MyDB()
    psdb.connect()

    headers = []
    headers_sql = """SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'movie_info'"""
    for item in psdb.query(headers_sql, fetch=True):
        headers.append(item[0])

    data = []
    data_sql = """SELECT gross, run_time_min, imdb_rating, metascore, num_voted_users, id, imdb_movie_id, title, release_year, certificate, description FROM movie_info"""
    for item in psdb.query(data_sql, fetch=True):
        data.append(list(item))

    psdb.close()
    return headers, data

def get_person():
    psdb = mydb.MyDB()
    psdb.connect()

    headers = []
    headers_sql = """SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'person'"""
    for item in psdb.query(headers_sql, fetch=True):
        headers.append(item[0])

    data = []
    data_sql = """SELECT id, imdb_person_id, full_name FROM person"""
    for item in psdb.query(data_sql, fetch=True):
        data.append(list(item))

    psdb.close()

    return headers, data

def get_movie_director():
    psdb = mydb.MyDB()
    psdb.connect()

    headers = []
    headers_sql = """SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'movie_director'"""
    for item in psdb.query(headers_sql, fetch=True):
        headers.append(item[0])

    data = []
    data_sql = """SELECT movie_id, person_id FROM movie_director"""
    for item in psdb.query(data_sql, fetch=True):
        data.append(list(item))

    psdb.close()

    return headers, data