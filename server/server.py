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
    
    print(sisalto)
    pyynnonkoodi = data[0][1]
    
    raja = sisalto.find("netascii")
    sisalto = sisalto[2:raja-1]
    
    
    print(sisalto)

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
            osat = len(lahetettava_data) // 512
            print(osat)
            k = 0
            b = 512

            for i in range(0, osat):
                lista.append(lahetettava_data[k:b])
                k += 512
                b += 512
            viimeinenosa = lahetettava_data[k:]
            lista.append(viimeinenosa)
            
            blokin_numero = 1
            for i in lista:
                datapaketti = bytearray()
                datapaketti.append(0)
                datapaketti.append(3)
                datapaketti.append(0)
                datapaketti.append(blokin_numero)
                datapaketti += i
                blokin_numero += 1
                palvelimenSoketti.sendto(datapaketti, asiakkaan_osoite)
                ack = palvelimenSoketti.recv(516)
                print(ack)
                
                    
                
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
            print(ack)            

    #asiakas haluaa luoda tiedoston
    elif pyynnonkoodi == 2:
        pass         
    

