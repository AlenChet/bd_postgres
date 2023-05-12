import psycopg2

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR (100) NOT NULL,
    phone integer[]); """)

    conn.commit()
    cur.close()


def add_client(conn, first_name, last_name, email, phone=None):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients (first_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s)
        RETURNING id;""", (first_name, last_name, email, phone))
    result = cur.fetchone()
    if result:
        client_id = result[0]
    else:
        client_id = None

    conn.commit()
    cur.close()
    return client_id

def add_phone_number(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
        UPDATE clients
        SET phone = array_append(phone, %s)
        WHERE id = %s;
        """, (phone, client_id))

    conn.commit()
    cur.close()


def update_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    cur.execute("""
        UPDATE clients
        SET first_name = COALESCE(%s, first_name),
            last_name =  COALESCE(%s, last_name),
            email = COALESCE(%s, email),
            phone = COALESCE(%s, phone)
        WHERE id = %s;
    """, (first_name, last_name, email, phone, client_id))

    conn.commit()
    cur.close()


def delete_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
        UPDATE clients
        SET phone = array_remove(phone, %s)
        WHERE id = %s;
    """, (phone, client_id))

    conn.commit()
    cur.close()


def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM clients
        WHERE id = %s; 
    """, (client_id))

    conn.commit()
    cur.close()


def find_client(conn, **kwargs):
    cur = conn.cursor()
    query = "SELECT * FROM clients WHERE "
    params = []
    for key, value in kwargs.items():
        if key == "phone":
            query += "phone @> ARRAY[%s] "
        else:
            query += f"{key} = %s"
        params.append(value)
    cur.execute(query, params)
    result = cur.fetchall()
    return result

if __name__ == "__main__":
    db_name = input("Введите название базы данных: ")
    db_user = input("Введите пользователя: ")
    db_pass = input("Введите пароль от базы данных: ")

    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_pass)

    # create_tables(conn)
    # client1 = add_client(conn, "Ален", "Чeт", "qwe@mail.ru")
    # add_phone_number(conn, client1, 83412323)

    # client3 = add_client(conn, "Павел", "Шуст", "sf@sdj", [213812, 3413])

    # update_client(conn, client3, first_name="Игорь", email="pac@wdk.com")

    # res = find_client(conn, first_name="Ален")
    # print(res)

    # delete_phone(conn, client1, "83412323")

    # delete_client(conn, (client1, ))

    # conn.close()