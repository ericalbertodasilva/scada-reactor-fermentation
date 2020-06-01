from app import db
from datetime import datetime
import time

class Medidas(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    UR = db.Column(db.Float, nullable=False)
    reator_CO2_1 = db.Column(db.Integer, nullable=False)
    reator_CO2_2 = db.Column(db.Integer, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Medidas {}>'.format(self.id)

class Reator_fermentacao_1(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    co2 = db.Column(db.Integer, nullable=False)
    data_excel = db.Column(db.Float, nullable=False)
    art_estimado = db.Column(db.Float, nullable=False)
    etanol_estimado = db.Column(db.Float, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Reator_fermentacao_1 {}>'.format(self.id)

class Reator_fermentacao_2(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    co2 = db.Column(db.Integer, nullable=False)
    data_excel = db.Column(db.Float, nullable=False)
    art_estimado = db.Column(db.Float, nullable=False)
    etanol_estimado = db.Column(db.Float, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Reator_fermentacao_2 {}>'.format(self.id)

class Dinamica(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Dinamica {}>'.format(self.id)