import os

from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(file, cmd, value):
    result = map(lambda log: log.strip(), file)
    if cmd == 'filter':
        result = filter(lambda log, text=value: text in log, result)

    if cmd == 'map':
        value = int(value)
        result = map(lambda log, index=value: log.split(' ')[index], result)

    if cmd == 'unique':
        result = set(result)

    if cmd == 'sort':
        if value == 'desc':
            result = sorted(result, reverse=True)
        else:
            result = sorted(result)
    if cmd == 'limit':
        value = int(value)
        result = list(result)[:value]

    return result



@app.route("/perform_query/", methods=['POST'])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат

    try:
        cmd1 = request.args["cmd1"]
        cmd2 = request.args["cmd2"]
        value1 = request.args["value1"]
        value2 = request.args["value2"]
        file_name = request.args['file_name']
    except KeyError:
        return 'Не найден параметр', 400
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return f"{file_name} не найден", 400
    with open(file_path) as file:
        result = build_query(file, cmd1, value1)
        result = build_query(result, cmd2, value2)
        content = '\n'.join(result)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()