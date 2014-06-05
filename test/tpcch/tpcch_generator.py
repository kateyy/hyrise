import random
import string
import sys
import time
import os

class TpcchGenerator:
    def __init__(self, scaleFactor=1, path=""):
        self.__scaleFactor = scaleFactor
        self.__path = path
        self.__olCNT = []
        self.__entryD = []

        self.__regionList = ['AFRICA','AMERICA','ASIA','EUROPE','MIDDLE EAST']
        self.__nationList = ['ALGERIA','ARGENTINA','BRAZIL','CANADA','EGYPT','ETHIOPIA',
            'FRANCE','GERMANY','INDIA','INDONESIA','IRAN','IRAQ','JAPAN','JORDAN',
            'KENYA','MOROCCO','MOZAMBIQUE','PERU','CHINA','ROMANIA','SAUDI ARABIA',
            'VIETNAM','RUSSIA','UNITED KINGDOM','UNITED STATES',
            'SPAIN','BELARUS','COLOMBIA','MONGOLIA','SWEDEN','BOLIVIA','ICELAND',
            'CHILE','ANGOLA','ZAMBIA','IRAN','YEMEN','NIGERIA','POLAND','ITALY',
            'FINLAND','THAILAND','PAKISTAN','NORTHKOREA','SOUTHKOREA','MALI',
            'NIGER','CHAD','PARAGUAY','URUGUAY','VENEZUELA','MEXICO','LATVIA',
            'NORWAY','ESTONIA','NETHERLANDS','TANZANIA','UGANDA','ISRAEL','SYRIA',
            'PANAMA','LAOS']
        self.__nationRegionList = ['0','1','1','1','4','0','3','3','2','2','4','4','2',
            '4','0','0','0','1','2','3','4','2','3','3','1','3','4','1','2','3','1','3',
            '1','0','0','4','4','0','3','3','3','2','2','2','2','0','0','0','1','1','1',
            '1','3','3','3','3','0','0','4','4','1','2']
        self.__nounList = ['foxes','ideas','theodolites','pinto beans',
            'instructions','dependencies','excuses','platelets',
            'asymptotes','courts','dolphins','multipliers','sauternes',
            'warthogs','frets','dinos','attainments','somas',
            'Tiresias\'','patterns','forges','braids','hockey players',
            'frays','warhorses','dugouts','notornis','epitaphs',
            'pearls','tithes','waters','orbits','gifts','sheaves',
            'depths','sentiments','decoys','realms','pains','grouches',
            'escapades']
        self.__verbList = ['sleep','wake','are','cajole','haggle','nag','use',
            'boost','affix','detect','integrate','maintain','nod','was',
            'lose','sublate','solve','thrash','promise','engage',
            'hinder','print','x-ray','breach','eat','grow','impress',
            'mold','poach','serve','run','dazzle','snooze','doze',
            'unwind','kindle','play','hang','believe','doubt']
        self.__adjectiveList = ['furious','sly','careful','blithe','quick',
            'fluffy','slow','quiet','ruthless','thin','close','dogged',
            'daring','brave','stealthy','permanent','enticing','idle',
            'busy','regular','final','ironic','even','bold','silent']
        self.__adverbList = ['sometimes','always','never','furiously','slyly',
            'carefully','blithely','quickly','fluffily','slowly','quietly',
            'ruthlessly','thinly','closely','doggedly','daringly','bravely',
            'stealthily','permanently','enticingly','idly','busily',
            'regularly','finally','ironically','evenly','boldly','silently']
        self.__prepositionList =['about','above','according to','across','after',
            'against','along','alongside of','among','around','at','atop',
            'before','behind','beneath','beside','besides','between','beyond',
            'by','despite','during','except','for','from','in place of','inside',
            'instead of','into','near','of','on','outside','over','past','since',
            'through','throughout','to','toward','under','until','up','upon',
            'without','with','within']
        self.__auxList = ['do','may','might','shall','will','would','can','could',
            'should','ought to','must','will have to','shall have to',
            'could have to','should have to','must have to','need to','try to']
        self.__termList = ['.',';',':','?','!','--']
        self.__lastNameList = ['BAR','OUGHT','ABLE','PRI','PRES','ESE','ANTI',
            'CALLY','ATION','EING']

    def do(self):
        self.start()

    def __printOutProgress(self,startProgress,endProgress,relativeProgress):
        progress = startProgress+ (endProgress-startProgress)*relativeProgress
        output = "Progress: {:10.1f}".format(progress*100)
        if output[-1:] == "0":
            sys.stdout.write(output[:-2]+'%  \r')
        else:
            sys.stdout.write(output+'%\r')
        sys.stdout.flush()

    def start(self):
        self.__createRegion(0.0,1/12.0)
        self.__createNation(1/12.0,2/12.0)
        self.__createSupplier(2/12.0,3/12.0)
        self.__createItem(3/12.0,4/12.0)
        self.__createWarehouse(4/12.0,5/12.0)
        self.__createStock(5/12.0,6/12.0)
        self.__createDistrict(6/12.0,7/12.0)
        self.__createCustomer(7/12.0,8/12.0)
        self.__createHistory(8/12.0,9/12.0)
        self.__createOrder(9/12.0,10/12.0)
        self.__createOrderline(10/12.0,11/12.0)
        self.__createNewOrder(11/12.0,1.0)

    def __randomString(self,min,max):
        length = random.randint(min,max)
        return "".join(random.choice(string.ascii_letters) for x in xrange(length))

    def __textString(self,min,max):
        result = ''
        while len(result) < max :
            result += ' '+self.__text()

        length = random.randint(min,max)
        start = random.randint(0,len(result)-length)
        return result[start:start+length]


    def __text(self):
        if random.randint(0,1) == 0:
            return self.__sentence()
        else:
            return self.__text()+' '+self.__sentence()

    def __sentence(self):
        choice = random.randint(0,4)

        if choice == 0:
            return self.__nounPhrase()+' '+self.__verbPhrase()+self.__terminator()
        elif choice == 1:
            return self.__nounPhrase()+' '+self.__verbPhrase()+' '+self.__prepositionalPhrase()+self.__terminator()
        elif choice == 2:
            return self.__nounPhrase()+' '+self.__verbPhrase()+' '+self.__nounPhrase()+self.__terminator()
        elif choice == 3:
            return self.__nounPhrase()+' '+self.__prepositionalPhrase()+' '+self.__verbPhrase()+' '+self.__nounPhrase()+self.__terminator()
        else:
            return self.__nounPhrase()+' '+self.__prepositionalPhrase()+' '+self.__verbPhrase()+' '+self.__prepositionalPhrase()+self.__terminator()

    def __nounPhrase(self):
        choice = random.randint(0,3)

        if choice == 0:
            return self.__noun()
        elif choice == 1:
            return self.__adjective()+' '+self.__noun()
        elif choice == 2:
            return self.__adjective()+' and '+self.__adjective()+' '+self.__noun()
        else:
            return self.__adverb()+' '+self.__adjective()+' '+self.__noun()

    def __verbPhrase(self):
        choice = random.randint(0,3)

        if choice == 0:
            return self.__verb()
        elif choice == 1:
            return self.__auxiliary()+' '+self.__verb()
        elif choice == 2:
            return self.__verb()+', '+self.__adverb()
        else:
            return self.__auxiliary()+' '+self.__verb()+' '+self.__adverb()

    def __prepositionalPhrase(self):
        return self.__preposition()+' the '+self.__nounPhrase()

    def __noun(self):
        choice = random.randint(0,40)
        return self.__nounList[choice]

    def __verb(self):
        choice = random.randint(0,39)
        return self.__verbList[choice]

    def __adjective(self):
        choice = random.randint(0,24)
        return self.__adjectiveList[choice]

    def __adverb(self):
        choice = random.randint(0,27)
        return self.__adverbList[choice]

    def __preposition(self):
        choice = random.randint(0,46)
        return self.__prepositionList[choice]

    def __auxiliary(self):
        choice = random.randint(0,17)
        return self.__auxList[choice]

    def __terminator(self):
        choice = random.randint(0,5)
        return self.__termList[choice]


    def __createRegion(self,startProgress,endProgress):
        regionHeaderFile = open(self.__path + 'region_header.tbl', 'w')
        regionHeaderFile.write('R_REGIONKEY|R_NAME|R_COMMENT\n')
        regionHeaderFile.write('INTEGER|STRING|STRING\n')
        regionHeaderFile.write('0_R|0_R|0_R')
        regionHeaderFile.close()

        self.__printOutProgress(startProgress,endProgress,0.0)
        regionContentFile = open(self.__path + 'region.csv', 'w')
        for region in range(5):
            name = self.__regionList[region]
            comment = self.__textString(31,115)

            regionContentFile.write(
                str(region)+','
                +name+','
                +comment+'\n')
        regionContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createNation(self,startProgress,endProgress):
        nationHeaderFile = open(self.__path + 'nation_header.tbl', 'w')
        nationHeaderFile.write('N_NATIONKEY|N_NAME|N_REGIONKEY|N_COMMENT\n')
        nationHeaderFile.write('INTEGER|STRING|INTEGER|STRING\n')
        nationHeaderFile.write('0_R|0_R|0_R|0_R')
        nationHeaderFile.close()

        self.__printOutProgress(startProgress,endProgress,0.0)

        nationContentFile = open(self.__path + 'nation.csv', 'w')
        for nation in range(62):
            if nation == 31:
                self.__printOutProgress(startProgress,endProgress,0.5)
            comment = self.__textString(31,114)
            nationContentFile.write(
                str(nation)+','
                +self.__nationList[nation]+','
                +self.__nationRegionList[nation]+','
                +comment+'\n')

        nationContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __stringAppendNumber(self,s,n,minDigits):
        nString = str(n)
        result = s + '#'
        if minDigits > len(nString):
            for i in range(minDigits-len(nString)):
                result += '0'

        return result+nString

    def __phoneNumber(self,id):
        result = str(id+10)
        result += '-'+str(random.randint(100,999))
        result += '-'+str(random.randint(100,999))
        result += '-'+str(random.randint(1000,9999))
        return result

    def __supplierComment(self,case):
        result = self.__randomString(25,100)

        if case == 0:
            firstString = 'Customer'
            secondsString = 'Recommends'
        elif case == 1:
            firstString = 'Customer'
            secondsString = 'Complaints'
        else:
            firstString = ''
            secondsString = ''

        wildcard = self.__randomString(0,len(result)-len(firstString+secondsString))
        insertion = firstString+wildcard+secondsString

        position = random.randint(0,len(result)-len(insertion))
        result = result[0:position]+insertion+result[position+len(insertion):]
        return result

    def __createSupplier(self,startProgress,endProgress):
        supplierHeaderFile = open(self.__path + 'supplier_header.tbl', 'w')
        supplierHeaderFile.write('SUP_SUPPKEY|SUP_NAME|SUP_ADDRESS|SUP_NATIONKEY|SUP_PHONE|SUP_ACCTBAL|SUP_COMMENT\n')
        supplierHeaderFile.write('INTEGER|STRING|STRING|INTEGER|STRING|FLOAT|STRING\n')
        supplierHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        supplierHeaderFile.close()

        supplierContentFile = open(self.__path + 'supplier.csv', 'w')
        suppliers = 10000

        recommendations = []
        while len(recommendations)<suppliers/2000:
            num = random.randint(0,suppliers-1)
            if not (num in recommendations):
                recommendations.append(num)
        recommendations = sorted(recommendations)

        complaints = []
        while len(complaints)<suppliers/2000:
            num = random.randint(0,suppliers-1)
            if not (num in recommendations or num in complaints):
                complaints.append(num)
        complaints = sorted(complaints)

        for supplier in range(suppliers):
            if supplier%1000 == 0:
                self.__printOutProgress(startProgress,endProgress,0.1*(supplier/1000))
            name = self.__stringAppendNumber('Supplier',supplier,9)
            address = self.__randomString(10,40)
            nationkey = random.randint(0,61)
            phone = self.__phoneNumber(nationkey)
            acctbal = str(random.randint(-99999,99999)/100.0)

            if len(recommendations) and supplier == recommendations[0]:
                comment = self.__supplierComment(0)
                recommendations.pop(0)
            elif len(complaints) and supplier == complaints[0]:
                comment = self.__supplierComment(1)
                complaints.pop(0)
            else:
                comment = self.__supplierComment(2)

            supplierContentFile.write(
                str(supplier)+','
                +name+','
                +address+','
                +str(nationkey)+','
                +phone+','
                +acctbal+','
                +comment+'\n')

        supplierContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __originalData(self,insertOriginal,min,max):
        result = self.__randomString(min,max)
        positions = []
        while len(positions)<8:
            num = random.randint(0,len(result)-1)
            if not (num in positions):
                positions.append(num)
        positions = sorted(positions)
        if insertOriginal:
            for i in range(len(positions)):
                result = result[:positions[i]]+'ORIGINAL'[i]+result[positions[i]+1:]
        return result


    def __createItem(self,startProgress,endProgress):
        itemHeaderFile = open(self.__path + 'item_header.tbl', 'w')
        itemHeaderFile.write('I_ID|I_IM_ID|I_NAME|I_PRICE|I_DATA\n')
        itemHeaderFile.write('INTEGER|INTEGER|STRING|FLOAT|STRING\n')
        itemHeaderFile.write('0_R|0_R|0_R|0_R|0_R')
        itemHeaderFile.close()

        itemContentFile = open(self.__path + 'item.csv', 'w')

        items = 100000

        originals = []
        while len(originals)<items/10:
            num = random.randint(0,items-1)
            if not (num in originals):
                originals.append(num)
        originals = sorted(originals)

        for item in range(items):
            if item%5000 == 0:
                self.__printOutProgress(startProgress,endProgress,float(item)/items)
            IImId = str(random.randint(1,10000))
            name = self.__randomString(14,24)
            price = str(random.randint(1,10000)/100.0)

            if len(originals) and item == originals[0]:
                data = self.__originalData(True,26,50)
                originals.pop(0)
            else:
                data = self.__originalData(False,26,50)


            itemContentFile.write(
                str(item)+','
                +IImId+','
                +name+','
                +price+','
                +data+'\n')

        itemContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __zipCode(self):
        result = "".join(random.choice(string.digits) for x in xrange(4))
        result += "11111"
        return result

    def __createWarehouse(self,startProgress,endProgress):
        warehouseHeaderFile = open(self.__path + 'warehouse_header.tbl', 'w')
        warehouseHeaderFile.write('W_ID|W_NAME|W_STREET_1|W_STREET_2|W_CITY|W_STATE|W_ZIP|W_TAX|W_YTD\n')
        warehouseHeaderFile.write('INTEGER|STRING|STRING|STRING|STRING|STRING|STRING|FLOAT|FLOAT\n')
        warehouseHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        warehouseHeaderFile.close()

        self.__printOutProgress(startProgress,endProgress,0.0)
        warehouseContentFile = open(self.__path + 'warehouse.csv', 'w')

        for warehouse in range(self.__scaleFactor):
            name = self.__randomString(6,10)
            street1 =  self.__randomString(10,20)
            street2 =  self.__randomString(10,20)
            city =  self.__randomString(10,20)
            state =  self.__randomString(2,2)
            zipCode = self.__zipCode()
            taxCode = str(random.randint(0,2000)/10000.0)
            ytd = "300000.00"

            warehouseContentFile.write(
                str(warehouse)+','
                +name+','
                +street1+','
                +street2+','
                +city+','
                +state+','
                +zipCode+','
                +taxCode+','
                +ytd+'\n')

        warehouseContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createStock(self,startProgress,endProgress):
        stockHeaderFile = open(self.__path + 'stock_header.tbl', 'w')
        stockHeaderFile.write('S_I_ID|S_W_ID|S_QUANTITY|S_DIST_01|S_DIST_02|S_DIST_03|S_DIST_04|S_DIST_05|'
            'S_DIST_06|S_DIST_07|S_DIST_08|S_DIST_09|S_DIST_10|S_YTD|S_ORDER_CNT|S_REMOTE_CNT|S_DATA\n')
        stockHeaderFile.write('INTEGER|INTEGER|INTEGER|STRING|STRING|STRING|STRING|STRING|STRING|STRING|'
            'STRING|STRING|STRING|INTEGER|INTEGER|INTEGER|STRING\n')
        stockHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        stockHeaderFile.close()

        stockContentFile = open(self.__path + 'stock.csv', 'w')

        stocksPerWarehouse = 100000

        for warehouse in range(self.__scaleFactor):
            originals = []
            while len(originals)<stocksPerWarehouse/10:
                num = random.randint(0,stocksPerWarehouse-1)
                if not (num in originals):
                    originals.append(num)
            originals = sorted(originals)
            for stock in range(stocksPerWarehouse):
                if stock%5000 == 0:
                    self.__printOutProgress(startProgress,endProgress,(warehouse*stocksPerWarehouse+stock)/float(self.__scaleFactor*stocksPerWarehouse))
                iId = str(stock)
                wId = str(warehouse)
                quantity = str(random.randint(10,100))
                dist = "".join(self.__randomString(24,24)+"," for i in range(10))
                ytd = "0"
                orderCnt = "0"
                remoteCnt = "0"

                if len(originals) and stock == originals[0]:
                    data = self.__originalData(True,26,50)
                    originals.pop(0)
                else:
                    data = self.__originalData(False,26,50)

                stockContentFile.write(
                    iId+','
                    +wId+','
                    +quantity+','
                    +dist
                    +ytd+','
                    +orderCnt+','
                    +remoteCnt+','
                    +data+'\n')

        stockContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createDistrict(self,startProgress,endProgress):
        districtHeaderFile = open(self.__path + 'district_header.tbl', 'w')
        districtHeaderFile.write('D_ID|D_W_ID|D_NAME|D_STREET_1|D_STREET_2|D_CITY|D_STATE|D_ZIP|D_TAX|D_YTD|D_NEXT_O_ID\n')
        districtHeaderFile.write('INTEGER|INTEGER|STRING|STRING|STRING|STRING|STRING|STRING|FLOAT|FLOAT|INTEGER\n')
        districtHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        districtHeaderFile.close()

        districtContentFile = open(self.__path + 'district.csv', 'w')

        districtsPerWarehouse = 10
        for warehouse in range(self.__scaleFactor):
            for district in range(districtsPerWarehouse):
                if district == 5:
                    self.__printOutProgress(startProgress,endProgress,0.5)

                name = self.__randomString(6,10)
                street1 = self.__randomString(10,20)
                street2 = self.__randomString(10,20)
                city = self.__randomString(10,20)
                state = self.__randomString(2,2)
                zipCode = self.__zipCode()
                tax = str(random.randint(0,2000)/10000.0)
                ytd = "30000.00"
                nextOId = "3001"

                districtContentFile.write(
                    str(district)+','
                    +str(warehouse)+','
                    +name+','
                    +street1+','
                    +street2+','
                    +city+','
                    +state+','
                    +zipCode+','
                    +tax+','
                    +ytd+','
                    +nextOId+'\n')

        districtContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __lastName(self,x):
        numberString = "{:1.3f}".format(x/1000.0)[2:]
        return self.__lastNameList[int(numberString[0])]+self.__lastNameList[int(numberString[1])]+self.__lastNameList[int(numberString[2])]

    def __nuRandom(self,a,x,y,c):
        aTerm = random.randint(0,a)
        bTerm = random.randint(x,y)

        cTerm = (aTerm | bTerm) + c
        return (cTerm % (y-x+1)) + x

    def __createCustomer(self,startProgress,endProgress):
        customerHeaderFile = open(self.__path + 'customer_header.tbl', 'w')
        customerHeaderFile.write('C_ID|C_D_ID|C_W_ID|C_LAST|C_MIDDLE|C_FIRST|C_STREET_1|C_STREET_2|C_CITY|C_STATE|C_ZIP|C_PHONE|'
            'C_SINCE|C_CREDIT|C_CREDIT_LIM|C_DISCOUNT|C_BALANCE|C_YTD_PAYMENT|C_PAYMENT_CNT|C_DELIVERY_CNT|C_DATA\n')
        customerHeaderFile.write('INTEGER|INTEGER|INTEGER|STRING|STRING|STRING|STRING|STRING|STRING|STRING|STRING|'
            'STRING|STRING|STRING|FLOAT|FLOAT|FLOAT|FLOAT|INTEGER|INTEGER|STRING\n')
        customerHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        customerHeaderFile.close()

        customerContentFile = open(self.__path + 'customer.csv', 'w')

        districtsPerWarehouse = 10
        customersPerDistrict = 3000
        for warehouse in range(self.__scaleFactor):
            for district in range(districtsPerWarehouse):
                bcs = 0
                for customer in range(customersPerDistrict):
                    if customer == 0:
                        self.__printOutProgress(
                            startProgress,
                            endProgress,
                            (warehouse*districtsPerWarehouse+district)/float(self.__scaleFactor*districtsPerWarehouse)
                        )

                    if customer<1000:
                        last = self.__lastName(customer)
                    else:
                        c = random.randint(0,255)
                        last = self.__lastName(self.__nuRandom(255,0,999,c))

                    middle = 'OE'
                    first = self.__randomString(8,16)
                    street1 = self.__randomString(10,20)
                    street2 = self.__randomString(10,20)
                    city = self.__randomString(10,20)
                    state = self.__randomString(2,2)
                    zipCode = self.__zipCode()
                    phone = "".join(random.choice(string.digits) for x in xrange(16))
                    since = time.strftime("%Y%m%d%H%M%S")
                    credit = 'GC'
                    creditLim = '50000.00'
                    discount = str(random.randint(0,5000)/10000.0)
                    balance = '-10.00'
                    ytdPayment = '10.00'
                    paymentCnt = '1'
                    deliveryCnt = '0'
                    data = self.__randomString(300,500)
                    
                    insertBC = random.randint(0,9)
                    if ((insertBC == 0)and(bcs<customersPerDistrict/10))or(9*customersPerDistrict/10 == customer-bcs):
                        credit = 'BC'
                        bcs += 1

                    customerContentFile.write(
                        str(customer)+','
                        +str(district)+','
                        +str(warehouse)+','
                        +last+','
                        +middle+','
                        +first+','
                        +street1+','
                        +street2+','
                        +city+','
                        +state+','
                        +zipCode+','
                        +phone+','
                        +since+','
                        +credit+','
                        +creditLim+','
                        +discount+','
                        +balance+','
                        +ytdPayment+','
                        +paymentCnt+','
                        +deliveryCnt+','
                        +data+'\n')

        customerContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createHistory(self,startProgress,endProgress):
        historyHeaderFile = open(self.__path + 'history_header.tbl', 'w')
        historyHeaderFile.write('H_C_ID|H_C_D_ID|H_C_W_ID|H_D_ID|H_W_ID|H_DATE|H_AMOUNT|H_DATA\n')
        historyHeaderFile.write('INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|FLOAT|STRING\n')
        historyHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        historyHeaderFile.close()

        historyContentFile = open(self.__path + 'history.csv', 'w')

        districtsPerWarehouse = 10
        customersPerDistrict = 3000
        for warehouse in range(self.__scaleFactor):
            for district in range(districtsPerWarehouse):
                for customer in range(customersPerDistrict):
                    if customer == 0:
                        self.__printOutProgress(
                            startProgress,
                            endProgress,
                            (warehouse*districtsPerWarehouse+district)/float(self.__scaleFactor*districtsPerWarehouse)
                        )

                    date = time.strftime("%Y%m%d%H%M%S")
                    amount = '10.00'
                    data = self.__randomString(12,24)
                    
                    historyContentFile.write(
                        str(customer)+','
                        +str(district)+','
                        +str(warehouse)+','
                        +str(district)+','
                        +str(warehouse)+','
                        +date+','
                        +amount+','
                        +data+'\n')

        historyContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createOrder(self,startProgress,endProgress):
        orderHeaderFile = open(self.__path + 'order_header.tbl', 'w')
        orderHeaderFile.write('O_ID|O_D_ID|O_W_ID|O_C_ID|O_ENTRY_D|O_CARRIER_ID|O_OL_CNT|O_ALL_LOCAL\n')
        orderHeaderFile.write('INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER\n')
        orderHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        orderHeaderFile.close()

        orderContentFile = open(self.__path + 'order.csv', 'w')

        districtsPerWarehouse = 10
        ordersPerDistrict = 3000
        customers = range(3000)
        random.shuffle(customers)
        for warehouse in range(self.__scaleFactor):
            for district in range(districtsPerWarehouse):
                for order in range(ordersPerDistrict):
                    if order == 0:
                        self.__printOutProgress(
                            startProgress,
                            endProgress,
                            (warehouse*districtsPerWarehouse+district)/float(self.__scaleFactor*districtsPerWarehouse)
                        )

                    customer = customers[order]
                    entryD = time.strftime("%Y%m%d%H%M%S")
                    self.__entryD.append(entryD)
                    if order <2100:
                        carrierID = str(random.randint(0,9))
                    else:
                        order = 'NULL'
                    olCNT = random.randint(5,15)
                    self.__olCNT.append(olCNT)
                    allLocal = '1'
                    
                    orderContentFile.write(
                        str(order)+','
                        +str(customer)+','
                        +str(district)+','
                        +str(warehouse)+','
                        +entryD+','
                        +carrierID+','
                        +str(olCNT)+','
                        +allLocal+'\n')

        orderContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createOrderline(self,startProgress,endProgress):
        orderlineHeaderFile = open(self.__path + 'orderline_header.tbl', 'w')
        orderlineHeaderFile.write('OL_O_ID|OL_D_ID|OL_W_ID|OL_NUMBER|OL_I_ID|OL_SUPPLY_W_ID|OL_DELIVERY_D|OL_QUANTITY|OL_AMOUNT|OL_DIST_INFO\n')
        orderlineHeaderFile.write('INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|INTEGER|FLOAT|STRING\n')
        orderlineHeaderFile.write('0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R|0_R')
        orderlineHeaderFile.close()

        orderlineContentFile = open(self.__path + 'orderline.csv', 'w')

        districtsPerWarehouse = 10
        ordersPerDistrict = 3000
        customers = range(3000)
        random.shuffle(customers)
        absOrder = 0
        for warehouse in range(self.__scaleFactor):
            for district in range(districtsPerWarehouse):
                for order in range(ordersPerDistrict):
                    for orderline in range(self.__olCNT[absOrder]):
                        if order == 0:
                            self.__printOutProgress(
                                startProgress,
                                endProgress,
                                (warehouse*districtsPerWarehouse+district)/float(self.__scaleFactor*districtsPerWarehouse)
                            )


                        iId = random.randint(0,99999)
                        quantity = '5'
                        if order < 2100:
                            deliveryD = self.__entryD[absOrder]
                            amount = '0.00'
                        else:
                            deliveryD = 'NULL'
                            amount = str(random.randint(1,999999)/100.0)
                        distInfo = self.__randomString(24,24)
                        
                        orderlineContentFile.write(
                            str(order)+','
                            +str(district)+','
                            +str(warehouse)+','
                            +str(orderline)+','
                            +str(iId)+','
                            +str(warehouse)+','
                            +deliveryD+','
                            +quantity+','
                            +amount+','
                            +distInfo+'\n')
                    absOrder += 1

        orderlineContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

    def __createNewOrder(self,startProgress,endProgress):
        newOrderHeaderFile = open(self.__path + 'newOrder_header.tbl', 'w')
        newOrderHeaderFile.write('NO_O_ID|NO_D_ID|NO_W_ID\n')
        newOrderHeaderFile.write('INTEGER|INTEGER|INTEGER\n')
        newOrderHeaderFile.write('0_R|0_R|0_R')
        newOrderHeaderFile.close()

        newOrderContentFile = open(self.__path + 'newOrder.csv', 'w')

        districtsPerWarehouse = 10
        ordersPerDistrict = 3000
        for warehouse in range(self.__scaleFactor):
            for district in range(districtsPerWarehouse):
                for order in range(2100,ordersPerDistrict):
                    if order == 0:
                        self.__printOutProgress(
                            startProgress,
                            endProgress,
                            (warehouse*districtsPerWarehouse+district)/float(self.__scaleFactor*districtsPerWarehouse)
                        )
                    
                    newOrderContentFile.write(
                        str(order)+','
                        +str(district)+','
                        +str(warehouse)+'\n')

        newOrderContentFile.close()
        self.__printOutProgress(startProgress,endProgress,1.0)

if __name__ == "__main__":
    print "\n\n\n"
    print "#############################"
    print "#   TPC-CH data generator   #"
    print "#############################\n"
    if len(sys.argv) < 2:
        scaleFactor = int(raw_input("Scale factor (at least 1): "))
        print ""
    else:
        scaleFactor = int(sys.argv[1])

    if not os.path.exists("tables"):
        os.makedirs("tables")

    tpcchGenerator = TpcchGenerator(scaleFactor,"tables/")

    tpcchGenerator.do()
