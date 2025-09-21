from flask import Blueprint, render_template, request, redirect, url_for, flash

import sqlite3

recorrentes = Blueprint("recorrentes", __name__)


def open_db(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    return conn, c


def close_db(conn, cursor):
    cursor.close()
    conn.close()


@recorrentes.route("/recorrentes/", methods=["GET"])
def recorrentes_index():
    conn, c = open_db("entradas.db")

    sql = '''
    SELECT *
    FROM recorrentes
    '''

    c.execute(sql)
    recorrentes = c.fetchall()

    close_db(conn, c)

    return render_template("recorrente.html",
                           recorrentes=recorrentes)


@recorrentes.route("/recorrentes/", methods=["POST"])
def recorrente_store():
    descricao = request.form.get("descricao")

    if descricao:
        conn, c = open_db("entradas.db")

        sql = '''
        INSERT INTO recorrentes (descricao)
        VALUES (?)
        '''

        c.execute(sql, (descricao,))
        conn.commit()

        close_db(conn, c)

        flash("Entrada inserida com sucesso!", "success")
    else:
        flash("Entrada não inserida!", "danger")

    return redirect(url_for(".recorrentes_index"))


@recorrentes.route("/recorrentes/<int:recorrente_id>/edit/", methods=["GET"])
def recorrente_edit(recorrente_id):

    conn, c = open_db("entradas.db")

    sql = '''
    SELECT *
    FROM recorrentes
    WHERE id = ?
    ORDER BY id ASC
    '''

    c.execute(sql, (recorrente_id,))
    recorrente = c.fetchone()

    return render_template("recorrente_edit.html",
                           recorrente=recorrente)


@recorrentes.route("/recorrentes/<int:recorrente_id>", methods=["POST"])
def recorrente_update(recorrente_id):
    descricao = request.form.get("descricao")

    if descricao:
        conn, c = open_db("entradas.db")

        sql = '''
        UPDATE recorrentes
        SET descricao = ?
        WHERE id = ?
        '''

        c.execute(sql, (descricao, recorrente_id))
        conn.commit()

        close_db(conn, c)

        flash("Entrada editada com sucesso!", "success")
    else:
        flash("Entrada não editada!", "danger")

    return redirect(url_for(".recorrentes_index"))


@recorrentes.route("/recorrentes/<int:recorrente_id>/delete", methods=["GET"])
def recorrente_destroy(recorrente_id):
    conn, c = open_db("entradas.db")

    sql = '''
    DELETE FROM recorrentes
    WHERE id = ?
    '''

    c.execute(sql, (recorrente_id, ))
    conn.commit()

    close_db(conn, c)

    flash("Entrada removida com sucesso!", "success")

    return redirect(url_for(".recorrentes_index"))
