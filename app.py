import os
import re
from typing import Union, Tuple, Iterator, Set, List, Dict

from flask import Flask, request, Response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(file: Union[Iterator[str], List, Set], cmd: str, value: Union[str, int]) -> Union[
    Iterator[str], List, Set]:
    result: Union[Iterator[str], List, Set] = map(lambda log: log.strip(), file)
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

    if cmd == 'regex':
        regex = re.compile(rf'{value}')
        result = filter(lambda log: regex.search(log), result)

    if cmd == 'limit':
        value = int(value)
        result = list(result)[:value]

    return result


@app.route("/perform_query/", methods=['POST'])
def perform_query() -> Union[Response, Tuple[str, int]]:
    try:
        data: Dict[str, str] = request.get_json()  # type:ignore
    except KeyError:
        return 'Пустое поле запроса', 400

    try:
        cmd1: str = data["cmd1"]
        cmd2: str = data["cmd2"]
        value1: str = data["value1"]
        value2: str = data["value2"]
        file_name: str = data['file_name']
    except KeyError:
        return 'Не найден параметр', 400
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return f"{file_name} не найден", 400
    with open(file_path) as file:
        result: Union[Iterator[str], List, Set] = build_query(file, cmd1, value1)
        result = build_query(result, cmd2, value2)
        content = '\n'.join(result)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()
