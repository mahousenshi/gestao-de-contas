from flask import Blueprint, render_template, request, redirect, flash

import sqlite3

messes = Blueprint('messes', __name__)


def open_db(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    return conn, c


def close_db(conn, cursor):
    cursor.close()
    conn.close()


@messes.route('/<int:ano>/<int:mes>/')
def mes_show(ano, mes):
    if ano <= 0:
        flash('Ano invalido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes invalido!', 'danger')
        return redirect(request.referrer)

    conn, c = open_db('entradas.db')

    sql = '''
    SELECT *
    FROM entradas
    WHERE ano = ?
    AND mes = ?
    ORDER BY id ASC
    '''

    c.execute(sql, (ano, mes))
    entradas = c.fetchall()

    soma_mes = str(sum(int(entrada['valor']) for entrada in entradas))

    close_db(conn, c)

    return render_template('mes.html',
                           entradas=entradas,
                           soma_mes=soma_mes,
                           ano=ano,
                           mes=mes)
