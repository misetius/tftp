import socket


ip = "127.0.0.1"
portti = 69
osoite = (ip, portti)

palvelimenSoketti = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
palvelimenSoketti.bind(osoite)

while True:
    data = palvelimenSoketti.recvfrom(516)
    asiakkaan_osoite = data[1]
    print(asiakkaan_osoite)
    sisalto = data[0]
    sisalto = sisalto.decode()
    
    #print(sisalto)
    pyynnonkoodi = data[0][1]
    
    raja = sisalto.find("netascii")
    sisalto = sisalto[2:raja-1]
    #print(pyynnonkoodi)
    
   # print(sisalto)

    #asiakas haluaa lukea tiedoston
    if pyynnonkoodi == 1:
        tiedosto = open(sisalto, "r")
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
                palvelimenSoketti.sendto(datapaketti, asiakkaan_osoite)
                ack = palvelimenSoketti.recv(516)
               # print(ack)
                
                    
                
        #vain yksi paketti  
        else:
            datapaketti = bytearray()
            datapaketti.append(0)
            datapaketti.append(3)
            datapaketti.append(0)
            datapaketti.append(1)
            datapaketti += lahetettava_data
            palvelimenSoketti.sendto(datapaketti, asiakkaan_osoite)
            ack = palvelimenSoketti.recv(516)
           # print(ack)            

    #asiakas haluaa lähettää tiedoston
    elif pyynnonkoodi == 2:
        lahetys_soketti = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        lahetys_soketti.bind(("127.0.0.1", 22992))
        jarjestysnumero = 0
        tiedosto = open(sisalto, "wb")
        ack = bytearray()
        ack.append(0)
        ack.append(4)
        ack.append(0)
        ack.append(jarjestysnumero)
        lahetys_soketti.sendto(ack, asiakkaan_osoite)

        while True:
            jarjestysnumero += 1
            ack = bytearray()
            ack.append(0)
            ack.append(4)
            ack.append(0)
            ack.append(jarjestysnumero)
            
            lahetys_soketti.sendto(ack, asiakkaan_osoite)
            data = lahetys_soketti.recv(600)
            sisalto1 = data[4:]
            
            tiedosto.write(sisalto1)
            print(len(data))
            if len(data) < 516:
                
                break
            
        tiedosto = open(sisalto, "r")
        data = tiedosto.read() 
        #print(data)       


             
    

