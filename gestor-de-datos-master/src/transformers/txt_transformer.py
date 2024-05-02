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
                lines = txt_file.readlines()
                for line in lines:
                    # Dividir la línea en campos usando "|" como separador
                    fields = line.strip().split("|")
                    # Crear un diccionario para cada línea
                    entry = {
                        "description": fields[0],
                        "quantity": fields[1],
                        "price": fields[2],
                        "total": float(fields[1]) * float(fields[2]),
                        "invoice": fields[3],
                        "provider": fields[4],
                        "country": fields[5]
                    }
                    result.append(entry)

        with self.output().open('w') as out:
            out.write(json.dumps(result, indent=4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))


if __name__ == "__main__":
    luigi.build([TextFileTransformer()], local_scheduler=True)
