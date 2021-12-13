import csv
import math
from SolutionDrawer import *




class Route:
  def __init__(self, route,capacity,id,time):
    self.route = route
    self.capacity  = capacity
    self.id = id
    self.time = time

class Customer:
  def __init__(self, id, x, y, demand, serv_time, profit, added):
    self.id = id
    self.x = x
    self.y = y
    self.demand = demand
    self.serv_time = serv_time
    self.profit = profit
    self.added = added

class BestInsertion(object):
    def __init__(self):
        self.cost = 10*900
        self.customer = None
        self.route = None
        self.position = None
        self.cl = 10*900
        

    def Initialize(self):
        self.cost = 10*900
        self.customer = None
        self.route = None
        self.position = None
        self.cl = 10*900



def getCost_Matrix(c_list):
    cost_matrix=[]
    c_list.insert(0,Customer(0,23.142,11.736,0,0,0,False))
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
        customer_obj = Customer(int(rows[i][0]),float(rows[i][1]),float(rows[i][2]),int(rows[i][3]),int(rows[i][4]),int(rows[i][5]), False)
        cust_list.append(customer_obj)
    return cust_list
    



def IdentifyMinimumCostInsertion(rt_list,cust_list):
    best_insertion = BestInsertion()
    for customer in cust_list:
        if customer.added == False:
            for rt in rt_list:
                
                if rt.capacity + customer.demand <= 150:
                    
                    for j in range(0, len(rt.route) - 1):
                        A = rt.route[j].id
                        B = rt.route[j + 1].id
                    
                        costAdded = cost_matrix[A][customer.id] + cost_matrix[customer.id][B]
                        costRemoved = cost_matrix[A][B]
                        
                        trialCost = costAdded - costRemoved + customer.serv_time
                        

                        if rt.time  + trialCost <= 200:
                        #calculate the insertion criterion
                            criterion = calculate_insertion_criterion(customer,trialCost)
                            
                            if criterion < best_insertion.cl:
                                
                                best_insertion.customer = customer
                                best_insertion.route = rt.id
                                best_insertion.position = j
                                best_insertion.cost = trialCost 
                                best_insertion.cl = criterion
                            
                else:
                    continue
    return best_insertion


def getEmptyRoutes(trucks):
    apothiki = Customer(0,0,0,0,0,0,False)
    route_list = []

    for i in range(0,trucks):
        r = Route([apothiki,apothiki],0,i,0)
        route_list.append(r)
    return route_list



def not_all_added(cust_list):
    v = False
    for i in cust_list:
        if i.added == False:
            v = True
    return v

def calculate_insertion_criterion(customer,trial_cost):
    
    time_var = ((1+trial_cost)/(1+Max_Time))**time_weight
    demand_var = (customer.demand/Max_Capacity)**demand_weight
    profit_var = (customer.profit/ Max_Profit )**profit_weight
    ic = (time_var * demand_var)/profit_var
    return ic





def InsertBestFit(best_fit,route_list):
    
    r = route_list[best_fit.route].route
    r.insert(best_fit.position+1,best_fit.customer)
    route_list[best_fit.route].route = r
    route_list[best_fit.route].capacity += best_fit.customer.demand
    route_list[best_fit.route].time +=  best_fit.cost
    best_fit.customer.added = True


def calclulateProfitRoute(route_list):
    profit = []

    for i in route_list:
        prof = 0
        for k in i.route:
            prof += k.profit
        profit.append(prof)
    return profit

def calclulateTotalProfit(prof):
    total_prof = 0
    for i in prof:
        total_prof = total_prof +i
    return total_prof



Max_Time = 200
Max_Capacity = 150
Max_Profit = 35


#weigths
profit_weight = 0.56
demand_weight = 0.12
time_weight = 0.32



route_list = getEmptyRoutes(6)
cust_list = getCustomers("instance.csv")

cost_matrix = getCost_Matrix(cust_list)
keep_going = True
while not_all_added(cust_list) and keep_going:
    best = IdentifyMinimumCostInsertion(route_list,cust_list)
    if best.customer != None:
        InsertBestFit(best,route_list)
    else:
        keep_going = False

prof = calclulateProfitRoute(route_list)
total_prof = calclulateTotalProfit(prof)
print(total_prof)
for k in route_list:
    print("ROUTE " , k.id ,"LEN: " , len(k.route), "TIME: ", k.time, "CAPACITY: ", k.capacity, "PROFIT: ", prof[k.id])
    

for i in route_list:
    print("ROUTE ", i.id)
    for k in i.route:
        print(k.id, end = " ")
    print()



#for r in route_list:
#    cost = 0
#    for j in range(0,len(r.route)-1):
#        cost = cost + cost_matrix[r.route[j].id][r.route[j+1].id]
#    print(cost)
pr = 0
c = 0
for n in cust_list:
    
    if n.added == False:
        pr = pr +n.profit
        c = c +1 
avg_pr = pr/c
print("AVG PROFIT REMAINING: ", avg_pr)


SolDrawer.drawRoutes(route_list)
SolDrawer.drawPointsUsed(cust_list)

        