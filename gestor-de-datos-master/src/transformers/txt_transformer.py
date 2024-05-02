##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: txt_transformer.py
# Capitulo: Flujo de Datos
# Autor(es): Heli, Cristian, Jorge y Jonathan
# Version: 1.0.1 Marzo 2023
# Descripción:
#
#   Este archivo define un procesador de datos que se encarga de transformar
#   y formatear el contenido de un archivo TXT
#-------------------------------------------------------------------------
from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, csv, json, re

class TXTransformer(luigi.Task):
    def requires(self):
        return TXTExtractor()

    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                data = txt_file.read()
                # Split rows by ';'
                rows = data.strip().split(';')
                for i in len(1, rows):
                    # Split fields by ','
                    fields = row[i].strip().split(',')
                    # Create a dictionary for each row
                    entry = {
                        "description": fields[2],
                        "quantity": fields[3],
                        "price": fields[5],
                        "total": float(fields[3]) * float(fields[5]),
                        "invoice": fields[0],
                        "provider": fields[6],
                        "country": fields[7]
                    }
                    result.append(entry)

        with self.output().open('w') as out:
            out.write(json.dumps(result, indent =4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))

