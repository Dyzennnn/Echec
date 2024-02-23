from tkinter import *
import tkinter as tk
import os.path as OP
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename


# Définition du plateau d'échecs sous forme de liste de listes
plateau = [
    ['t', 'c', 'f', 'q', 'k', 'f', 'c', 't'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['T', 'C', 'F', 'Q', 'K', 'F', 'C', 'T']
]

# Variable pour suivre le tour actuel
tour_blanc = True
tour_précédent = []

#pour la fonction pointeur qui detecte les clics
depart_deplacement_lig = 20
depart_deplacement_col = 20

arriere_plan = "#2A3A4A"
case_blanche = "#B4CFEC"
case_noire = "#235A8C"



def roi_blanc_vivant():
    
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == "K":
                return True
    canv.create_text(hauteur/2, hauteur/2, text="Echec et mat Noirs", font=("Courier", 30), fill="#1A2A3A")

 
def roi_noir_vivant():
    
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == "k":
                return True
    canv.create_text(hauteur/2, hauteur/2, text="LES BLANCS ONT BATTU LES NOIRS", font=("Courier", 30), fill="#1A2A3A")
    canv.create_rectangle(j*coef+1.5, j*coef+1.5, largeur, hauteur, fill="#E0E0E0")











#Verifier pour chaque pièces si le coup est règlementaire

def autorisation_roi(d_col, d_lig, a_col, a_lig):
    
    if a_lig == d_lig+1 and a_col == d_col+1:
        return True
    elif a_lig == d_lig+1 and a_col == d_col:
        return True
    elif a_lig == d_lig+1 and a_col == d_col-1:
        return True    
    elif a_lig == d_lig and a_col == d_col+1:
        return True
    elif a_lig == d_lig and a_col == d_col-1:
        return True    
    elif a_lig == d_lig-1 and a_col == d_col+1:
        return True
    elif a_lig == d_lig-1 and a_col == d_col:
        return True    
    elif a_lig == d_lig-1 and a_col == d_col-1:
        return True
    
    #pour le roque :
    elif plateau[d_lig][d_col] == "K":
        if a_lig == 7 and a_col == 2 and plateau[7][0] == "T" and plateau[7][1] == " " and plateau[7][2] == " " and plateau[7][3] == " ":  
            piece2 = plateau[7][0]
            plateau[7][0] = ' '
            plateau[7][3] = piece2            
            return True
        elif a_lig == 7 and a_col == 6 and plateau[7][7] == "T" and plateau[7][6] == " " and plateau[7][5] == " ":
            piece2 = plateau[7][7]
            plateau[7][7] = ' '
            plateau[7][5] = piece2            
            return True
    elif plateau[d_lig][d_col] == "k":
        if a_lig == 0 and a_col == 2 and plateau[0][0] == "t" and plateau[0][1] == " " and plateau[0][2] == " " and plateau[0][3] == " ":
            piece2 = plateau[0][0]
            plateau[0][0] = ' '
            plateau[0][3] = piece2            
            return True
        elif a_lig == 0 and a_col == 6 and plateau[0][7] == "t" and plateau[0][6] == " " and plateau[0][5] == " ":
            piece2 = plateau[0][7]
            plateau[0][7] = ' '
            plateau[0][5] = piece2            
            return True
    
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
                for i in range(1, a_lig - d_lig):  
                    if plateau[d_lig + i][d_col + i] != " ":
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
            if d_lig == 1:
                plateau[d_lig][d_col] = "Q"
                return True
            return True
        elif a_col == d_col-1 or a_col == d_col+1:
            if plateau[a_lig][a_col] != " ":
                if d_lig == 1:
                    plateau[d_lig][d_col] = "Q"
                    return True
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
            if d_lig == 6:
                plateau[d_lig][d_col] = "q"
                return True
            return True
        elif a_col == d_col+1 or a_col == d_col-1:
            if plateau[a_lig][a_col] != " ":
                if d_lig == 6:
                    plateau[d_lig][d_col] = "q"
                    return True
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
    
    elif plateau[d_lig][d_col] == "T" or plateau[d_lig][d_col] == "t":
        if autorisation_tour(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False
        
    elif plateau[d_lig][d_col] == "C" or plateau[d_lig][d_col] == "c":
        if autorisation_cavalier(d_col, d_lig, a_col, a_lig)==True:
            return True
        else : return False

    elif plateau[d_lig][d_col] == "F" or plateau[d_lig][d_col] == "f":
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

    photo_poney = Image.open("Cavalier.png")
    photo_poney.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_cavalier = ImageTk.PhotoImage(photo_poney)
    
    photo_einstein = Image.open("fou_noir.png")
    photo_einstein.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_fou = ImageTk.PhotoImage(photo_einstein)
    
    photo_jumelle = Image.open("tour_noir.png")
    photo_jumelle.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_tour = ImageTk.PhotoImage(photo_jumelle)
    
    photo_king = Image.open("roi_noir.png")
    photo_king.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_roi = ImageTk.PhotoImage(photo_king)
    
    photo_queen = Image.open("reine_noir.png")
    photo_queen.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_reine = ImageTk.PhotoImage(photo_queen)
    
    photo_pions = Image.open("Pion_noir.png")
    photo_pions.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_pion = ImageTk.PhotoImage(photo_pions)
    
    photo_poney_blanc = Image.open("Cavalier_blanc.png")
    photo_poney_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_cavalier_blanc = ImageTk.PhotoImage(photo_poney_blanc)
    
    photo_einstein_blanc = Image.open("fou_blanc.png")
    photo_einstein_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_fou_blanc = ImageTk.PhotoImage(photo_einstein_blanc)
    
    photo_jumelle_blanc = Image.open("tour_blanc.png")
    photo_jumelle_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_tour_blanc = ImageTk.PhotoImage(photo_jumelle_blanc)
    
    photo_king_blanc = Image.open("roi_blanc.png")
    photo_king_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_roi_blanc = ImageTk.PhotoImage(photo_king_blanc)
    
    photo_queen_blanc = Image.open("reine_blanc.png")
    photo_queen_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_reine_blanc = ImageTk.PhotoImage(photo_queen_blanc)
    
    photo_pions_blanc = Image.open("Pion_blanc.png")
    photo_pions_blanc.thumbnail((9/10*coef, 9/10*coef), Image.BICUBIC)
    photo_pion_blanc = ImageTk.PhotoImage(photo_pions_blanc)


    for i in range(8):
        for j in range(8):
                
            if plateau[i][j] == 'c':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_cavalier)
   
            elif plateau[i][j] == 'f':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_fou)

            elif plateau[i][j] == 't':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_tour)

            elif plateau[i][j] == 'k':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_roi)

            elif plateau[i][j] == 'q':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_reine)

            elif plateau[i][j] == 'p':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_pion)
                
            elif plateau[i][j] == 'C':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_cavalier_blanc)
   
            elif plateau[i][j] == 'F':
                canv.create_image(j*coef + 1.5 * coef, i*coef + 1.5 * coef, image=photo_fou_blanc)

            elif plateau[i][j] == 'T':
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
        if autorisation_deplacement(d_col, d_lig, a_col, a_lig, tour_précédent)==True:
            
            piece = plateau[d_lig][d_col]
            plateau[d_lig][d_col] = ' '
            plateau[a_lig][a_col] = piece
            tour_blanc = not tour_blanc# Changer de tour
            tour_précédent = [d_lig, d_col, a_lig, a_col]


#if (tour_blanc and ((pièce_a.islower()) or (pièce_a == " "))) or (not tour_blanc and ((pièce_a.islower()) or (pièce_a == " "))):


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
                        canv.create_oval(i*coef+2, j*coef+2, (i+1)*coef-2, (j+1)*coef-2)
                    else :
                        arrivée_deplacement_lig = j-1
                        arrivée_deplacement_col = i-1
                        pièce_a = plateau[arrivée_deplacement_lig][arrivée_deplacement_col]
                        if (tour_blanc and ((pièce_a.islower()) or (pièce_a == " "))) or (not tour_blanc and ((pièce_a.isupper()) or (pièce_a == " "))):
                            deplacer_piece((depart_deplacement_col, depart_deplacement_lig), (arrivée_deplacement_col, arrivée_deplacement_lig))
                        afficher_pièces()
                        roi_blanc_vivant()
                        roi_noir_vivant()
                        depart_deplacement_lig = 20
                        depart_deplacement_col = 20


def changer_de_couleur():
    global case_noire
    global case_blanche
    global arriere_plan
    
    if(chang_couleur.cget("text") == 'Mettre en rose'):
        chang_couleur.config(text = 'Mettre en bleu')
        case_noire = "#9d8189"
        case_blanche = "#ffcad4"
        arriere_plan = "#d8e2dc"
        afficher_pièces()
    else:
        chang_couleur.config(text = 'Mettre en rose')  
        case_noire = "#235A8C"
        arriere_plan = "#2A3A4A"
        case_blanche = "#B4CFEC"
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


txt = canv.create_text(hauteur / 2, 10, text="Echec SANS ALEXANDRE!!!!!!!!", fill=arriere_plan)


# Dessin du plateau

coef = hauteur / 10  #correspond à la taille d'une case du plateau

canv.create_rectangle(coef-1/4*coef, coef-1/4*coef, 9*coef+1/4*coef, 9*coef+1/4*coef, fill="#5A6A7A")


# Dessin des numéro de lignes et colonnes
a = coef
i2 = "A"
for i in range(8, 0, -1):
    txt = canv.create_text(coef-coef/9, int(a + (0.5 * coef)), text=i, fill=case_blanche)
    a += coef
    txt = canv.create_text(int(a - (0.5 * coef)), 9*coef+coef/8, text=i2, fill=case_blanche)
    i2 = chr(ord(i2) + 1)
    
afficher_pièces()

#bouton quitter
quitter = Button(fenetre, text="Quitter", command=fenetre.destroy)
quitter.place(x=int(hauteur - (hauteur / 12)), y=int(hauteur - (coef / 2)))

chang_couleur = Button(fenetre, text="Mettre en rose", command = changer_de_couleur)
chang_couleur.place(x=10, y=int(hauteur - (coef / 2)))

fenetre.mainloop()

