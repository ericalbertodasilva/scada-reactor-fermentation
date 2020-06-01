# coding: utf-8

from app import app
from app.models import *


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Medidas': Medidas, 'Reator_fermentacao_1': Reator_fermentacao_1,
            'Reator_fermentacao_2': Reator_fermentacao_2, 'Dinamica': Dinamica}


if __name__ == "__main__":
    import logging

    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(debug=True)
