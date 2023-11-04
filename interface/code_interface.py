#%%
import tkinter as tk
from tkinter import ttk
import sqlite3

# Fonction pour exécuter la recherche
def rechercher():
    critere = critere_entry.get()
    conn = sqlite3.connect("atc.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT A.fmppnm, H.TI, G.FGalNm, A.ddd, A.ddu, M.Cheapest, M.Narcotic, A.summary, GG.Link2MPG FROM (SELECT * FROM ATCDPP LEFT JOIN PBT ON ATCDPP.atc = PBT.atc) A, MPP M, DCI D, GAL G, GGR_LINK GG, HYR H,IR I, MP, SAM S, STOF ST WHERE A.fmppnm LIKE ? AND M.mppcv LIKE A.mppcv AND M.mppcv LIKE GG.Mppcv AND M.mppcv LIKE D.ampp_cnk_pub AND M.mppcv LIKE S.mppcv AND S.Stofcv LIKE ST.StofCV AND M.mpcv LIKE MP.MPcv AND I.IRCV LIKE MP.IRCV AND M.hyrcv LIKE H.HyrCV AND M.GalCV LIKE G.GalCV", ('%' + critere + '%',))
    result = cursor.fetchall()
    conn.close()

    # Efface les données actuelles dans le tableau
    effacer_tableau()

    if result:
        for row in result:
            tableau.insert("","end", values=row)
    else:
        tableau.insert("", "end", values=("Aucun résultat trouvé.", "", ""))

# Fonction pour effacer les données actuelles du tableau
def effacer_tableau():
    for row in tableau.get_children():
        tableau.delete(row)

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Interface de recherche")
fenetre.configure(bg="white")

# Créer une étiquette et une zone de texte pour le critère de recherche
critere_label = tk.Label(fenetre, text="Entrez le nom du médicament à rechercher :")
critere_label.pack()
critere_entry = tk.Entry(fenetre)
critere_entry.pack()

# Créer un bouton pour lancer la recherche
rechercher_bouton = tk.Button(fenetre, text="Rechercher", bg="white", command=rechercher)
rechercher_bouton.pack()

# Créer un tableau pour afficher les résultats
tableau = ttk.Treeview(fenetre, columns=("fmppnm", "TI", "FGalNm", "ddd", "ddu", "Cheapest", "Narcotic", "PBT", "Link2MPG"))
tableau.heading("#1", text="Nom complet")
tableau.heading("#2", text="Action")
tableau.heading("#3", text="Méthode d'administration")
tableau.heading("#4'", text="ddd")
tableau.heading("#5", text="ddu")
tableau.heading("#6", text="Moins cher")
tableau.heading("#7", text="Narcotique")
tableau.heading("#8", text="PBT")
tableau.heading("#9", text="Lien CBIP par groupe")
tableau.pack()

# Ajuster la taille des colonnes
tableau.column("#0", width=0)  
tableau.column("#1", width=300)  
tableau.column("#2", width=100) 
tableau.column("#3", width=150)  
tableau.column("#4", width=70) 
tableau.column("#5", width=50)  
tableau.column("#6", width=100)  
tableau.column("#7", width=100)  
tableau.column("#8", width=700) 
tableau.column("#9", width=300)

# Démarrer la boucle principale de l'interface
fenetre.mainloop()