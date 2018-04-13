#test class
from giocatore import *
from mondo import *
from oggetti import *
from personaggi import *

def findsubclass(baseclass, indent=0):
    if indent == 0:
        print ("Subclasses of %s are:" % baseclass.__name__)
    indent = indent + 1
    for c in baseclass.__subclasses__():
        print ("-"*indent*4 + ">" + c.__name__)
        findsubclass(c, indent)
        
def listsubclass(baseclass, cl):
    cl.append(baseclass.__name__)
    for c in baseclass.__subclasses__():
        listsubclass(c, cl)
        
def test_oggetto():
    classi=[]
    listsubclass(Oggetto,classi)
    for classe in classi:
        try:
            tmp=eval(classe)()
            print("Gli oggetti %s hanno:" % eval(classe).__name__)
            print("  nome: %s" % tmp.nome)
            print("  descrizione: %s"% tmp.descrizione)            
            print("  prezzo: %d" % tmp.prezzo)
            if hasattr(tmp,'danno'):
                print("  danno: %d" % tmp.danno)
            if hasattr(tmp,'recupero'):
                print("  recupero: %d" % tmp.recupero)                
        except TypeError:
            pass

def test_personaggi(test_attacco=False):
    classi=[]
    listsubclass(Personaggio,classi)
    for classe in classi:
        try:
            tmp=eval(classe)()
            print("Gli oggetti %s hanno:" % eval(classe).__name__)
            print("  str: %s" % tmp)
            print("  nome: %s" % tmp.nome)
            if hasattr(tmp,'descrizione_vivo'):
                print("  descrizione_vivo: %s" % tmp.descrizione_vivo.strip())
            if hasattr(tmp,'descrizione_morto'):
                print("  descrizione_morto: %s" % tmp.descrizione_morto.strip())                
            if hasattr(tmp,'danno'):
                print("  danno: %d" % tmp.danno)
            if hasattr(tmp,'oro'):
                print("  oro: %d" % tmp.oro)
            if hasattr(tmp,'vita'):
                print("  vita: %d" % tmp.vita)
            if hasattr(tmp,'racconta_storia'):
                print('  storia:')
                tmp.racconta_storia()                    
            if hasattr(tmp,'inventario'):
                print("  inventario: ")
                for oggetto in tmp.inventario:
                    print("    %s" % oggetto)
            if hasattr(tmp,'attacco') and test_attacco:
                print("  attacco:")
                tmpMappa=Mappa()
                tmpgiocatore=Giocatore(tmpMappa)
                while tmpgiocatore.vita>0:
                    tmp.attacco(tmpgiocatore)
        except TypeError:
            pass

def test_mondo(test_descrizione=False):
    classi=[]
    listsubclass(CasellaMappa,classi)
    for classe in classi:
        try:
            tmp=eval(classe)()
            print("Gli oggetti %s hanno:" % eval(classe).__name__)
            print("  str: %s" % tmp)
            if hasattr(tmp,'nome'):
                print("  nome: %s" % tmp.nome)
            if hasattr(tmp,'descrizione') and test_descrizione:
                print("  descrizione da visitare: %s" % tmp.descrizione())
                tmp.visitata=True
                print("  descrizione visitata: %s" % tmp.descrizione())
            if hasattr(tmp,'oro'):
                print("  oro: %d" % tmp.oro)
            if hasattr(tmp,'oggetti'):
                print("  oggetto: ")
                for oggetto in tmp.oggetti:
                    print("    %s" % oggetto)
            if hasattr(tmp,'attacco') and test_attacco:
                print("  attacco:")
                tmpMappa=Mappa()
                tmpgiocatore=Giocatore(tmpMappa)
                while tmpgiocatore.vita>0:
                    tmp.attacco(tmpgiocatore)
        except TypeError:
            pass        

#test_oggetto()
#test_personaggi()
test_mondo()