import csv
from datetime import datetime
import os
import csv

# Pawan Kumar
# ID: 2046222

#making directory for output files
if not os.path.exists('reports/'):
    os.mkdir('./reports/')


# Class for generating output files
class GenerateOutputFiles:

    def __init__(self, item_list):

        self.item_list = item_list

    def fullInventory(self):
        #generating csv file for fullinventory
        with open('./reports/FullInventory.csv', 'w') as file:
            items = self.item_list

            keys=[]
            for i in items.keys():
                keys.append(i)
            # print(keys)
            man_name=[]
            for item in items.keys():
                man_name.append(items[item]['manufacturer'])

            for i in range(len(keys)):
                for j in range(len(keys) - 1):
                    if man_name[j] > man_name[j+1]:
                        swap = man_name[j]
                        man_name[j] = man_name[j +1 ]
                        man_name[j+1] = swap
                        swap2 = keys[j]
                        keys[j] = keys[j+1]
                        keys[j+1] = swap2

            for item in keys:
                itemid = item
                man_name = items[item]['manufacturer']
                item_type = items[item]['item_type']
                price = items[item]['price']
                service_date = items[item]['service_date']
                isdamaged = items[item]['damaged']
                file.write('{},{},{},{},{},{}\n'.format(itemid,man_name,item_type,price,service_date,isdamaged))

    def itemTypes(self):
        #CSV file for item types e.g laptop
        items = self.item_list
        types = []
        keys = sorted(items.keys())
        for item in items:
            item_type = items[item]['item_type']
            if item_type not in types:
                types.append(item_type)
        for type in types:
            file_name = type.capitalize() + 'Inventory.csv'
            with open('./reports/'+file_name, 'w') as file:
                for item in keys:
                    id = item
                    man_name = items[item]['manufacturer']
                    price = items[item]['price']
                    service_date = items[item]['service_date']
                    damaged = items[item]['damaged']
                    item_type = items[item]['item_type']
                    if type == item_type:
                        file.write('{},{},{},{},{}\n'.format(id, man_name, price, service_date, damaged))

    def pastService(self):

        items = self.item_list

        # for dtime in sorted(items.keys()):
        #     # print(item,datetime.strptime(items[item]['service_date'],"%m/%d/%Y").date())
        #     print(sorted(items.keys, datetime.strptime(items[item]['service_date'],"%m/%d/%Y").date()))
        # for item in items.keys():
        #     var=datetime.strptime(items[item]['service_date'],"%m/%d/%Y").date()
        #     print(sorted(items.keys(),key=var))
        # print(items.values())
        keys=[]
        for i in items.keys():
            keys.append(i)
        # print(keys)
        dtime=[]
        for item in items.keys():
            dtime.append(str(datetime.strptime(items[item]['service_date'],"%m/%d/%Y").date()))

        # print(dtime)

        for i in range(len(keys)):
            for j in range(len(keys) - 1):
                if dtime[j] < dtime[j+1]:
                    swap = dtime[j]
                    dtime[j] = dtime[j +1 ]
                    dtime[j+1] = swap
                    swap2 = keys[j]
                    keys[j] = keys[j+1]
                    keys[j+1] = swap2

        with open('./reports/PastServiceDateInventory.csv', 'w') as file:
            #generating dictionary
            for item in keys:
                id = item
                man_name = items[item]['manufacturer']
                item_type = items[item]['item_type']
                price = items[item]['price']
                service_date = items[item]['service_date']
                damaged = items[item]['damaged']
                today = datetime.now().date()
                service_expiration = datetime.strptime(service_date, "%m/%d/%Y").date()
                expired = service_expiration < today
                if expired:
                    file.write('{},{},{},{},{},{}\n'.format(id, man_name, item_type, price, service_date, damaged))


    def ItemsDamaged(self):

        items = self.item_list

        keys=[]
        for i in items.keys():
            keys.append(i)
        # print(keys)
        price=[]
        for item in items.keys():
            price.append(items[item]['price'])

        for i in range(len(keys)):
            for j in range(len(keys) - 1):
                if price[j] < price[j+1]:
                    swap = price[j]
                    price[j] = price[j +1 ]
                    price[j+1] = swap
                    swap2 = keys[j]
                    keys[j] = keys[j+1]
                    keys[j+1] = swap2

        # print(dtime)

        with open('./reports/DamagedInventory.csv', 'w') as file:
            #generating dictionary
            for item in keys:
                id = item
                man_name = items[item]['manufacturer']
                item_type = items[item]['item_type']
                price = items[item]['price']
                service_date = items[item]['service_date']
                damaged = items[item]['damaged']
                if damaged:
                    file.write('{},{},{},{},{}\n'.format(id, man_name, item_type, price, service_date))


if __name__ == '__main__':
    results = {}
    files = ['ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv']
    for file in files:
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                item_id = line[0]
                if file == files[0]:
                    results[item_id] = {}
                    man_name = line[1]
                    item_type = line[2]
                    damaged = line[3]
                    results[item_id]['manufacturer'] = man_name.strip()
                    results[item_id]['item_type'] = item_type.strip()
                    results[item_id]['damaged'] = damaged
                elif file == files[1]:
                    price = line[1]
                    results[item_id]['price'] = price
                elif file == files[2]:
                    service_date = line[1]
                    results[item_id]['service_date'] = service_date

    inventory = GenerateOutputFiles(results)
    inventory.fullInventory()
    inventory.itemTypes()
    inventory.pastService()
    inventory.ItemsDamaged()
    ids=[]
    manufacturer=[]
    types=[]
    price=[]
    date=[]
    with open('reports/FullInventory.csv', 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        for row in my_reader:
            ids.append(int(row[0]))
            manufacturer.append(row[1])
            types.append(row[2])
            price.append(int(row[3]))
            date.append(row[4])
    data={}
    data['id']= ids
    data['manufacturer']=manufacturer
    data['type']=types
    data['price']=price
    data['data']=date


    while True:
        #prompt the user for the query
        q = input("Type a query or q to quit: ")
        #if the user enters q exit the program
        if(q == "q"):
            break
        #intialize the manufacturer and type
        item = ""
        types = ""
        #iterate over the dictionary
        for i in data["manufacturer"]:
        #if the current manufacturer is present in the query
            if i in q:
            #assign the manufacturer to items
                item = i

            #iterate over all the types in data
        for i in data["type"]:
        #if the current type in the query
            if i in q:
                #assignt the type
                types = i
        if(item == "" or types == ""):
            print("No such item in invetory")
        else:
            details = ["", "", "", 0]


    #if either item or type is empty print it
        for i in range(len(data["id"])):
            if(data["manufacturer"][i] == item and data["type"][i] == types):
                if(details[3] < data["price"][i]):
                    details[0] = data["id"][i]
                    details[1] = data["manufacturer"][i]
                    details[2] = data["type"][i]
                    details[3] = data["price"][i]
                    print("Your item is " + str(details[0]) + " " + str(details[1]) + " " + str(details[2]) + " " + str(details[3]))
                    extra = []
                    for i in range(len(data["id"])):
                        if(data["type"][i] == types and data["manufacturer"][i] != item):
                            extra.append([data["id"][i], data["manufacturer"][i], data["type"][i], data["price"][i]])
                        if(len(extra) != 0):
                            print("You may also like ")
                            for i in range(len(extra)):
                                print(str(extra[i][0]) + " " + extra[i][1] + " " + extra[i][2] + " " + str(extra[i][3]))

