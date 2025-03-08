import socket

DATANPITUUS = 516

soketti = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
osoite = ('127.0.0.1', 69)

def luetiedosto(tiedoston_nimi):
    paketti = bytearray()
    paketti.append(0)
    paketti.append(1)
    tiedoston_nimi = tiedoston_nimi.encode("utf-8")
    paketti += tiedoston_nimi
    paketti.append(0)
    netascii = bytearray(b"netascii")
    paketti += netascii
    paketti.append(0)
    print(paketti)

    osoite = ('127.0.0.1', 69)

    soketti.sendto(paketti, osoite)
    tiedosto = open(tiedoston_nimi, "wb")
    while True:
        data, osoite = soketti.recvfrom(600)
        laheta_kuittaus(data[:4], osoite)
        sisalto = data[4:]
        print(sisalto)
        tiedosto.write(sisalto)

        if len(data) < DATANPITUUS:
           break

def laheta_kuittaus(blokkikoodi, osoite):
    
    blokki = blokkikoodi[3]
    print(blokki)
    lahetattava_kuittaus = bytearray()
    lahetattava_kuittaus.append(0)
    lahetattava_kuittaus.append(4)
    lahetattava_kuittaus.append(0)
    lahetattava_kuittaus.append(blokki)
    
    soketti.sendto(lahetattava_kuittaus, osoite)

luetiedosto("lyhyempiteksti.txt")



