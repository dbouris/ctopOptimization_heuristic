import csv
import math
from shutil import move
from typing import NewType
from SolutionDrawer import *
import copy
from itertools import combinations
import pprint
import random
import timeit
import tabu_search
import local_search

# insert the problem variables
Max_Time = 200
Max_Capacity = 150
Max_Profit = 35

# initialize the weights for the insertion criterion
# the weights have been optimaly calculated to fit the problem.
profit_weight = 0.56
demand_weight = 0.12
time_weight = 0.32

class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None
        self.moveCost = 10**9

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None
        self.moveCost = 10 ** 9


class PairInsertionMove(object):
    def __init__(self):
        self.route = None
        self.nodetoremove = None
        self.route_list = None
        self.route_time = None
        self.capacity_change = None
        self.profit_added = -1
        self.pair_added = None
        self.pservedremove=None
        self.nodetoadd = None

    def Initialize(self):
        self.route = None
        self.nodetoremove = None
        self.nodetoadd = None
        self.route_list = None
        self.route_time = None
        self.pair_added = None
        self.capacity_change = None
        self.profit_added = -1
        self.pservedremove=None
        


class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.timeChangeFirstRt = None
        self.timeChangeSecondRt = None
        self.moveCost = 10**9
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.timeChangeFirstRt = None
        self.timeChangeSecondRt = None
        self.moveCost = 10 ** 9

class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10**9
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9



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
    self.isTabuTillIterator = -1

class BestInsertion(object):
    def __init__(self):
        self.time = 10*900
        self.customer = None
        self.route = None
        self.position = None
        self.cl = 10*900
        

    def Initialize(self):
        self.time = 10*900
        self.customer = None
        self.route = None
        self.position = None
        self.cl = 10*900


class OneRouteBi(object):
    def __init__(self):
        self.time = 10*900
        self.customer = None
        self.position = None
        

    def Initialize(self):
        self.time = 10*900
        self.customer = None
        self.position = None

class CandidatePairs:

    def __init__(self, customers):
        self.customers = customers
        self.totalProfit = 0
        self.totalDemand = 0
        self.totalServiceTime = 0
        for x in customers:
             self.totalProfit += x.profit
             self.totalDemand += x.demand
             self.totalServiceTime += x.serv_time
    
def InitializeOperators(rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()



#  calculate the distance between two customers in the cost matrix, which is a 2D array
def getCost_Matrix(c_list):
    cost_matrix=[]
    # add the first row of the cost matrix, which is the central depot of the problem
    c_list.insert(0,Customer(0,23.142,11.736,0,0,0,False))
    # initialize the cost matrix with zeros in all positions
    rows = len(c_list)
    cost_matrix = [[0.0 for x in range(rows)] for y in range(rows)]
    # iterate over all the pairs of customers
    for i in range(0, len(c_list)):
            for j in range(0, len(c_list)):
                # calculate the distance between the two customers
                a = c_list[i]
                b = c_list[j]
                # get the distance as the euclidean distance between the two customers
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                # update the cost matrix with the distance
                cost_matrix[i][j] = dist
    # remove the first row of the cost matrix, which is the central depot of the problem
    c_list.pop(0)
    return cost_matrix

# reads the customers and their attributes from the csv file
def getCustomers(txt_file):
    # get the rows of the csv file in a list
    rows = []
    # open the csv file
    with open(txt_file, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    cust_list = []
    # iterate over the rows of the csv file which contain customer data
    for i in range(11,347):
        # create the customer object
        customer_obj = Customer(int(rows[i][0]),float(rows[i][1]),float(rows[i][2]),int(rows[i][3]),int(rows[i][4]),int(rows[i][5]), False)
        # add the customer object to the list of customers
        cust_list.append(customer_obj)
    return cust_list
    


# finds the best insertion for our solution based on an insertion criterion and returns 
# the best insertion object
def identifyMinimumCostInsertion(rt_list,cust_list, cost_matrix):
    # initialize the BestInsertion object
    best_insertion = BestInsertion()
    # iterate over all customers 
    for customer in cust_list:
        # check if the customer is already added to the solution
        if customer.added == False:
            # iterate over all routes
            for rt in rt_list:
                # check if the customer fits in the route demand wise
                if rt.capacity + customer.demand <= 150:
                    # check the insertion criterion for all the possible positions-insertions in the route
                    for j in range(0, len(rt.route) - 1):
                        # get the customers ids
                        A = rt.route[j].id
                        B = rt.route[j + 1].id
                        # calculate the cost of inserting the customer in the route
                        # there is some cost added and some cost removed after inserting the customer
                        costAdded = cost_matrix[A][customer.id] + cost_matrix[customer.id][B]
                        costRemoved = cost_matrix[A][B]
                        # get the trial cost
                        trialCost = costAdded - costRemoved + customer.serv_time
                        
                        # check if the customer fits in the route time wise
                        if rt.time  + trialCost <= 200:
                            #calculate the insertion criterion
                            criterion = calculate_insertion_criterion(customer,trialCost)
                            # check if the current insertion criterion is better than our previous best
                            if criterion < best_insertion.cl:
                                # update the best insertion object
                                best_insertion.customer = customer
                                best_insertion.route = rt.id
                                best_insertion.position = j
                                best_insertion.time = trialCost 
                                best_insertion.cl = criterion
                            
                else:
                    # if the customer does not fit in the route demand wise, continue to the next route
                    continue
    return best_insertion

# creates empty routes based on the nummber of trucks
# each route starts and ends at the central depot
# example empty route: [apothiki,apothiki]
def getEmptyRoutes(trucks):
    apothiki = Customer(0,23.142,11.736,0,0,0,False)
    route_list = []
    # iterate over the number of trucks and create a route for each truck
    for i in range(0,trucks):
        r = Route([apothiki,apothiki],0,i,0)
        route_list.append(r)
    return route_list


# check if all the customers in the problem are added in the solution
# return true if all the customers are not added, else false
def not_all_added(cust_list):
    v = False
    # iterate through the customers
    for i in cust_list:
        # if a customer is not added, return true
        if i.added == False:
            v = True
    return v

# calculate the weighted insertion criterion
# the criterion consists of three factors: time, demand and profit added
# the criterion is based on the following idea: "We prefer a customer which takes low time to serve, takes little 
# demand and has high profit"
def calculate_insertion_criterion(customer,trial_cost):
    
    # get the 3 variables based on the pre calculated weights
    time_var = ((1+trial_cost)/(1+Max_Time))**time_weight
    demand_var = (customer.demand/Max_Capacity)**demand_weight
    profit_var = (customer.profit/ Max_Profit )**profit_weight
    # calculate the criterion
    ic = (time_var * demand_var)/profit_var
    return ic




# inserts the customer in the route in the position given
# the customer and the info for the insertion position is given in the best_fit object
def InsertBestFit(best_fit,route_list):
 
    # get the route list to insert into and insert the customer
    r = route_list[best_fit.route].route
    r.insert(best_fit.position+1,best_fit.customer)
    # update the route info
    route_list[best_fit.route].route = r
    # update the route capacity
    route_list[best_fit.route].capacity += best_fit.customer.demand
    # update the route time
    route_list[best_fit.route].time +=  best_fit.time
    # mark the customer as added
    best_fit.customer.added = True

# calculate the profit of each route in the list, and return a list with the profits
def calclulateProfitRoute(route_list):
    profit = []
    # iterate over the routes
    for i in route_list:
        prof = 0
        # iterate over the customers in the route
        for k in i.route:
            prof += k.profit
        profit.append(prof)
    return profit

# calculate the total profit of the solution, using the list of profit of each route
def calclulatetotalProfit(prof):
    total_prof = 0
    for i in prof:
        total_prof = total_prof +i
    return total_prof

# calculate the total serv time of the solution
def getTransferCost(route_list, cost_matrix):
    transfer = 0
    for i in route_list:
        transfer_cost = 0
        for j in range(0, len(i.route) - 1):
            A = i.route[j].id
            B = i.route[j + 1].id
            transfer_cost = transfer_cost + cost_matrix[A][B]
            if (j != 0):
                transfer_cost = transfer_cost + i.route[j].serv_time
        transfer = transfer + transfer_cost
    return transfer


# calculate the time cost of a route
# the time in each route consists of the time of the customers in the route (service time) 
# and the transfer time
def getTimeInRoute(route, cost_matrix):
    c = 0
    # iterate over the customers in the route
    for j in range (0, len(route) - 1):
        a = route[j]
        b = route[j + 1]
        # get the transfer time between the customers
        c += cost_matrix[a.id][b.id]
        # add the service time of the customer
        c += a.serv_time
    return c

        

# used to draw the solution in a matplotlib plot
def DrawSolution(route_list, cust_list):
    # first, draw the routes
    SolDrawer.drawRoutes(route_list)
    # then, draw the customers
    SolDrawer.drawPointsUsed(cust_list)


# apply the swap move to the solution
def ApplySwapMove(sm, route_list):
    # get the two routes
    rt1 = route_list[sm.positionOfFirstRoute]
    rt2 = route_list[sm.positionOfSecondRoute]
    # get the two customers to be swapped
    b1 = rt1.route[sm.positionOfFirstNode]
    b2 = rt2.route[sm.positionOfSecondNode]
    # swap the customers
    rt1.route[sm.positionOfFirstNode] = b2
    rt2.route[sm.positionOfSecondNode] = b1
    # if the two routes are the same, update the time of the route, the capacity is not changed
    if (rt1 == rt2):
        rt1.time += sm.moveCost
    # if the two routes are different, update the time and capacity of the two routes
    else:
        # update time
        rt1.time += sm.timeChangeFirstRt
        rt2.time += sm.timeChangeSecondRt
        # update capacity
        rt1.capacity = rt1.capacity - b1.demand + b2.demand
        rt2.capacity = rt2.capacity + b1.demand - b2.demand
        


# apply the relocation move on our current solution
        

# the function checks if there is a violation of the capacity constraint of the problem
# used in the two-opt move
def CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):

        # calculate the capacity of the first segment of the first route
        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.route[i]
            rt1FirstSegmentLoad += n.demand
        # get the capacity of the second segment of the first route by subtracting the first segment 
        # from the total capacity of the route
        rt1SecondSegmentLoad = rt1.capacity - rt1FirstSegmentLoad

        # get the capacity of the first segment of the second route
        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.route[i]
            rt2FirstSegmentLoad += n.demand
        # get the capacity of the second segment of the second route by subtracting the first segment
        # from the total capacity of the route
        rt2SecondSegmentLoad = rt2.capacity - rt2FirstSegmentLoad

        # check if the capacity of the first route is violated
        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > 150):
            return True
        # check if the capacity of the second route is violated
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > 150):
            return True

        return False








# created a first solution for the problem using the minimum cost insertion heuristic
def solve(cust_list, route_list, cost_matrix):
    keep_going = True
    # while there are customers that have not been inserted into a route
    while not_all_added(cust_list) and keep_going:
        # find the best customer to insert in the list
        best = identifyMinimumCostInsertion(route_list,cust_list , cost_matrix)
        # if we have found one: insert it else, stop
        if best.customer != None:
            # add the customer to the route selected above
            InsertBestFit(best,route_list)
        else:
            # the problem is infeasible
            keep_going = False




# get all the possible pairs of customers which are not served
def generatePairs(cust_list):
    customers = []
    for x in cust_list:
        if (x.added == False):
            customers.append(x)
    # get all the size:2 combinations of customers
    combinationPairs = combinations(customers, 2)

    pairs = []
    # create the pairs of the customers as objects
    for x in combinationPairs:
        candidate = CandidatePairs(x)
        pairs.append(candidate)

    return pairs

# generate all the possible pairs of customers which are served
def generateServedPairs(cust_list):
    # get all the customers which are served
    customers = []
    for x in cust_list:
        if (x.added == True):
            customers.append(x)
    # get all the size:2 combinations of customers
    combinationPairs = combinations(customers, 2)

    # create the pairs objects and return them
    pairs = []
    for x in combinationPairs:
        candidate = CandidatePairs(x)
        pairs.append(candidate)

    return pairs

# find the best possible addition for a node in a route list 
def IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix):
    # initialize the best insertion
    best_insertion = OneRouteBi()
    # iterate through all the customers which we need to add
    for customer in candidateroute:
        # if the customer is not added
        if customer.added == False:
            # iterate over all the possible positions in the route for the node to be added
            for j in range(0, len(newrt.route) - 1):
                # get the customers ids
                A = newrt.route[j].id
                B = newrt.route[j + 1].id
                # get the cost of the insertion
                costAdded = cost_matrix[A][customer.id] + cost_matrix[customer.id][B]
                costRemoved = cost_matrix[A][B]
                
                trialCost = costAdded - costRemoved + customer.serv_time

                # if the cost is lower than the best cost so far, update the best cost
                if trialCost < best_insertion.time:
                    best_insertion.customer = customer
                    best_insertion.position = j
                    best_insertion.time = trialCost 
        # if the customer is added, we do not need to add it again      
        else:
            continue
    # return the best insertion for the current state of the solution
    return best_insertion



def ApplyInsertion(newrt, best):
    # update time and capacity of the route
    newrt.capacity += best.customer.demand
    newrt.time +=  best.time 

    # add the node to its new position
    r = newrt.route
    r.insert(best.position+1,best.customer)
    newrt.route = r
    # mark the customer as added
    best.customer.added = True
    
# apply the pair move to the current solution
def ApplyPairMove(best : PairInsertionMove,route_list):
    # update the route list
    route_list[best.route].route = best.route_list
    # update the time and capacity of the route
    route_list[best.route].time = best.route_time
    # update the capacity of the route
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change
    # mark the customers as added
    best.pair_added.customers[0].added = True
    best.pair_added.customers[1].added = True
    best.nodetoremove.added = False

# apply the pair move (served pair) to the current solution 
def ApplyPairMoveServed(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change
    best.pair_added.customers[0].added = True
    best.pair_added.customers[1].added = True
    best.pservedremove.customers[0].added=False
    best.pservedremove.customers[1].added=False

# apply the move: PairMoveOneUnserved to the current solution
def ApplyPairMoveOneUnserved(best : PairInsertionMove,route_list):
    # update the route list
    route_list[best.route].route = best.route_list
    # update the time and capacity of the route
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change    
    # mark the customers as added
    best.nodetoadd.added = True
    best.pservedremove.customers[0].added=False
    best.pservedremove.customers[1].added=False



def ApplyOneNodeMove(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change
    best.nodetoadd.added = True   
    best.nodetoremove.added = False
    
    
    
def ApplyDestroy(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = best.capacity 



# find the best pair insertion move
     
def calculate_route_details(route, cost_matrix):
    rt_profit = 0
    rt_load = 0
    rt_time = 0
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i+1]
        rt_profit += from_node.profit
        rt_load += from_node.demand
        if i !=0:
            rt_time += from_node.serv_time
        travel_time = cost_matrix[from_node.id][to_node.id]
        rt_time += travel_time
    return rt_time, rt_load, rt_profit

def PairInsertion(pairlist, route_list, cost_matrix):
    
    # initialize the best move object
    best = PairInsertionMove()
    # iterate over all the pairs in the list
    for pair in pairlist:
        # if both the customers are not added
        if pair.customers[0].added == False and pair.customers[1].added == False:
            # iterate over all the routes
            for route in route_list:
                rt = route.route
                # iterate over all the positions in the route
                for nodeIndextoremove in range(1,len(route.route)-1):
                    # check if the profit to be added is greater than the profit to be removed
                    if pair.totalProfit >  rt[nodeIndextoremove].profit:
                        # check if the pair can fit in the route demand wise
                        if route.capacity - rt[nodeIndextoremove].demand + pair.totalDemand > 150:
                            continue
                        # check if the pair can fit in the route time wise
                        if route.time - rt[nodeIndextoremove].serv_time + pair.totalServiceTime > 200:
                            continue
                        
                        candidateroute = route.route[1:len(route.route)-1]
                        candidateroute.remove(rt[nodeIndextoremove])
                        for k in pair.customers:
                            candidateroute.append(k)
                        

                        newrt = getEmptyRoutes(1)[0]
                        for i in candidateroute:
                            i.added = False

                        # find the best position for the 2 customers to be inserted
                        for i in range(0,len(candidateroute)):
                            best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                            ApplyInsertion(newrt, best_inser)

                        pair.customers[0].added = False
                        pair.customers[1].added = False
                        
                        
                        # calculate the profit change
                        profit =  pair.totalProfit - rt[nodeIndextoremove].profit 
                        # check if the change is feasible time wise
                        if newrt.time > 200:
                            continue
                        
                        # if the change is feasible, check if it is better than the best move we have stored                                                 
                        if profit > best.profit_added:
                            best.profit_added = profit
                            best.route = route.id
                            best.route_list = newrt.route
                            best.route_time = newrt.time
                            best.pair_added = pair
                            best.nodetoremove = rt[nodeIndextoremove]
                            best.capacity_change = pair.customers[0].demand + pair.customers[1].demand - rt[nodeIndextoremove].demand
    # return the best move                            
    return best
           
def TwoPairExchange(route_list, cost_matrix, pairlist, pairserved): 
    # initialize the best move object
    best = PairInsertionMove()
    # iterate over all the pairs in the list
    for pair in pairlist:
        # check if both the customers are not added       
        if pair.customers[0].added == False and pair.customers[1].added == False:
            # iterate over all the routes
            for i in range(0,len(route_list)-1):
                # iterate over all the pairs in the route                              
                for pserved in pairserved[i]:
                    # check if both the customers are added, debug...
                    if pserved.customers[0].added == True and pserved.customers[1].added == True:
                        # check if the profit to be added is greater than the profit to be removed
                        if pair.totalProfit >  pserved.totalProfit: 
                            # check if the pair can fit in the route demand wise
                            if route_list[i].capacity - pserved.totalDemand + pair.totalDemand > 150:
                                continue
                            # check if the pair can fit in the route time wise
                            if route_list[i].time - pserved.totalServiceTime + pair.totalServiceTime > 200 :
                                continue
                            
                            candidateroute = route_list[i].route[1:len(route_list[i].route)-1] 
                            if (not pserved.customers[0] in route_list[i].route) or (not pserved.customers[1] in route_list[i].route):
                                continue
                            # remove the pair to be removed
                            candidateroute.remove(pserved.customers[0])
                            candidateroute.remove(pserved.customers[1])                             
                            # add the pair to be added
                            for k in pair.customers:
                                candidateroute.append(k)
                            newrt = getEmptyRoutes(1)[0]
                            for c in candidateroute:
                                c.added = False
                            # find the best position for the 2 customers to be inserted
                            for j in range(0,len(candidateroute)):
                                best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                                ApplyInsertion(newrt, best_inser)
                            pair.customers[0].added = False
                            pair.customers[1].added = False
                            profit =  pair.totalProfit - pserved.totalProfit
                            # check if the change is feasible time wise
                            if newrt.time > 200:
                                continue   
                            # if the change is feasible, check if it is better than the best move we have stored                         
                            if profit > best.profit_added:                                 
                                best.profit_added = profit 
                                best.route = route_list[i].id
                                best.route_list = newrt.route
                                best.route_time = newrt.time
                                best.pair_added = pair
                                best.pservedremove = pserved
                                best.capacity_change = pair.customers[0].demand + pair.customers[1].demand - (pserved.customers[0].demand + pserved.customers[1].demand)
                                
    return best

# find the best change for one served and one unserved customer
def OneServedOneUnservedExchange(route_list, cost_matrix, c_list): 
    # initialize the best move object
    best = PairInsertionMove()
    # iterate over all customers
    for c in c_list:
        # check if the customer is not added       
        if c.added == False:
            # iterate over all the routes
            for rt in route_list:
                # iterate over all the customers in the route which are served
                for served in rt.route:
                    if served.added == True:
                        # check if the profit to be added is greater than the profit to be removed
                        if c.profit >  served.profit:
                            # check if the customer can fit in the route demand wise
                            if rt.capacity - served.demand + c.demand > 150:
                                continue
                            # check if the customer can fit in the route time wise
                            if rt.time - served.serv_time + c.serv_time > 200 :
                                continue
                            
                            candidateroute = rt.route[1:len(rt.route)-1]                             
                            candidateroute.remove(served)
                            candidateroute.append(c)
                            newrt = getEmptyRoutes(1)[0]
                            for cand in candidateroute:
                                cand.added = False
                            # find the best position for the customer to be inserted
                            for j in range(0,len(candidateroute)):
                                best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                                ApplyInsertion(newrt, best_inser)
                            c.added=False
                            # calculate the profit change
                            profit =  c.profit - served.profit    
                            # check if the change is feasible time wise                       
                            if newrt.time > 200:                                 
                                continue
                            # if the change is feasible, check if it is better than the best move we have stored
                            if profit > best.profit_added:                                 
                                best.profit_added = profit 
                                best.route = rt.id
                                best.route_list = newrt.route
                                best.route_time = newrt.time
                                best.nodetoadd = c
                                best.nodetoremove = served
                                best.capacity_change = c.demand  - served.demand
    # return the best move                                 
    return best

# find the best move for adding one unserved customer and removing two served customers
def TwoServedOneUnservedExchange(route_list, cost_matrix, c_list, pairserved): 
    best = PairInsertionMove()
    # iterate over all customers
    for c in c_list:      
        # if the customer is not added 
        if c.added == False:
            # iterate over all the routes
            for i in range(0,len(route_list)-1):    
                # iterate over all the pairs in the route (served)                            
                for pserved in pairserved[i]:
                    if pserved.customers[0].added == True and pserved.customers[1].added == True:
                        # check if the profit to be added is greater than the profit to be removed
                        if c.profit >  pserved.totalProfit: 
                            # check if the customer can fit in the route demand wise
                            if route_list[i].capacity - pserved.totalDemand + c.demand > 150:
                                continue
                            # check if the customer can fit in the route time wise
                            if route_list[i].time - pserved.totalServiceTime + c.serv_time > 200 :
                                continue
                            
                            # find the best position for the customer to be inserted
                            candidateroute = route_list[i].route[1:len(route_list[i].route)-1]                             
                            candidateroute.remove(pserved.customers[0])
                            candidateroute.remove(pserved.customers[1]) 
                            
                            candidateroute.append(c)
                            newrt = getEmptyRoutes(1)[0]
                            for cand in candidateroute:
                                cand.added = False
                            for j in range(0,len(candidateroute)):
                                best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                                # apply the insertion
                                ApplyInsertion(newrt, best_inser)
                            c.added=False
                            # calculate the profit change
                            profit =  c.profit - pserved.totalProfit    
                            # check if the change is feasible time wise                         
                            if newrt.time > 200:                                 
                                continue
                            # if the change is feasible, check if it is better than the best move we have stored
                            if profit > best.profit_added:                                 
                                best.profit_added = profit 
                                best.route = route_list[i].id
                                best.route_list = newrt.route
                                best.route_time = newrt.time
                                best.nodetoadd = c
                                best.pservedremove = pserved
                                best.capacity_change = c.demand  - (pserved.customers[0].demand + pserved.customers[1].demand)                           
    # return the best move                     
    return best


def VND_PROFIT(route_list, cost_matrix, pairlist, pairlist2, pairserved, c_list):
        bestSolution = copy.deepcopy(route_list)
        VNDIterator = 0
        kmax = 2
        k = 0

        while k <= kmax:
            if k == 1:
                best: PairInsertionMove = PairInsertion(pairlist, route_list, cost_matrix)
                if best.profit_added > 0:
                        ApplyPairMove(best, route_list)
                       
                        VNDIterator = VNDIterator + 1
                        k = 0
                else:
                    k += 1
            elif k == 0:
                best: PairInsertionMove = TwoPairExchange(route_list, cost_matrix, pairlist2, pairserved)
                if best.profit_added > 0:
                       
                        ApplyPairMoveServed(best, route_list)
                       
                        VNDIterator = VNDIterator + 1
                        k = 0
                else:
                    k += 1
            elif k == 2:
                best: PairInsertionMove = TwoServedOneUnservedExchange(route_list, cost_matrix, c_list, pairserved)
                if best.profit_added > 0:
                        
                        ApplyPairMoveOneUnserved(best,route_list)
                        
                        VNDIterator = VNDIterator + 1
                        k = 0
                else:
                    k += 1

            


           
            bestSolution = copy.deepcopy(route_list)
            prof = calclulateProfitRoute(bestSolution)
            total_prof = calclulatetotalProfit(prof)
            

            bestSolution = copy.deepcopy(route_list)
            prof = calclulateProfitRoute(bestSolution)
            total_prof = calclulatetotalProfit(prof)
            
# the tabu search function, implements the a functionality similar to the Local Search function
# but lets the algorithm to further explore the neighbourhood of the current solution by choosing solutions
# which do not improve the current solution
def TabuSearch(operator, route_list, cost_matrix, cust_list):
    solution_cost_trajectory = []
    random.seed(30)
    bestSolution = copy.deepcopy(route_list)
    terminationCondition = False
    localSearchIterator = 0

    rm = RelocationMove()
    sm = SwapMove()
    top:TwoOptMove = TwoOptMove()

   

    while terminationCondition is False:
        # choose the operator to be used in random
        operator = random.randint(0,2)
        InitializeOperators(rm, sm, top)
        
        # Relocations
        if operator == 0:
            # find the best relocation move
            tabu_search.FindBestRelocationMoveTabu(rm, localSearchIterator, route_list, cost_matrix, bestSolution)
            # if there is a move found, apply it
            if rm.originRoutePosition is not None:
                tabu_search.ApplyRelocationMoveTabu(rm, route_list, localSearchIterator)
                
        # Swaps
        elif operator == 1:
            # find the best swap move
            tabu_search.FindBestSwapMoveTabu(sm,route_list, cost_matrix, localSearchIterator, bestSolution)
            # if there is a move found, apply it
            if sm.positionOfFirstRoute is not None:
                tabu_search.ApplySwapMoveTabu(sm, route_list, localSearchIterator)
        # two opt    
        elif operator == 2:
            # find the best two opt move
            tabu_search.FindBestTwoOptMoveTabu(top,route_list, cost_matrix, localSearchIterator, bestSolution)
            # find the best two opt move
            if top.positionOfFirstRoute is not None:
                tabu_search.ApplyTwoOptMoveTabu(top,route_list, cost_matrix, localSearchIterator)
                

        # self.ReportSolution(self.sol)
        
        solution_cost_trajectory.append(getTransferCost(route_list, cost_matrix))

        if (getTransferCost(route_list, cost_matrix) < getTransferCost(bestSolution, cost_matrix)):
            bestSolution = copy.deepcopy(route_list)

        # SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

        localSearchIterator = localSearchIterator + 1

        candidates = generatePairs(cust_list)
        servedpairs=[]
        candidates2=[]
        candidates2 = generatePairs(cust_list)
        allservedpairs=[]
        allservedpairs=generateServedPairs(cust_list)
        
        
        for r in route_list:
            servedpairs.append(generateServedPairs(r.route))

        VND_PROFIT(route_list, cost_matrix, candidates, candidates2, servedpairs, cust_list)

        if localSearchIterator > 5:
            terminationCondition = True

    # SolDrawer.draw('final_ts', self.bestSolution, self.allNodes)
    # SolDrawer.drawTrajectory(solution_cost_trajectory)

    route_list = copy.deepcopy(bestSolution)

# define a function to random remove a customer from a route and replacing it with
# another customer from another route or unserved customer
def randomRemoval(rt,cost_matrix,seed,route_list):
    best = PairInsertionMove()
    remnodes=[]
    random.seed(seed)    
    remnodes=random.sample(range(1,len(rt.route)-1), 4)
    remnodes.sort(reverse=True)    
    for node in remnodes:
        remcustomer=rt.route[node]            
        remcustomer.added=False
        rt.route.remove(remcustomer)
        if len(rt.route)==2:
            break
    
    candidateroute = rt.route[1:len(rt.route)-1]
    newrt = getEmptyRoutes(1)[0]
    for cand in candidateroute:
        cand.added = False
        #print(cand.id)
    for j in range(0,len(candidateroute)):
        best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
        ApplyInsertion(newrt, best_inser)    
    best.route = rt.id
    best.route_list = newrt.route
    best.route_time = newrt.time
    
    best.capacity = newrt.capacity
    ApplyDestroy(best, route_list)

# export the solution to a txt file
def export_txt(route_list, total_prof):
    # open the file
    f = open("solution.txt","w+")
    print("Total Profit")
    # write the total profit
    f.write("Total Profit\n")
    print("%d" %total_prof)
    # write the total profit
    f.write("%d\n" %total_prof)
    # iterate through the routes
    for i in range(0,len(route_list)):
        # print the route id
        f.write("Route %d\n" %(i+1))
        print("Route %d" %(i+1))
        k = 0
        # iterate through the routes customers
        for c in route_list[i].route:
            k = k + 1
            if (k == len(route_list[i].route)):
                f.write("%d" %c.id)
            else:
                f.write("%d " %c.id)            
            print("%d" %c.id, end =" ")
        f.write("\n")
        print("")


# the function handles and calls them methods to solve the problem
def solveProblem():
    
    # create 6 empty routes
    route_list = getEmptyRoutes(6)
    # get the customer data from the csv file
    cust_list = getCustomers("instance.csv")
    # create the cost matrix, which is a 2D array containing the distance beteween each customer
    cost_matrix = getCost_Matrix(cust_list)
    # get a first solution using the minimum insertion algorithm and a clever weighted index
    solve(cust_list, route_list, cost_matrix)
    # DrawSolution(route_list, cust_list)
           
    
    candidates = generatePairs(cust_list)
    servedpairs=[]
    candidates2=[]
    
    # apply a combination of Tabu, Local Search and randomRemoval to further improve the solution
    for j in range(0,4):        
        # apply random removal to the solution
        randomRemoval(route_list[3],cost_matrix,20,route_list)
        randomRemoval(route_list[4],cost_matrix,40,route_list)  
        # apply local search to the solution: relocation    
        local_search.LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
        # check if we can further add any customers to the solution
        solve(cust_list, route_list, cost_matrix)        
           
        candidates = generatePairs(cust_list)
        servedpairs=[]
        candidates2=[]   
        candidates2 = generatePairs(cust_list)
        allservedpairs=[]
        allservedpairs=generateServedPairs(cust_list)    
        
        for r in route_list:
            servedpairs.append(generateServedPairs(r.route))
        # apply local search to the solution: swap
        local_search.LocalSearch(4, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)        
        # apply local search to the solution: relocation
        local_search.LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
        # check if we can further add any customers to the solution
        solve(cust_list, route_list, cost_matrix)
        # apply the tabu search heuristic to the solution
        TabuSearch(0, route_list, cost_matrix, cust_list)
               
        
        
        
    candidates = generatePairs(cust_list)
    servedpairs=[]
    candidates2=[]   
    candidates2 = generatePairs(cust_list)
    allservedpairs=[]
    allservedpairs=generateServedPairs(cust_list)
    
    
    for r in route_list:
        servedpairs.append(generateServedPairs(r.route))
       
    local_search.LocalSearch(4, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)    
    local_search.LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
    
    solve(cust_list, route_list, cost_matrix)
    
    # calculate the profit of the solution
    prof = calclulateProfitRoute(route_list)
    # calculate the total cost of the solution
    total_prof = calclulatetotalProfit(prof)
    
   
    export_txt(route_list, total_prof)
    DrawSolution(route_list, cust_list)


if __name__ == "__main__":
    solveProblem()