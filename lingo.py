#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 11:23:52 2021

@author: Emeline
"""

import random
import tkinter as tk

# load list of words frome file
fichier = open("dico.txt", "r")
words2 = fichier.readlines()           
fichier.close()
# Remove the character '\n'
words=[word.rstrip( ) for word in words2]
# load list of words
with open('dico.txt') as f:
    frenchWords=f.readlines()
with open('ukenglish.txt') as f:
    englishWords=f.readlines()

listFrenchWords=[word.strip('\n').upper() for word in frenchWords]
listEnglishWords=[word.strip('\n').upper() for word in englishWords]

#global variables
lgMotus=7
languages=['english','french']
currentLanguage="english"
dic={'english':listEnglishWords,'french':listFrenchWords} 
OKnb=0
TotalNb=0
############################################################################
# Functions
############################################################################

# Reinitiate the global variables
def reinit():
    global mot,attemptsNb,lettersOK,motTrouve
    motTrouve=False
    attemptsNb=0
    mot=[]
    lettersOK=[]
    for count in range(lgMotus*6):
        labChar[count].configure(text='_',fg='black')
    labError.configure(text=' ')

# Display
def show(currentWord,i,couleur):
    global attemptsNb
    rowId=lgMotus*(attemptsNb+i)
    if attemptsNb+i<6:
        for count in range(len(motus)):
            labChar[rowId+count].configure(text=currentWord[count],fg=couleur)
       
# This function returns the word to be guess (wTG)
def chooseWord(length):
    global currentLanguage
    words=dic[currentLanguage]
    wordCharNb=[word for word in words if len(word) ==length] 
    wTG=wordCharNb[random.randint(0,len(wordCharNb))] 
    return wTG

# Returns a dictionnary from a string with the occurence of characters (key=letter and value = occurence)
def occurenceCharacters(wordInput):
    word=wordInput.upper()
    dicOccurence={}
    for char in word:
        if char in dicOccurence:
            dicOccurence[char]+=1
        else:
            dicOccurence[char]=1
    return dicOccurence

def delete():
    labError.configure(text='')

# Reads the proposal from the entry box
def play():
    global lgMotus,attemptsNb,motTrouve
    if attemptsNb<7 and not motTrouve:
        proposal=entry.get()
        if len(proposal)==lgMotus:
            show(proposal,0,'black')
            if proposal in words:
                window.after(1000,check)
            else:
                show(proposal,0,'black')
                labError.configure(text="Unknown word",fg='red')
                attemptsNb+=1
                show(lettersOK,0,'blue')
                window.after(1500,delete)
                if attemptsNb==6:
                    window.after(1500,answer)
        else:
            labError.configure(text="Inadequate length",fg='red')
            attemptsNb+=1
            show(lettersOK,0,'blue')
            window.after(1000,delete)
            if attemptsNb==6:
                    window.after(500,answer)
                    window.after(1500,game)

# 
def check():
    global lgMotus,motus,mot,lettersOK,attemptsNb,motTrouve,OKnb
    proposal=entry.get()
    dic=occurenceCharacters(motus)
    dicProposal=occurenceCharacters(proposal)
    motTrouve=True
    for count,charMotus in enumerate(motus):
        letter=proposal[count].upper()
        dicProposal[letter]-=1  
        if letter==charMotus:
            mot[count]=charMotus
            lettersOK[count]=charMotus
            dic[letter]-=1
            labChar[lgMotus*(attemptsNb)+count].configure(text=letter,fg='green')
        elif letter in dic and dic[letter]>0 and dicProposal[letter]<dic[letter]:
            mot[count]=letter.lower()
            dic[letter]-=1  
            labChar[lgMotus*(attemptsNb)+count].configure(text=letter,fg='red')
            motTrouve=False
        else:
            mot[count]='_'
            motTrouve=False
    attemptsNb+=1
    if motTrouve:
        OKnb+=1
        lab_OKnb.configure(text=str(OKnb))
        window.after(1500,game)
    else:
        show(lettersOK,0,'blue')
    if attemptsNb==6:
        window.after(500,answer)
        window.after(1500,game)
    
# Shows the correct answer
def answer():
    global attemptsNb
    attemptsNb=6
    show(motus,-1,'green')
    window.after(1500,game)
    
# Motus game 
def game():
    global lgMotus,motus,mot,attemptsNb,lettersOK,motTrouve,TotalNb
    TotalNb+=1
    lab_TotalNb.configure(text=str(TotalNb))
    reinit()
    motus=chooseWord(lgMotus)
    mot.append(motus[0])
    lettersOK.append(motus[0])
    for i in range(lgMotus-1):
        mot.append('_')
        lettersOK.append('_')
    show(lettersOK,0,'blue')
    
def playFrench():
    '''
    Launches a new game with languages settings = french 

    Returns
    -------
    None.

    '''
    global currentLanguage
    currentLanguage='french'
    newGame()
 
def playEnglish():
    '''
    Launches a new game with languages settings =english

    Returns
    -------
    None.

    '''
    global currentLanguage
    currentLanguage='english'
    newGame()  

def newGame():
    '''
    Lauches a new game after reset of game statistics

    Returns
    -------
    None.

    '''    
    global TotalNb,OKnb
    TotalNb=0
    OKnb=0
    game()
############################################################################
# Graphics window
############################################################################
window = tk.Tk()
window.title("LINGO")

top = tk.Menu(window)
window.config(menu=top)
jeu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Game', menu=jeu)
jeu.add_command(label='New game', command=newGame)
jeu.add_command(label='Close', command=window.destroy)
settings = tk.Menu(top, tearoff=False)
top.add_cascade(label='Language', menu=settings)
settings.add_command(label='English', command=playEnglish)
settings.add_command(label='French', command=playFrench)
############################################################################
# Labels
############################################################################
# Info message

# Error message
labError=tk.Label(window,text='')
labError.grid(row=2,column=0)

# Motus grid
labChar=[]
for i in range(lgMotus*6):
    labChar.append(tk.Label(window,text='_',font=("Helvetica", 25)))
for count in range(lgMotus*6):
    labChar[count].grid(row=1+count//lgMotus, column=3+count%lgMotus)

# Statistics
lab_text_TotalNb=tk.Label(window,text='Played games',font=("Helvetica", 15))
lab_text_TotalNb.grid(row=2,column=17)
lab_TotalNb=tk.Label(window,text=0,font=("Helvetica", 15))
lab_TotalNb.grid(row=3,column=17)


lab_text_OKnb=tk.Label(window,text='Found words',font=("Helvetica", 15))
lab_text_OKnb.grid(row=4,column=17)
lab_OKnb=tk.Label(window,text=0,font=("Helvetica", 15))
lab_OKnb.grid(row=5,column=17)

############################################################################
# Entry box
############################################################################
# Entry box for the player
entry=tk.Entry()
entry.grid(row=0,column=0)

############################################################################
# Buttons
############################################################################
but_Enter=tk.Button(window,text="Enter",command=play)
but_Enter.grid(row=1,column=0)


but_Answer=tk.Button(window,text="Solution",command=answer)
but_Answer.grid(row=5,column=0)

############################################################################
# Start-up
############################################################################
#random.seed(6)
game()
window.mainloop()
