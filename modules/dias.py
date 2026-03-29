from datetime import date, timedelta
from flask import Blueprint, render_template, request, redirect, flash

import sqlite3

dias = Blueprint('dias', __name__)


def valida_data(s):
    try:
        date.fromisoformat(s)
    except ValueError:
        return False
    return True


def open_db(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    return conn, c


def close_db(conn, cursor):
    cursor.close()
    conn.close()


@dias.route('/<int:ano>/<int:mes>/<int:dia>/', methods=["GET"])
def dia_show(ano, mes, dia):
    if ano <= 0:
        flash('Ano inválido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes inválido!', 'danger')
        return redirect(request.referrer)

    data = f'{ano}-{mes:0>2}-{dia:0>2}'
    if not valida_data(data):
        flash('Dia inválido!', 'danger')
        return redirect(request.referrer)

    conn, c = open_db('entradas.db')

    sql = '''
    SELECT *
    FROM entradas
    WHERE agendado = ?
    '''

    c.execute(sql, (data,))
    agendados = c.fetchall()

    sql = '''
    SELECT *
    FROM entradas
    WHERE pago = ?
    '''

    c.execute(sql, (data,))
    pagos = c.fetchall()

    close_db(conn, c)

    soma_agendado = sum(int(agendado['valor']) for agendado in agendados)
    soma_pago = sum(int(pago['valor']) for pago in pagos)

    hoje = date.fromisoformat(data)

    ontem_d = hoje + timedelta(days=-1)
    ontem = {'ano': ontem_d.year, 'mes': ontem_d.month, 'dia': ontem_d.day}

    amanha_d = hoje + timedelta(days=+1)
    amanha = {'ano': amanha_d.year, 'mes': amanha_d.month, 'dia': amanha_d.day}

    return render_template('dia.html',
                           agendados=agendados,
                           soma_agendado=str(soma_agendado),
                           pagos=pagos,
                           soma_pago=str(soma_pago),
                           ano=ano,
                           mes=mes,
                           dia=dia,
                           ontem=ontem,
                           amanha=amanha)
