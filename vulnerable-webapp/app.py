from flask import abort, Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'this_isnt_actually_secret'

import mysql.connector
from mysql.connector import pooling

db_config = {
    'database': 'vulnerable_webapp',
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'raise_on_warnings': True
}
def get_sql_commands_from_file(filename):
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()

    return filter(None, sql_file.split(';'))


class Database:
    def __init__(self):
        try:
            self.conn_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name='vulnerable_webapp_pool',
                pool_size=5,
                **db_config
            )
        except mysql.connector.Error as err:
            print ("Error when connecting to database: {}".format(err))
            self.setup_database()


    def setup_database(self):
        try:
            conn = mysql.connector.connect(
                **{
                    'user': 'root',
                    'password': '',
                    'host': '127.0.0.1',
                    'raise_on_warnings': True
                }
            )
            cursor = conn.cursor()
            setup_commands = get_sql_commands_from_file('./sql/create_schema_and_seed.sql')

            for command in setup_commands:
                cursor.execute(command)
                conn.commit()

        except mysql.connector.Error as err:
            print("Failed to create the database, error: {}".format(err))
        else:
            cursor.close()
            conn.close()

    def query(self, query, query_data={}):
        results = []
        try:
            conn = self.conn_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, query_data)

            for row in cursor:
                results.append(row)
            conn.commit()
        except mysql.connector.Error as err:
            print("Failed query, error: {}".format(err))
        else:
            cursor.close()
            conn.close()

        return results


DB = Database()

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['name']
    password = request.form['password']

    # NOTE: SQL injection!
    sql_statement = "SELECT role FROM users WHERE username = '{}' AND password = '{}'".format(
        username,
        password
    )
    print('running SQL statement: {}'.format(sql_statement))

    matching_users = DB.query(sql_statement)

    if any(matching_users):
        print('setting session...')
        session['username'] = username
        session['password'] = password
        session['role'] = matching_users[0][0]

    return redirect(url_for('users'))


@app.route('/users', methods=['GET', 'POST'])
def users():
    if not session.get('username'):
        abort(401)

    if request.method == 'GET':
        database_results = DB.query('SELECT * FROM users')
        return render_template('users.html', users=database_results, num_users=len(database_results))
    elif request.method == 'POST':
        if session.get('role') != 'admin':
            abort(403)
        username = request.form['name']
        password = request.form['password']
        # NOTE: SQL Injection!
        DB.query(
            "INSERT INTO users(username, role, password) VALUES('{}', '{}', '{}')".format(
                username, 
                'user',
                password
            )
        )
        print('adding user with username: {}'.format(username))
        return redirect(url_for('users'))


@app.route('/admin')
def admin():
    if not session.get('username'):
        abort(401)
    if session.get('role') != 'admin':
        abort(403)

    return render_template('admin.html')



if __name__ == '__main__':
    app.run(use_reloader=True)
