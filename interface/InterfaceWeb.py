# -*- coding: utf-8 -*-
"""
Created on Sat Nov 4 12:51:07 2023
@author: Thonnard Julien
"""

from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Configuration de la base de données SQLite
DATABASE = 'atc.sqlite'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/', methods=['GET', 'POST'])
def recherche():
    resultats = []
    include_additional_condition = False  # par défaut, la case n'est pas cochée
    
    if request.method == 'POST':
        # Récupérer les termes de recherche du formulaire
        terme_de_recherche = request.form['terme_de_recherche']
        
        # Vérifier si la case a été cochée
        if 'include_additional_condition' in request.form:
            include_additional_condition = True

        # Établir une connexion à la base de données
        conn = connect_db()
        cur = conn.cursor()

        # Construire la requête SQL en fonction de la case à cocher
        if include_additional_condition:
            # Exécuter une requête SQL avec la condition supplémentaire
            cur.execute('select A.fmppnm, HYR.TI, A.ddd, A.ddu, MPP.Cheapest, MPP.Narcotic, A.Persistence, A.Bioaccumulation, A.Toxicity, MPP.bilan_carbone from ((A full outer join MPP on MPP.mppcv = A.mppcv) full outer join HYR on MPP.hyrcv = HYR.HyrCV) where A.fmppnm LIKE ?', ('%' + terme_de_recherche + '%',))
        else:
            # Exécuter une requête SQL sans la condition supplémentaire
            cur.execute('select A.fmppnm, A.ddd, A.ddu, MPP.Cheapest, MPP.Narcotic, A.Persistence, A.Bioaccumulation, A.Toxicity, MPP.bilan_carbone from ((A join MPP on MPP.mppcv = A.mppcv) full outer join HYR on MPP.hyrcv = HYR.HyrCV) where HYR.TI LIKE ?', ('%' + terme_de_recherche + '%',))

        resultats = cur.fetchall()

        # Fermer la connexion
        conn.close()

    return render_template('recherche.html', resultats=resultats, include_additional_condition=include_additional_condition)

if __name__ == '__main__':
    app.run()

