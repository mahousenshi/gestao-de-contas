from datetime import date
from itertools import batched
from flask import Flask, redirect, url_for

from modules.anos import anos
from modules.dias import dias
from modules.messes import messes
from modules.entradas import entradas
from modules.recorrentes import recorrentes

app = Flask(__name__)
app.secret_key = '11e5de3cbf69ed9f0dfa512f78652af7b1810b26dfb4c14e4c575a590d5fc50f'

app.register_blueprint(anos)
app.register_blueprint(dias)
app.register_blueprint(messes)
app.register_blueprint(entradas)
app.register_blueprint(recorrentes)


@app.context_processor
def hoje():
    hoje = date.today()
    return dict(hoje={'ano': hoje.year, 'mes': hoje.month, 'dia': hoje.day})


@app.template_filter('mes_br')
def mes_br_filter(n):
    return ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][n]


@app.template_filter('data_br')
def data_filter(s):
    if s:
        ano, mes, dia = s.split('-')
        return f'{dia}/{mes}/{ano}'
    return ''


@app.template_filter('dinheiro')
def dinheiro_filter(s):
    if len(s) == 1:
        return f'0,0{s}'
    elif len(s) == 2:
        return f'0,{s}'

    reais, centavos = s[:-2], s[-2:]

    return f'{centavos[::-1]},{','.join(''.join(bloco) for bloco in batched(reais[::-1], 3))}'[::-1]


@app.route('/')
def index():
    hoje = date.today()
    return redirect(url_for('messes.mes_show',
                            ano=hoje.year,
                            mes=hoje.month))


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
