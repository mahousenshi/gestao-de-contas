from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash

import sqlite3

entradas = Blueprint('entradas', __name__)


def valida_data(s):
    try:
        date.fromisoformat(s)
    except ValueError:
        return False
    return True


def valida_valor(s):
    try:
        int(s)
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


@entradas.route('/<int:ano>/<int:mes>', methods=['POST'])
def entrada_store(ano, mes):
    if ano <= 0:
        flash('Ano inválido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes inválido!', 'danger')
        return redirect(request.referrer)

    descricao = request.form.get('descricao')
    pago = request.form.get('pago')
    agendado = request.form.get('agendado')
    valor = request.form.get('valor')
    comentario = request.form.get('comentario')

    if descricao:
        if pago is None or pago == '':
            pago = ''
        elif not valida_data(pago):
            flash('Data de pagamento inválida!', 'danger')
            return redirect(request.referrer)

        if agendado is None or agendado == '':
            agendado = ''
        elif not valida_data(agendado):
            flash('Data de agendadameto inválida!', 'danger')
            return redirect(request.referrer)

        valor = valor.replace(',', '').replace('.', '')
        if valor is None:
            valor = '0'
        elif not valida_valor(valor):
            flash('Valor inválido!', 'danger')
            return redirect(request.referrer)

        comentario = '' if comentario is None else comentario

        conn, c = open_db('entradas.db')

        sql = '''
        INSERT INTO entradas (ano, mes, descricao, pago, agendado, valor, comentario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        c.execute(sql, (ano, mes, descricao, pago, agendado, valor, comentario))
        conn.commit()

        close_db(conn, c)

        flash('Entrada inserida com sucesso!', 'success')
    else:
        flash('Entrada não inserida!', 'danger')

    return redirect(url_for('messes.mes_show',
                            ano=ano,
                            mes=mes))


@entradas.route('/<int:ano>/<int:mes>/<int:entrada_id>/edit', methods=['GET'])
def entrada_edit(ano, mes, entrada_id):
    if ano <= 0:
        flash('Ano inválido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes inválido!', 'danger')
        return redirect(request.referrer)

    conn, c = open_db('entradas.db')

    sql = '''
    SELECT *
    FROM entradas
    WHERE id = ?
    ORDER BY id ASC
    '''

    c.execute(sql, (entrada_id,))
    entrada = c.fetchone()

    return render_template('entrada_edit.html',
                           entrada=entrada,
                           ano=ano,
                           mes=mes)


@entradas.route('/<int:ano>/<int:mes>/<int:entrada_id>', methods=['POST'])
def entrada_update(ano, mes, entrada_id):
    if ano <= 0:
        flash('Ano inválido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes inválido!', 'danger')
        return redirect(request.referrer)

    descricao = request.form.get('descricao')
    pago = request.form.get('pago')
    agendado = request.form.get('agendado')
    valor = request.form.get('valor')
    comentario = request.form.get('comentario')

    if descricao:
        if pago is None or pago == '':
            pago = ''
        elif not valida_data(pago):
            flash('Data de pagamento inválida!', 'danger')
            return redirect(request.referrer)

        if agendado is None or agendado == '':
            agendado = ''
        elif not valida_data(agendado):
            flash('Data de agendadameto inválida!', 'danger')
            return redirect(request.referrer)

        valor = valor.replace(',', '').replace('.', '')
        if valor is None:
            valor = '0'
        elif not valida_valor(valor):
            flash('Valor inválido!', 'danger')
            return redirect(request.referrer)

        comentario = '' if comentario is None else comentario

        conn, c = open_db('entradas.db')

        sql = '''
        UPDATE entradas
        SET descricao = ?,
            pago = ?,
            agendado = ?,
            valor = ?,
            comentario = ?
        WHERE id = ?
        '''

        c.execute(sql, (descricao, pago, agendado, int(valor), comentario, entrada_id))
        conn.commit()

        close_db(conn, c)

        flash('Entrada editada com sucesso!', 'success')
    else:
        flash('Entrada não editada!', 'danger')

    return redirect(url_for('messes.mes_show',
                            ano=ano,
                            mes=mes))


@entradas.route('/<int:ano>/<int:mes>/<int:entrada_id>/delete', methods=['GET'])
def entrada_destroy(ano, mes, entrada_id):
    if ano <= 0:
        flash('Ano inválido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes inválido!', 'danger')
        return redirect(request.referrer)

    conn, c = open_db('entradas.db')

    sql = '''
    DELETE FROM entradas
    WHERE id = ?
    '''

    c.execute(sql, (entrada_id, ))
    conn.commit()

    close_db(conn, c)

    flash('Entrada removida com sucesso!', 'success')

    return redirect(url_for('messes.mes_show',
                            ano=ano,
                            mes=mes))


@entradas.route('/<int:ano>/<int:mes>/recorrentes')
def mes_recorrente(ano, mes):
    if ano <= 0:
        flash('Ano inválido!', 'danger')
        return redirect(request.referrer)

    if mes <= 0 or mes > 12:
        flash('Mes inválido!', 'danger')
        return redirect(request.referrer)

    conn, c = open_db('entradas.db')

    sql = '''
    SELECT *
    FROM recorrentes
    '''

    c.execute(sql)
    recorrentes = c.fetchall()

    for recorrente in recorrentes:
        sql = '''
        INSERT INTO entradas (ano, mes, descricao, pago, agendado, valor, comentario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        c.execute(sql, (ano, mes, recorrente['descricao'], '', '', '0', ''))
        conn.commit()

    close_db(conn, c)

    flash('Entradas inseridas com sucesso!', 'success')

    return redirect(url_for('messes.mes_show',
                            ano=ano,
                            mes=mes))
