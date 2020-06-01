# coding: utf-8

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory, json, jsonify
from app import app, db
from app.models import *
import time

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Medidas': Medidas, 'Reator_fermentacao_1': Reator_fermentacao_1, 'Reator_fermentacao_2': Reator_fermentacao_2, 'Dinamica':Dinamica}

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True)