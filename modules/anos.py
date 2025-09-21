from flask import Blueprint, render_template, request, redirect, flash

import sqlite3

anos = Blueprint('anos', __name__)


def open_db(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    return conn, c


def close_db(conn, cursor):
    cursor.close()
    conn.close()


@anos.route('/<int:ano>/', methods=['GET'])
def ano_show(ano):
    if ano <= 0:
        flash('Ano invalido!', 'danger')
        return redirect(request.referrer)

    conn, c = open_db('entradas.db')

    sql = '''
    SELECT *
    FROM entradas
    WHERE ano = ?
    ORDER BY mes ASC
    '''

    c.execute(sql, (ano,))
    entradas = c.fetchall()

    close_db(conn, c)

    messes = []
    soma_messes = ['0']
    soma_anual = 0

    i = 0
    for mes in range(1, 13):
        mes_atual = []

        soma_mensal = 0
        while i < len(entradas) and mes == entradas[i]['mes']:
            mes_atual.append(entradas[i])
            soma_mensal += int(entradas[i]['valor'])
            i += 1

        messes.append(mes_atual)
        soma_messes.append(str(soma_mensal))
        soma_anual += soma_mensal

    return render_template('ano.html',
                           messes=messes,
                           soma_messes=soma_messes,
                           soma_anual=str(soma_anual),
                           ano=ano)
