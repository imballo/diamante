from utilita import *
from giocatore import *
from mondo import *

aiuto="""
Le possibili azioni sono:
h, H, aiuto: aiuto
n, N, nord: muovi verso il nord
s, S, sud: muovi verso il sud
e, E, est: muovi verso l'est
o, O, ovest: muovi verso l'ovest
i, I, inventario: mostra inventario
g, G, mangia: guarisci
a, A, attacca: attacca mostro
c, C, commercio: commercia
m, M, mappa: mappa
u, U, usa: usa oggetto
z, Z, ascolta: ascolta
q, Q, uscire: termina l'avventura"""
print("""
Le GO.ZY sono liete di presentarvi questa fantastica avventura.
""")
print("""Che mappa vuoi affrontare:
1) la mappa dello zig zag
2) la mappa della mortalità
3) il labirinto della fantasia

""")
risposta=int(input("Inserisci un numero:"))
if risposta==1:
    nome_mappa='./mappe/g.csv'
elif risposta==2:
    nome_mappa='./mappe/l.csv'
else:
    nome_mappa='./mappe/ap.csv'
mappa = Mappa(nome_mappa)    
risposta=input('\nDifficoltà ridotta (mappa visibile, nemici meno potenti, vita/oro aumentati) (s/n)?')
if risposta=='s' or risposta=='S':
    facile=True
else:
    facile=False
if facile:
    mappa.gioco_facile()
giocatore = Giocatore(mappa)
if facile:
    giocatore.gioco_facile()
print("\nDigita h/H help per ricevere aiuto sui comandi!\n")    
azione=''
while True:                                    #“game loop”
    stanza = mappa.casella_a(giocatore.x,giocatore.y)
    if azione not in ['i','I','inventario','g','G','mangia','u','U','usa','m','M','mappa','c',\
                      'C','commercia','z','Z','ascolta']:
        print(stanza.descrizione())
    if isinstance(stanza, CasellaOro):
        giocatore.raccogli_oro(stanza)
    elif isinstance(stanza, CasellaOggetto):
        giocatore.raccogli_oggetto(stanza)
    elif isinstance(stanza,CasellaFine) or not giocatore.vivo():
        print("\nLa tua avventura finisce qui.\n")
        break        
    azione = input('Azione: ')
    if azione in ['h','H','aiuto']:
        print(aiuto, veloce=True)    
    elif azione in ['n','N','nord'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
        giocatore.muovi_nord()
    elif azione in ['s','S','sud'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
        giocatore.muovi_sud()
    elif azione in ['e','E','est'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
        giocatore.muovi_est()
    elif azione in ['o','O','ovest'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
        giocatore.muovi_ovest()
    elif azione in ['i','I','inventario']:
        giocatore.stampa_inventario()
    elif azione in ['g','G','mangia']:
        giocatore.mangia()
    elif azione in ['u','U','usa']:
        giocatore.usa_oggetto()            
    elif azione in ['m','M','mappa']:
        mappa.mappa_visitata(giocatore)
    elif azione in ['a','A','attacca'] and hasattr(stanza, 'nemico') and stanza.nemico.vivo():
        giocatore.attacco(stanza.nemico)
    elif azione in ['c','C','commercia'] and hasattr(stanza, 'commerciante'):
        stanza.vuoi_commerciare(giocatore)
    elif azione in ['z','Z','ascolta']  and hasattr(stanza, 'cantastorie'):
        stanza.cantastorie.racconta_storia(stanza.storia)
    elif azione in ['q','Q']:
        risposta=input('\nVuoi veramente terminare la partita!\n****Tutti i progressi verranno persi****\n(s/n)')
        if risposta=='s' or risposta=='S':
            break;
    else:
        print('\nAzione non valida!')
    if hasattr(stanza, 'nemico'):
        stanza.nemico.attacco(giocatore)            
    if not stanza.visitata:
        stanza.visitata = True
print("""
Le GO.ZY vi aspettano per la prossima avventura.
""")        
input('Premi un tasto per continuare.')
print(open('./immagini_storie/crediti.txt').read(),veloce=True)                       