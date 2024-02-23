from tkinter import *
import tkinter as tk
import os.path as OP
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

import sys
sys.path.append(r"dist")
import chess
import chess.engine



# Définition du plateau d'échecs sous forme de liste de listes
plateau = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

autorise_roque = [1,1,1,1]


# Variable pour suivre le tour actuel
tour_blanc = True
tour_précédent = []

#pour la fonction pointeur qui detecte les clics
depart_deplacement_lig = 20
depart_deplacement_col = 20

arriere_plan = "#2A3A4A"
contour = "#5A6A7A"
case_blanche = "#B4CFEC"
case_noire = "#235A8C"






def obtenir_meilleur_coup(fen_position):
    # Initialiser le moteur Stockfish
    with chess.engine.SimpleEngine.popen_uci("stockfish.exe") as engine:
        # Charger la position depuis la notation FEN
        position = chess.Board(fen_position)

        # Demander le meilleur coup au moteur Stockfish
        result = engine.play(position, chess.engine.Limit(time=2.0))

        # Afficher le meilleur coup
        print("Meilleur coup:", result.move.uci())
        return result.move.uci()


def plateau_to_fen(plateau, tour_blanc, autorise_roque):
    fen = ''
    
    # Conversion du plateau en chaîne FEN
    for row in plateau:
        empty_count = 0
        for piece in row:
            if piece == ' ':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += piece
        if empty_count > 0:
            fen += str(empty_count)
        fen += '/'
    
    # Suppression du dernier '/'
    fen = fen[:-1]
    
    # Ajout d'informations supplémentaires
    fen += ' ' + ('w' if tour_blanc else 'b')  # Tour actuel (blanc ou noir)
    fen += ' '
    
    # Autorisation de roque
    fen += 'K' if autorise_roque[3] else ''
    fen += 'Q' if autorise_roque[2] else ''
    fen += 'k' if autorise_roque[1] else ''
    fen += 'q' if autorise_roque[0] else ''
    
    if not(autorise_roque[0]) and not(autorise_roque[1]) and not(autorise_roque[2]) and not(autorise_roque[3]):
        fen += "-"
    
    
    fen += ' - 0 1'  # Informations supplémentaires (pouvant être adaptées selon les besoins)
    
    return fen



def coup_ordi():
    
    fen_resultat = plateau_to_fen(plateau, tour_blanc, autorise_roque)
    
    print(fen_resultat)
    
    meill_coup = obtenir_meilleur_coup(fen_resultat)
    
    for i in range(8):
        if ord(meill_coup[0]) == 97+i:
            d_col = i
        if ord(meill_coup[2]) == 97+i:
            a_col = i

    d_lig = 8-int(meill_coup[1])
    a_lig = 8-int(meill_coup[3])
    
    depart = (d_col, d_lig)
    arrivee = (a_col, a_lig)
    
    deplacer_piece(depart, arrivee)
    
    print(depart)
    print(arrivee)
    print("oui")
    print(plateau)
    afficher_pièces()
    



def roi_blanc_vivant():
    
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == "K":
                return True
    canv.create_text(hauteur/2, hauteur/2, text="LES BLANCS ONT PERDU", font=("Courier", 30), fill="#1A2A3A")
def roi_noir_vivant():
    
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == "k":
                return True
    canv.create_text(hauteur/2, hauteur/2, text="LES BLANCS ONT BATTU LES NOIRS", font=("Courier", 30), fill="#1A2A3A")



def case_en_échec(a_lig, a_col, couleur):

    for i in range(8):
        for j in range(8):
            if plateau[i][j] != " " and plateau[i][j] != "k" and plateau[i][j] != "K":
                if autorisation_deplacement(j, i, a_col, a_lig, tour_précédent) == True:
                    if couleur == "blanc":
                        if plateau[i][j].islower():
                            return True
                    else :
                        if plateau[i][j].isupper():
                            return True
    return False

def roi_noir_en_échec():

    for i in range(8):
        for j in range(8):
            if plateau[i][j] == "k":
                if case_en_échec(i, j, "noir") == True:
                    return True
    return False

def roi_blanc_en_échec():

    for i in range(8):
        for j in range(8):
            if plateau[i][j] == "K":
                if case_en_échec(i, j, "blanc") == True:
                    return True
    return False









def vérif_roque(d_col, d_lig, a_col, a_lig):
    
    if plateau[d_lig][d_col] == "k" :
        
        if d_lig == 0 and d_col == 4:
            if a_lig == 0 and a_col == 2 and autorise_roque[0] == 1:
                plateau[0][0] = " "
                plateau[0][3] = "r"
                autorise_roque[0] = 0
                autorise_roque[1] = 0
                return
            elif a_lig == 0 and a_col == 6 and autorise_roque[1] == 1:
                plateau[0][7] = " "
                plateau[0][5] = "r"
                autorise_roque[0] = 0
                autorise_roque[1] = 0
                return
    
    elif plateau[d_lig][d_col] == "K" :
        
        if d_lig == 7 and d_col == 4:
            if a_lig == 7 and a_col == 2 and autorise_roque[2] == 1:
                plateau[7][0] = " "
                plateau[7][3] = "R"
                autorise_roque[2] = 0
                autorise_roque[3] = 0
                return
            elif a_lig == 7 and a_col == 6 and autorise_roque[3] == 1:
                plateau[7][7] = " "
                plateau[7][5] = "R"
                autorise_roque[2] = 0
                autorise_roque[3] = 0
                return
    return



def effectuer_promotion_Q():
    
    for i in range(8):
        if plateau[0][i] == "P":
            plateau[0][i] = "Q"
        elif plateau[7][i] == "p":
            plateau[7][i] = "q"
    promo_Q.place(x=10000, y=10000)
    promo_T.place(x=10000, y=10000)
    promo_F.place(x=10000, y=10000)
    promo_C.place(x=10000, y=10000)
    afficher_pièces()

def effectuer_promotion_T():
    
    for i in range(8):
        if plateau[0][i] == "P":
            plateau[0][i] = "R"
        elif plateau[7][i] == "p":
            plateau[7][i] = "r"
    promo_Q.place(x=10000, y=10000)
    promo_T.place(x=10000, y=10000)
    promo_F.place(x=10000, y=10000)
    promo_C.place(x=10000, y=10000)
    afficher_pièces()
    
def effectuer_promotion_F():
    
    for i in range(8):
        if plateau[0][i] == "P":
            plateau[0][i] = "B"
        elif plateau[7][i] == "p":
            plateau[7][i] = "b"
    promo_Q.place(x=10000, y=10000)
    promo_T.place(x=10000, y=10000)
    promo_F.place(x=10000, y=10000)
    promo_C.place(x=10000, y=10000)
    afficher_pièces()
    
def effectuer_promotion_C():
    
    for i in range(8):
        if plateau[0][i] == "P":
            plateau[0][i] = "N"
        elif plateau[7][i] == "p":
            plateau[7][i] = "n"
    promo_Q.place(x=10000, y=10000)
    promo_T.place(x=10000, y=10000)
    promo_F.place(x=10000, y=10000)
    promo_C.place(x=10000, y=10000)
    afficher_pièces()

def vérif_promotion():
    
    for i in range(8):
        
        if plateau[0][i] == "P":
            promo_Q.place(x=(i+1)*coef, y=2.2*coef)
            promo_T.place(x=(i+1)*coef, y=2.6*coef)
            promo_F.place(x=(i+1)*coef, y=3*coef)
            promo_C.place(x=(i+1)*coef, y=3.4*coef)
        elif plateau[7][i] == "p":
            promo_Q.place(x=(i+1)*coef, y=6.4*coef)
            promo_T.place(x=(i+1)*coef, y=6.8*coef)
            promo_F.place(x=(i+1)*coef, y=7.2*coef)
            promo_C.place(x=(i+1)*coef, y=7.6*coef)
            
    




#Verifier pour chaque pièces si le coup est règlementaire

def autorisation_roi(d_col, d_lig, a_col, a_lig):
    
    if (plateau[d_lig][d_col] == "K" and case_en_échec(a_lig, a_col, "blanc") == False) or (plateau[d_lig][d_col] == "k" and case_en_échec(a_lig, a_col, "noir") == False) :
    
        if a_lig == d_lig+1 and a_col == d_col+1 :
            return True
        elif a_lig == d_lig+1 and a_col == d_col :
            return True
        elif a_lig == d_lig+1 and a_col == d_col-1 :
            return True    
        elif a_lig == d_lig and a_col == d_col+1 :
            return True
        elif a_lig == d_lig and a_col == d_col-1 :
            return True    
        elif a_lig == d_lig-1 and a_col == d_col+1 :
            return True
        elif a_lig == d_lig-1 and a_col == d_col :
            return True    
        elif a_lig == d_lig-1 and a_col == d_col-1 :
            return True
        
        #pour le roque :
        elif plateau[d_lig][d_col] == "K":
            if a_lig == 7 and a_col == 2 and plateau[7][0] == "R" and plateau[7][1] == " " and plateau[7][2] == " " and plateau[7][3] == " ":             
                return True
            elif a_lig == 7 and a_col == 6 and plateau[7][7] == "R" and plateau[7][6] == " " and plateau[7][5] == " ":     
                return True
            elif plateau[d_lig][d_col] == "k":
                if a_lig == 0 and a_col == 2 and plateau[0][0] == "r" and plateau[0][1] == " " and plateau[0][2] == " " and plateau[0][3] == " ":           
                    return True
                elif a_lig == 0 and a_col == 6 and plateau[0][7] == "r" and plateau[0][6] == " " and plateau[0][5] == " ":         
                    return True
    
        else : return False
    else : return False


def autorisation_tour(d_col, d_lig, a_col, a_lig):
    
    if a_lig == d_lig:
        if a_col > d_col :
            for i in range(d_col+1, a_col):
                if plateau[a_lig][i] != " ":
                    return False
            return True
        if a_col < d_col :
            for i in range(d_col-1, a_col, -1):
                if plateau[a_lig][i] != " ":
                    return False
            return True
        
    elif a_col == d_col:
        if a_lig > d_lig :
            for i in range(d_lig+1, a_lig):
                if plateau[i][a_col] != " ":
                    return False
            return True
        if a_lig < d_lig :
            for i in range(d_lig-1, a_lig, -1):
                if plateau[i][a_col] != " ":
                    return False
            return True

    else : return False
    
    
def autorisation_cavalier(d_col, d_lig, a_col, a_lig):
    
    if a_lig == d_lig+1 and a_col == d_col+2:
        return True
    elif a_lig == d_lig+1 and a_col == d_col-2:
        return True
    elif a_lig == d_lig-1 and a_col == d_col-2:
        return True    
    elif a_lig == d_lig-1 and a_col == d_col+2:
        return True
    elif a_lig == d_lig+2 and a_col == d_col+1:
        return True    
    elif a_lig == d_lig+2 and a_col == d_col-1:
        return True
    elif a_lig == d_lig-2 and a_col == d_col+1:
        return True    
    elif a_lig == d_lig-2 and a_col == d_col-1:
        return True
    else : return False
    
    
def autorisation_fou(d_col, d_lig, a_col, a_lig):

    if a_col > d_col:
        if a_lig > d_lig:
            if a_lig-d_lig == a_col-d_col:       
                for i in range(1, a_lig - d_lig):  
                    if plateau[d_lig + i][d_col + i] != " ":
                        return False
                return True
            else : return False
        elif a_lig < d_lig:
            if d_lig-a_lig == a_col-d_col:
                for i in range(1, d_lig - a_lig):  
                    if plateau[d_lig - i][d_col + i] != " ":
                        return False
                return True
            else : return False
        else : 
            return False
    if a_col < d_col:
        if a_lig > d_lig:
            if a_lig-d_lig == d_col-a_col:
                for i in range(1, a_lig - d_lig):  
                    if plateau[d_lig + i][d_col - i] != " ":
                        return False                  
                return True
            else : return False
        elif a_lig < d_lig:
            if d_lig-a_lig == d_col-a_col:
                for i in range(1, d_lig - a_lig):
                    if plateau[d_lig - i][d_col - i] != " ":
                        return False                    
                return True
            else : return False       
        else : 
            return False    
        

def autorisation_reine(d_col, d_lig, a_col, a_lig):
    
    if autorisation_fou(d_col, d_lig, a_col, a_lig) == True or autorisation_tour(d_col, d_lig, a_col, a_lig) == True:
        return True
    else :
        return False
                

def autorisation_pion_blanc(d_col, d_lig, a_col, a_lig, tour_précédent):

    #prise en passant
    if d_lig == 3 and a_lig == 2:
        if a_col == d_col+1 or a_col == d_col-1:
            if tour_précédent == [1, a_col, 3, a_col]:
                plateau[3][a_col] = " "
                return True
    #coup de base
    if a_lig == d_lig-1: 
        if a_col == d_col and plateau[a_lig][a_col] == ' ':
            return True
        elif a_col == d_col-1 or a_col == d_col+1:
            if plateau[a_lig][a_col] != " ":
                return True                      
        else :
            return False
    #premier coup de 2 cases
    elif d_lig == 6 and a_lig == 4 and plateau[5][a_col] == ' ' and plateau[a_lig][a_col] == ' ':    
        if a_col == d_col:
            return True
            
    else :
        return False
    

def autorisation_pion_noir(d_col, d_lig, a_col, a_lig, tour_précédent):

    if d_lig == 4 and a_lig == 5:
        if a_col == d_col+1 or a_col == d_col-1:
            if tour_précédent == [6, a_col, 4, a_col]:
                plateau[4][a_col] = " "
                return True
            
    if a_lig == d_lig+1:
        if a_col == d_col and plateau[a_lig][a_col] == ' ':
            return True
        elif a_col == d_col+1 or a_col == d_col-1:
            if plateau[a_lig][a_col] != " ":
                return True
        else :
            return False
    
    elif d_lig == 1 and a_lig == 3 and plateau[2][a_col] == ' ' and plateau[a_lig][a_col] == ' ':    
        if a_col == d_col:
            return True
    
    else :
        return False  

#cherche la pièce jouer pour appeler la bonne fonction de vérification
def autorisation_deplacement(d_col, d_lig, a_col, a_lig, tour_précédent):
    
    if plateau[d_lig][d_col] == " ":
        return False

    elif plateau[d_lig][d_col] == "K" or plateau[d_lig][d_col] == "k":
        if autorisation_roi(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False
    
    elif plateau[d_lig][d_col] == "R" or plateau[d_lig][d_col] == "r":
        if autorisation_tour(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False
        
    elif plateau[d_lig][d_col] == "N" or plateau[d_lig][d_col] == "n":
        if autorisation_cavalier(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False

    elif plateau[d_lig][d_col] == "B" or plateau[d_lig][d_col] == "b":
        if autorisation_fou(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False
        
    elif plateau[d_lig][d_col] == "Q" or plateau[d_lig][d_col] == "q":
        if autorisation_reine(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False    
        
    elif plateau[d_lig][d_col] == "P":
        if autorisation_pion_blanc(d_col, d_lig, a_col, a_lig, tour_précédent)==True:
            return True
        else : return False    
        
    elif plateau[d_lig][d_col] == "p":
        if autorisation_pion_noir(d_col, d_lig, a_col, a_lig, tour_précédent)==True:
            return True
        else : return False

    else : return True






def liste_possibilités(tour_précédent, d_lig, d_col):
    
    for i in range(8):
        for j in range(8):
            
            if autorisation_deplacement(d_col, d_lig, i, j, tour_précédent) == True:
                if (plateau[d_lig][d_col].islower() and (plateau[j][i].isupper() or plateau[j][i] == " ")) or (plateau[d_lig][d_col].isupper() and (plateau[j][i].islower() or plateau[j][i] == " ")):
                
                    canv.create_oval(i*coef+coef+(coef/2.5), j*coef+coef+(coef/2.5), (i+1)*coef+coef-(coef/2.5), (j+1)*coef+coef-(coef/2.5), fill = "black")
    
    
    
    
    
    
    
    
    
    


def afficher_arriere_plan(coef):

    txt = canv.create_text(hauteur / 2, 10, text="Echec SANS ALEXANDRE!!!!!!!!", fill=case_blanche)

    canv.create_rectangle(coef-1/4*coef, coef-1/4*coef, 9*coef+1/4*coef, 9*coef+1/4*coef, fill=contour)
    # Dessin des numéro de lignes et colonnes
    a = coef
    i2 = "A"
    for i in range(8, 0, -1):
        txt = canv.create_text(coef-coef/9, int(a + (0.5 * coef)), text=i, fill=case_blanche)
        a += coef
        txt = canv.create_text(int(a - (0.5 * coef)), 9*coef+coef/8, text=i2, fill=case_blanche)
        i2 = chr(ord(i2) + 1)



#affiche les pièces du jeu
def afficher_pièces():
 
    global photo_cavalier
    global photo_fou
    global photo_tour
    global photo_roi
    global photo_reine
    global photo_pion
    global photo_cavalier_blanc
    global photo_fou_blanc
    global photo_tour_blanc
    global photo_roi_blanc
    global photo_reine_blanc
    global photo_pion_blanc


    a = coef
    b = coef
    c = coef + a
    d = coef + a
    for i in range(4):
        a = coef
        c = coef + a
        for j in range(4):
            canv.create_rectangle(a, b, c, d, fill=case_blanche)
            canv.create_rectangle(a + coef, b, c + coef, d, fill=case_noire)
            canv.create_rectangle(a, b + coef, c, d + coef, fill=case_noire)
            canv.create_rectangle(a + coef, b + coef, c + coef, d + coef, fill=case_blanche)
            a += coef * 2
            c += coef * 2
        b += coef * 2
        d += coef * 2

    photo_poney = Image.open("image/cavalier_noir.png")
    photo_poney.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_cavalier = ImageTk.PhotoImage(photo_poney)
    
    photo_einstein = Image.open("image/fou_noir.png")
    photo_einstein.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_fou = ImageTk.PhotoImage(photo_einstein)
    
    photo_jumelle = Image.open("image/tour_noir.png")
    photo_jumelle.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_tour = ImageTk.PhotoImage(photo_jumelle)
    
    photo_king = Image.open("image/roi_noir.png")
    photo_king.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_roi = ImageTk.PhotoImage(photo_king)
    
    photo_queen = Image.open("image/reine_noir.png")
    photo_queen.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_reine = ImageTk.PhotoImage(photo_queen)
    
    photo_pions = Image.open("image/Pion_noir.png")
    photo_pions.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_pion = ImageTk.PhotoImage(photo_pions)
    
    photo_poney_blanc = Image.open("image/Cavalier_blancs.png")
    photo_poney_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_cavalier_blanc = ImageTk.PhotoImage(photo_poney_blanc)
    
    photo_einstein_blanc = Image.open("image/fou_blancs.png")
    photo_einstein_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_fou_blanc = ImageTk.PhotoImage(photo_einstein_blanc)
    
    photo_jumelle_blanc = Image.open("image/tour_blancs.png")
    photo_jumelle_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_tour_blanc = ImageTk.PhotoImage(photo_jumelle_blanc)
    
    photo_king_blanc = Image.open("image/roi_blancs.png")
    photo_king_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_roi_blanc = ImageTk.PhotoImage(photo_king_blanc)
    
    photo_queen_blanc = Image.open("image/reine_blancs.png")
    photo_queen_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_reine_blanc = ImageTk.PhotoImage(photo_queen_blanc)
    
    photo_pions_blanc = Image.open("image/Pion_blancs.png")
    photo_pions_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_pion_blanc = ImageTk.PhotoImage(photo_pions_blanc)


    for i in range(8):
        for j in range(8):
                
            if plateau[i][j] == 'n':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_cavalier)
   
            elif plateau[i][j] == 'b':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_fou)

            elif plateau[i][j] == 'r':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_tour)

            elif plateau[i][j] == 'k':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_roi)

            elif plateau[i][j] == 'q':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_reine)

            elif plateau[i][j] == 'p':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_pion)
                
            elif plateau[i][j] == 'N':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_cavalier_blanc)
   
            elif plateau[i][j] == 'B':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_fou_blanc)

            elif plateau[i][j] == 'R':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_tour_blanc)

            elif plateau[i][j] == 'K':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_roi_blanc)

            elif plateau[i][j] == 'Q':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_reine_blanc)

            elif plateau[i][j] == 'P':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_pion_blanc)



#deplace une pièce à partir de ses positions : colonne, lignes entre 0 et 7
def deplacer_piece(depart, arrivee):

    global tour_blanc
    global tour_précédent
    d_col, d_lig = depart
    a_col, a_lig = arrivee
    piece = plateau[d_lig][d_col]
    
    if plateau[d_lig][d_col] == " ":
        return False
    
    # Vérifier si c'est le tour de la pièce à déplacer
    if (tour_blanc and piece.isupper()) or (not tour_blanc and piece.islower()):
        if autorisation_deplacement(d_col, d_lig, a_col, a_lig, tour_précédent)==True :
            
            vérif_roque(d_col, d_lig, a_col, a_lig)
            piece = plateau[d_lig][d_col]
            plateau[d_lig][d_col] = ' '
            plateau[a_lig][a_col] = piece
            tour_blanc = not tour_blanc# Changer de tour
            tour_précédent = [d_lig, d_col, a_lig, a_col]
            vérif_promotion()



#est censé detecter les clics pour ensuite appeler la fonction de déplacement
def pointeur(event):   
    
    global depart_deplacement_lig
    global depart_deplacement_col
    
    for i in range(1, 9):
        for j in range(1, 9):
                if coef*i<event.x<coef*(i+1) and coef*j<event.y<coef*(j+1):
                    if depart_deplacement_lig == 20:
                        depart_deplacement_lig = j-1
                        depart_deplacement_col = i-1
                        pièce_d = plateau[depart_deplacement_lig][depart_deplacement_col]
                        if (tour_blanc and ((pièce_d.isupper()))) or (not tour_blanc and ((pièce_d.islower()))):
                            canv.create_oval(i*coef+2, j*coef+2, (i+1)*coef-2, (j+1)*coef-2)
                            liste_possibilités(tour_précédent, depart_deplacement_lig, depart_deplacement_col)
                            
                    else :
                        arrivée_deplacement_lig = j-1
                        arrivée_deplacement_col = i-1
                        pièce_a = plateau[arrivée_deplacement_lig][arrivée_deplacement_col]
                        if (tour_blanc and ((pièce_a.islower()) or (pièce_a == " "))) or (not tour_blanc and ((pièce_a.isupper()) or (pièce_a == " "))):
                            deplacer_piece((depart_deplacement_col, depart_deplacement_lig), (arrivée_deplacement_col, arrivée_deplacement_lig))
                        afficher_pièces()
                        roi_blanc_vivant()
                        roi_noir_vivant()
                        if roi_noir_en_échec() == True or roi_blanc_en_échec() == True:
                            canv.create_text(hauteur/2, coef*4.5, text="Echec", font=("Courier", 30), fill="#1A2A3A")

                        depart_deplacement_lig = 20
                        depart_deplacement_col = 20


def changer_de_couleur():
    global case_noire
    global case_blanche
    global arriere_plan
    global contour
    
    if(chang_couleur.cget("text") == 'Mettre en rose'):
        chang_couleur.config(text = 'Mettre en bleu')
        case_noire = "#A10684"
        case_blanche = "#CFA0E9"
        arriere_plan = "#D473D4"
        contour = "#6C0277"
        canv.config(bg=arriere_plan)
        quitter.config(bg=contour)
        chang_couleur.config(bg=contour)
        afficher_arriere_plan(coef)
        afficher_pièces()

        
    else:
        chang_couleur.config(text = 'Mettre en rose')  
        case_noire = "#235A8C"
        arriere_plan = "#2A3A4A"
        case_blanche = "#B4CFEC"
        contour = "#5A6A7A"
        canv.config(bg=arriere_plan)
        quitter.config(bg=contour)
        chang_couleur.config(bg=contour)
        afficher_arriere_plan(coef)
        afficher_pièces()





# Creation de la fenetre et de ses caractéristiques
fenetre = Tk()
fenetre.title("Projet de groupe : Echec SANS ALEXANDRE!!!!!!!!")

# Définition des dimensions de la fenetre en fonction de l'écran
hauteur = int(fenetre.winfo_screenheight() / 1.2)
largeur = int(fenetre.winfo_screenwidth() / 1.2)
fenetre.geometry(f"{largeur}x{hauteur}")
fenetre.maxsize(hauteur, hauteur)

# Creation du canvas pour l'affichage
canv = Canvas(fenetre, width=largeur, height=hauteur, bg=arriere_plan)

#pour detecter les clics avec la fonction pointeur
canv.bind("<Button-1>", pointeur)

canv.pack()

coef = hauteur / 10  #correspond à la taille d'une case du plateau
afficher_arriere_plan(coef)
    
afficher_pièces()

#bouton quitter
quitter = Button(fenetre, text="Quitter", command=fenetre.destroy, bg= "#5A6A7A")
quitter.place(x=int(hauteur - (hauteur / 12)), y=int(hauteur - (coef / 2)))

chang_couleur = Button(fenetre, text="Mettre en rose", command = changer_de_couleur, bg= "#5A6A7A")
chang_couleur.place(x=10, y=int(hauteur - (coef / 2)))


jouer_ordi = Button(fenetre, text="Faire jouer l'ordi", command=coup_ordi, bg= "#5A6A7A")
jouer_ordi.place(x=10, y=10)




promo_Q = Button(fenetre, text="Reine", command=effectuer_promotion_Q, bg= "#5A6A7A")
promo_Q.pack_forget()
promo_T = Button(fenetre, text="Tour", command=effectuer_promotion_T, bg= "#5A6A7A")
promo_T.pack_forget()
promo_F = Button(fenetre, text="Fou", command=effectuer_promotion_F, bg= "#5A6A7A")
promo_F.pack_forget()
promo_C = Button(fenetre, text="Cavalier", command=effectuer_promotion_C, bg= "#5A6A7A")
promo_C.pack_forget()








fenetre.mainloop()