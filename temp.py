
from pymongo import MongoClient
import pprint

client = MongoClient(port=27017)
db=client.business


def dropDB():
    db.race_detail.drop()
    db.horse_detail.drop()
    db.user_detail.drop()
    db.odds_detail.drop()
    db.bet_detail.drop()

def insertDB(race_data,horse_data,user_data,odds_data):
    db.race_detail.insert(race_data)
    db.horse_detail.insert(horse_data)
    db.user_detail.insert(user_data)
    db.odds_detail.insert(odds_data)
    updateOdds('R1')
    updateOdds('R2')
    updateOdds('R3')

def readRace():
    readData = db.race_detail.find()
    #pprint.pprint(db.race_detail.find())
    data = []
    for item in readData:
        data.append(item)
        #pprint.pprint(item)
    print(data)
    return data

def readOneRace(raceId):
    readData = db.race_detail.find_one({'raceId':raceId})
    return readData

def updateUser(qrcode):
    data = db.user_data.update(
        {'userId':'U1'},
        {'qrcode':qrcode}
        )

def readUser():
    return db.user_detail.find_one({'userId':'U1'})

def readOneRace(raceId):
    readData = db.race_detail.find_one({'raceId':raceId})
    return readData
    
def insertBetData(userId,raceId,horseId,bet):
    db.bet_detail.insert(
        {
            "userId":userId,
            "raceId":raceId,
            "horseId":horseId,
            "bet":bet,
            "winMoney":0,
            "QRcode":"you've not won anything"
            }
        )
    db.odds_detail.update(
        {'raceId':raceId,'horses.horseId':horseId},
        {'$inc':{'horses.$.bet':bet,'totalBet':bet}}
        )
    
    updateOdds(raceId)

   
    

def updateOdds(raceId):
    horse=db.odds_detail.find({'raceId':raceId},{'_id':0,'horses':1})
    #print(horse)
    
    totalBet = db.odds_detail.find({'raceId':"R1"},{'_id':0,'totalBet':1})
    data = []
    for item in totalBet:
        data.append(item)
        #pprint.pprint(item)
    totalBetValue = data[0]['totalBet']
        
    data = []
    for item in horse:
        data.append(item)
        #pprint.pprint(item)
    #print(data[0]['horses'])
    data1 = data[0]['horses']
    for item in data1:
        tempOdds = totalBetValue / item['bet']
        db.odds_detail.update(
        {'raceId':raceId,'horses.horseId':item['horseId']},
        {'$set':{'horses.$.odds':tempOdds}}
        )

        
def insert():
    odds_data = [
        {
            'raceId':'R1',
            'horses':[
                {
                'horseId':'H1',
                'bet':10,
                'odds':0
                },
                {
                'horseId':'H2',
                'bet':20,
                'odds':0
                },
                {
                'horseId':'H3',
                'bet':15,
                'odds':0
                },
                {
                'horseId':'H12',
                'bet':13,
                'odds':0
                },
                {
                'horseId':'H5',
                'bet':30,
                'odds':0
                },
                {
                'horseId':'H6',
                'bet':20,
                'odds':0
                },
                {
                'horseId':'H10',
                'bet':25,
                'odds':0
                },
                {
                'horseId':'H8',
                'bet':50,
                'odds':0
                }],
            'totalBet': 183
            },
        {
            'raceId':'R2',
            'horses':[
                {
                'horseId':'H1',
                'bet':32,
                'odds':0
                },
                {
                'horseId':'H12',
                'bet':12,
                'odds':0
                },
                {
                'horseId':'H3',
                'bet':42,
                'odds':0
                },
                {
                'horseId':'H9',
                'bet':100,
                'odds':0
                },
                {
                'horseId':'H11',
                'bet':84,
                'odds':0
                },
                {
                'horseId':'H5',
                'bet':62,
                'odds':0
                },
                {
                'horseId':'H7',
                'bet':14,
                'odds':0
                },
                {
                'horseId':'H8',
                'bet':56,
                'odds':0
                }],
            'totalBet': 402
            },
        {
            'raceId':'R3',
            'horses':[
                {
                'horseId':'H1',
                'bet':8,
                'odds':0
                },
                {
                'horseId':'H2',
                'bet':19,
                'odds':0
                },
                {
                'horseId':'H9',
                'bet':83,
                'odds':0
                },
                {
                'horseId':'H4',
                'bet':48,
                'odds':0
                },
                {
                'horseId':'H12',
                'bet':35,
                'odds':0
                },
                {
                'horseId':'H6',
                'bet':92,
                'odds':0
                },
                {
                'horseId':'H7',
                'bet':36,
                'odds':0
                },
                {
                'horseId':'H8',
                'bet':53,
                'odds':0
                }],
            'totalBet': 374
            }
        ]
            
                
    race_data = [
        {
            'raceId':"R1",
            'raceName':"roco",
            'startTime':"08/03/2019 12:42:00", #edit here
            'endTime':"08/03/2019 12:50:00", #here too
            'horseIds':["H1","H2","H3","H12","H5","H6","H10","H8"]
            
            },
        {
            'raceId':"R2",
            'raceName':"poco",
            'startTime':"09/03/2019 12:42:00", #edit here
            'endTime':"09/03/2019 12:50:00", #here too
            'horseIds':["H1","H12","H3","H9","H11","H5","H7","H8"]
            },
        {
            'raceId':"R3",
            'raceName':"koco",
            'startTime':"10/03/2019 12:42:00", #edit here
            'endTime':"10/03/2019 12:50:00", #here too
            'horseIds':["H1","H2","H9","H4","H12","H6","H7","H8"]
            },        
        ]
    horse_data = [
        {
            'horseId':"H1",
            'horseName':"Birju",
            'fitnessLevel':"69",
            'breed':"Thoroughbred",
            },
        {
            'horseId':"H2",
            'horseName':"Jackson",
            'fitnessLevel':"60",
            'breed':"Trakehner",
            },
        {
            'horseId':"H3",
            'horseName':"Pavan",
            'fitnessLevel':"95",
            'breed':"Kathiawari",
            },
        {
            'horseId':"H4",
            'horseName':"Rocky",
            'fitnessLevel':"54",
            'breed':"Paso fino",
            },
        {
            'horseId':"H5",
            'horseName':"Patty",
            'fitnessLevel':"80",
            'breed':"Friesian",
            },
        {
            'horseId':"H6",
            'horseName':"Mike",
            'fitnessLevel':"76",
            'breed':"Thoroughbred",
            },
        {
            'horseId':"H7",
            'horseName':"Dracko",
            'fitnessLevel':"64",
            'breed':"Breton",
            },
        {
            'horseId':"H8",
            'horseName':"Badal",
            'fitnessLevel':"92",
            'breed':"Marwari",
            },
        {
            'horseId':"H9",
            'horseName':"Raghu",
            'fitnessLevel':"86",
            'breed':"Marwari",
            },
        {
            'horseId':"H10",
            'horseName':"Diablo",
            'fitnessLevel':"82",
            'breed':"Spanish Mustang",
            },
        {
            'horseId':"H11",
            'horseName':"Tom",
            'fitnessLevel':"76",
            'breed':"Cruise",
            },
        {
            'horseId':"H12",
            'horseName':"Raju",
            'fitnessLevel':"92",
            'breed':"Kathiawari",
            }
        ]
    user_data = [
        {
            'userId':"U1",
            'name':"Brijesh",
            'password':"brijesh",
            'walletMoney':1000,
            'winMoney':0
            },
        {
            'userId':"U2",
            'name':"Vijay",
            'password':"vijay",
            'walletMoney':1000,
            'winMoney':0
            },
        {
            'userId':"U3",
            'name':"Kaushik",
            'password':"kaushik",
            'walletMoney':1000,
            'winMoney':0
            },
        ]
    insertDB(race_data,horse_data,user_data,odds_data)
    


# Code runs from here

dropDB()
insert()
insertBetData('U1','R1','H2',40)
#readOneRace("R3")