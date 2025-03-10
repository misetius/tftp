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
    lahetattava_kuittaus = bytearray()
    lahetattava_kuittaus.append(0)
    lahetattava_kuittaus.append(4)
    lahetattava_kuittaus.append(0)
    lahetattava_kuittaus.append(blokki)
    print(f"Lähetetty kuittaus: {lahetattava_kuittaus}")
    
    soketti.sendto(lahetattava_kuittaus, osoite)



def laheta_tiedosto(tiedostonnimi):
    wrq = bytearray()
    wrq.append(0)
    wrq.append(2)
    tiedostonnimi = tiedostonnimi.encode("utf-8")
    wrq += tiedostonnimi
    wrq.append(0)
    netascii = bytearray(b"netascii")
    wrq += netascii
    wrq.append(0)

    soketti.sendto(wrq, osoite)
    ack = soketti.recvfrom(600)
    uusiosoite = ack[1]
    print(f"Palvelimen uusiosoite, jossa uusi porttinumero {uusiosoite}")

    tiedosto = open(tiedostonnimi, "r")
    lahetettava_data = tiedosto.read()

    lahetettava_data = lahetettava_data.encode("utf-8")
        
        

    datapaketti = bytearray()
    datapaketti.append(0)
    datapaketti.append(3)
    datapaketti.append(0)
    datapaketti.append(1)
    lista = []


        #useampi paketti
    if len(lahetettava_data) > 512:

        k = 512
        osat = [lahetettava_data[i:i+k] for i in range(0, len(lahetettava_data), k)]


            
        blokin_numero = 1
        for i in osat:
            datapaketti = bytearray()
            datapaketti.append(0)
            datapaketti.append(3)
            datapaketti.append(0)
            datapaketti.append(blokin_numero)
            datapaketti += i
            blokin_numero += 1
            print(len(datapaketti))
            soketti.sendto(datapaketti, uusiosoite)
            ack = soketti.recv(516)
            print(f"Palvelimen lähettämä kuittaus: {ack}")
                
                    
                
        #vain yksi paketti  
    else:
        print("yksi paketti")
        datapaketti = bytearray()
        datapaketti.append(0)
        datapaketti.append(3)
        datapaketti.append(0)
        datapaketti.append(1)
        datapaketti += lahetettava_data
        soketti.sendto(datapaketti, uusiosoite)
        ack = soketti.recv(516)
        print(f"Palvelimen lähettämä kuittaus: {ack}")           


lahetysvailataus = input("Haluatko ladata(la) tiedoston vai lähettää(lä) tiedoston: ")

if lahetysvailataus == "la":
    tiedostonnimi = input("Anna tiedoston tarkka nimi: ")
    luetiedosto(tiedostonnimi)

if lahetysvailataus == "lä":
    tiedostonnimi = input("Anna tiedoston tarkka nimi: ")
    laheta_tiedosto(tiedostonnimi)

print("Kiitos ohjelman käytöstä.")




