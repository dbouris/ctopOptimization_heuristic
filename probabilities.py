import csv
import pprint
import math
import time

class Route:
  def __init__(self, route,capacity,id,time):
    self.route = route
    self.capacity  = capacity
    self.id = id
    self.time = time

class Customer:
  def __init__(self, id, x, y, demand, serv_time, profit ):
    self.id = id
    self.x = x
    self.y = y
    self.demand = demand
    self.serv_time = serv_time
    self.profit = profit

class BestInsertion(object):
    def __init__(self):
        self.cost = None
        self.customer = None
        self.route = None
        self.position = None
        

    def Initialize(self):
        self.cost = 10*900
        self.customer = None
        self.route = None
        self.position = None



def getCost_Matrix(c_list):
    cost_matrix=[]
    c_list.insert(0,Customer(0,23.142,11.736,0,0,0))
    rows = len(c_list)
    cost_matrix = [[0.0 for x in range(rows)] for y in range(rows)]
    for i in range(0, len(c_list)):
            for j in range(0, len(c_list)):
                a = c_list[i]
                b = c_list[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                cost_matrix[i][j] = dist
    c_list.pop(0)
    return cost_matrix

def getCustomers(txt_file):
    
    rows = []
    with open(txt_file, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    cust_list = []
    for i in range(11,347):
        customer_obj = Customer(int(rows[i][0]),float(rows[i][1]),float(rows[i][2]),int(rows[i][3]),int(rows[i][4]),int(rows[i][5]))
        cust_list.append(customer_obj)
    return cust_list
    

def getCustomersSorted(cust_list,s_serv,s_profit,s_demand):
    demand_list =[]
    serv_time_list =[]
    profit_list = []
    
    
    for i in cust_list:
        demand_list.append((i.id,i.demand))
        serv_time_list.append((i.id,i.serv_time))
        profit_list.append((i.id,i.profit))

    demand_list.sort(key=lambda x:x[1])
    serv_time_list.sort(key=lambda x:x[1])
    profit_list.sort(key=lambda x:x[1], reverse = True)

    cust_sorted=[]
    for i in cust_list:
        attractivness = s_demand*demand_list.index((i.id,i.demand)) + s_serv* serv_time_list.index((i.id,i.serv_time)) + s_profit*profit_list.index((i.id,i.profit))
        cust_sorted.append((i,attractivness))
    cust_sorted.sort(key=lambda x:x[1])
    
    return cust_sorted



class BestInsertion(object):
    def __init__(self):
        self.cost = 10**9
        self.customer = None
        self.route = None
        self.position = None
        

    def Initialize(self):
        self.cost = 100000.0
        self.customer = None
        self.route = None
        self.position = None

def IdentifyMinimumCostInsertion(node, rt_list):
    best_insertion = BestInsertion()
    for rt in rt_list:
        
        if rt.capacity + node.demand <= 150 and rt.time + node.serv_time <= 200:
            
            for j in range(0, len(rt.route) - 1):
                A = rt.route[j].id
                B = rt.route[j + 1].id
                
                costAdded = cost_matrix[A][node.id] + cost_matrix[node.id][B]
                costRemoved = cost_matrix[A][B]
                
                trialCost = costAdded - costRemoved
                
                if trialCost < best_insertion.cost:
                    
                    best_insertion.customer = node
                    best_insertion.route = rt.id
                    best_insertion.position = j
                    best_insertion.cost = trialCost
                    
        else:
            continue
    return best_insertion


def InsertBestFit(best_fit,route_list):
    
    r = route_list[best_fit.route].route
    r.insert(best_fit.position+1,best_fit.customer)
    route_list[best_fit.route].route = r
    route_list[best_fit.route].capacity += best_fit.customer.demand
    route_list[best_fit.route].time += best_fit.customer.serv_time
   
def calclulateProfit(route_list):
    profit = 0
    for i in route_list:
        for k in i.route:
            profit += k.profit
    print("PROFIT", profit)
    return profit







cust_list = getCustomers("instance.csv")
start = time.time()
cost_matrix = getCost_Matrix(cust_list)


cust_list = getCustomers("instance.csv")

start = time.time()
cost_matrix = getCost_Matrix(cust_list)

max_prof = -1
a1 = 0
a2 =0 
a3 = 0

for a in range(0,100,3):
    for l in range(0,100-a,3):
        apothiki = Customer(0,0,0,0,0,0)
        trucks = 6
        route_list = []

        for i in range(0,trucks):
            r = Route([apothiki,apothiki],0,i,0)
            route_list.append(r)

        weight_serv_time= a/100
        weight_profit = l/100
        weight_demand = (100-a-l)/100
        print(weight_serv_time,weight_profit,weight_demand)

        cust_sorted = getCustomersSorted(cust_list,weight_serv_time,weight_profit,weight_demand)
        for i in cust_sorted:
            b = IdentifyMinimumCostInsertion(i[0], route_list)
            if b.customer != None:
                InsertBestFit(b,route_list)
        prof = calclulateProfit(route_list)
        if prof > max_prof:
            max_prof = prof
            a1= weight_serv_time
            a2 = weight_profit
            a3 = weight_demand
            
        for k in route_list:
            print("ROUTE " , k.id ,"LEN: " , len(k.route), "TIME: ", k.time, "CAPACITY ", k.capacity)
print("THE BEST I FOUND WAS: ", max_prof)
print("SERV_WEIGHT: ", a1)
print("PROFIT_WEIGHT: ",a2)
print("DEMAND_WEIGHT: ", a3)