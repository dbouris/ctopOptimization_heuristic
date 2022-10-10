import csv
import math
from shutil import move
from typing import NewType
#from SolutionDrawer import *
import copy
from itertools import combinations
import pprint
import random
import timeit

# Creation of classes


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


def InitializeOperators(rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()


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
    



#  Methods



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


def getEmptyRoutes(trucks):
    apothiki = Customer(0,23.142,11.736,0,0,0,False)
    route_list = []

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


def calclulateProfitRoute(route_list):
    profit = []

    for i in route_list:
        prof = 0
        for k in i.route:
            prof += k.profit
        profit.append(prof)
    return profit

def calclulatetotalProfit(prof):
    total_prof = 0
    for i in prof:
        total_prof = total_prof +i
    return total_prof

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

def getServCost(route_list):
    serv_cost = []
    for i in route_list:
        cost = 0
        for k in i.route:
            cost = cost + k.serv_time
        serv_cost.append(cost)
    return serv_cost

def gettotalServCost(route_list, cost_matrix):
        c = 0
        for route in route_list:
            for j in range (0, len(route.route) - 1):
                a = route.route[j]
                b = route.route[j + 1]
                c += cost_matrix[a.id][b.id]
        return c

def getTimeInRoute(route, cost_matrix):
    c = 0
    for j in range (0, len(route) - 1):
        a = route[j]
        b = route[j + 1]
        c += cost_matrix[a.id][b.id]
        c += a.serv_time
    return c


def gettotalTime(cost_matrix, route):
    c = 0
    for j in range (0, len(route.route) - 1):
        a = route.route[j]
        b = route.route[j + 1]
        c += cost_matrix[a.id][b.id] + a.serv_time
    return c 
        




def DrawSolution(route_list, cust_list):
    SolDrawer.drawRoutes(route_list)
    SolDrawer.drawPointsUsed(cust_list)

def ApplySwapMoveTabu(sm, route_list, iterator):

    rt1 = route_list[sm.positionOfFirstRoute]
    rt2 = route_list[sm.positionOfSecondRoute]
    b1 = rt1.route[sm.positionOfFirstNode]
    b2 = rt2.route[sm.positionOfSecondNode]
    rt1.route[sm.positionOfFirstNode] = b2
    rt2.route[sm.positionOfSecondNode] = b1

    if (rt1 == rt2):
        rt1.time += sm.moveCost
    else:
        rt1.time += sm.timeChangeFirstRt
        rt2.time += sm.timeChangeSecondRt
        rt1.capacity = rt1.capacity - b1.demand + b2.demand
        rt2.capacity = rt2.capacity + b1.demand - b2.demand
        
    SetTabuIterator(b1, iterator)
    SetTabuIterator(b2, iterator)

def ApplySwapMove(sm, route_list):

    rt1 = route_list[sm.positionOfFirstRoute]
    rt2 = route_list[sm.positionOfSecondRoute]
    b1 = rt1.route[sm.positionOfFirstNode]
    b2 = rt2.route[sm.positionOfSecondNode]
    rt1.route[sm.positionOfFirstNode] = b2
    rt2.route[sm.positionOfSecondNode] = b1

    if (rt1 == rt2):
        rt1.time += sm.moveCost
    else:
        rt1.time += sm.timeChangeFirstRt
        rt2.time += sm.timeChangeSecondRt
        rt1.capacity = rt1.capacity - b1.demand + b2.demand
        rt2.capacity = rt2.capacity + b1.demand - b2.demand
        



def ApplyRelocationMoveTabu(rm, route_list, localSearchIterator):


        originRt = route_list[rm.originRoutePosition]
        targetRt = route_list[rm.targetRoutePosition]

        B = originRt.route[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.route[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.route.insert(rm.targetNodePosition, B)
            else:
                targetRt.route.insert(rm.targetNodePosition + 1, B)

            originRt.time += rm.moveCost
        else:
            del originRt.route[rm.originNodePosition]
            targetRt.route.insert(rm.targetNodePosition + 1, B)
            originRt.time += rm.timeChangeOriginRt
            targetRt.time += rm.timeChangeTargetRt
            originRt.capacity -= B.demand
            targetRt.capacity += B.demand

        SetTabuIterator(B,localSearchIterator)

# apply the relocation move on our current solution
def ApplyRelocationMove(rm, route_list):

        # get the origin and target route
        originRt = route_list[rm.originRoutePosition]
        targetRt = route_list[rm.targetRoutePosition]
        # get the node to be relocated
        B = originRt.route[rm.originNodePosition]
        # if the origin and target route are the same
        if originRt == targetRt:
            # delete the node from the origin route
            # the deletion causes the list to be shifted
            del originRt.route[rm.originNodePosition]
            # check if the node is inserted before or after the target node to avoid the shifting problem
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.route.insert(rm.targetNodePosition, B)
            else:
                targetRt.route.insert(rm.targetNodePosition + 1, B)
            # update the time of the target route
            originRt.time += rm.moveCost
        # if the origin and target route are different
        else:
            # delete the node from the origin route
            del originRt.route[rm.originNodePosition]
            # insert the node in the target route
            targetRt.route.insert(rm.targetNodePosition + 1, B)
            # update time and capacity of the origin and target route
            originRt.time += rm.timeChangeOriginRt
            targetRt.time += rm.timeChangeTargetRt
            originRt.capacity -= B.demand
            targetRt.capacity += B.demand

        

def StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
    sm.positionOfFirstRoute = firstRouteIndex
    sm.positionOfSecondRoute = secondRouteIndex
    sm.positionOfFirstNode = firstNodeIndex
    sm.positionOfSecondNode = secondNodeIndex
    sm.timeChangeFirstRt = costChangeFirstRoute
    sm.timeChangeSecondRt = costChangeSecondRoute
    sm.moveCost = moveCost

# store the best relocation move in the RelocationMove object
# keep track of the route and node positions
# update the move cost on both the target and origin routes
def StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.timeChangeOriginRt = originRtCostChange
        rm.timeChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

def FindBestRelocationMoveTabu(rm, localSearchIterator, route_list, cost_matrix, bestSolution):
        for originRouteIndex in range(0, len(route_list)):
            rt1 = route_list[originRouteIndex]
            for targetRouteIndex in range (0, len(route_list)):
                rt2 = route_list[targetRouteIndex]
                #print("CHECKING ORIGIN: ", originRouteIndex, "TARGET: ", targetRouteIndex)
                for originNodeIndex in range (1, len(rt1.route) - 1):
                    for targetNodeIndex in range (0, len(rt2.route) - 1):
                        

                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.route[originNodeIndex - 1]
                        B = rt1.route[originNodeIndex]
                        C = rt1.route[originNodeIndex + 1]

                        F = rt2.route[targetNodeIndex]
                        G = rt2.route[targetNodeIndex + 1]

                        #print("SEND ", B.id, "TO: ", F.id)

                        if originRouteIndex != targetRouteIndex:
                            if rt2.capacity + B.demand > 150:
                                #print("CAPACITY ISSUE AT ROUTE 2")
                                continue

                        costAdded = cost_matrix[A.id][C.id] + cost_matrix[F.id][B.id] + cost_matrix[B.id][G.id]
                        costRemoved = cost_matrix[A.id][B.id] + cost_matrix[B.id][C.id] + cost_matrix[F.id][G.id]

                        originRtCostChange = cost_matrix[A.id][C.id] - cost_matrix[A.id][B.id] - cost_matrix[B.id][C.id] 
                        targetRtCostChange = cost_matrix[F.id][B.id] + cost_matrix[B.id][G.id] - cost_matrix[F.id][G.id] + rt1.route[originNodeIndex].serv_time

                        if rt2.time + targetRtCostChange > 200:
                            continue 
                        
                       
                       
                        moveCost = costAdded - costRemoved
                        #print(moveCost)
                        
                        if (MoveIsTabu(B, localSearchIterator, moveCost, route_list, cost_matrix, bestSolution)):
                            
                            continue
                        
                        if (moveCost < rm.moveCost):
                            StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)
#  find the best relocation move for the current solution   
def FindBestRelocationMove(rm, route_list, cost_matrix):
        # iterate over all the routes in the solution as the origin route
        for originRouteIndex in range(0, len(route_list)):
            # get the origin route
            rt1 = route_list[originRouteIndex]
            # iterate over all the routes in the solution as the target route
            for targetRouteIndex in range (0, len(route_list)):
                # get the target route
                rt2 = route_list[targetRouteIndex]
                # iterate over all the nodes in the origin route, as the origin node
                for originNodeIndex in range (1, len(rt1.route) - 1):
                    # iterate over all the nodes in the target route, as the target node
                    for targetNodeIndex in range (0, len(rt2.route) - 1):
                        
                        # continue if the origin and target nodes are the same in the same route, or if they are consecutive
                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue
                        # get the node to be relocated, the node before and after it
                        A = rt1.route[originNodeIndex - 1]
                        B = rt1.route[originNodeIndex]
                        C = rt1.route[originNodeIndex + 1]
                        # get the target node and the node after it
                        F = rt2.route[targetNodeIndex]
                        G = rt2.route[targetNodeIndex + 1]

                        # if the relocation is between different routes, check if the target route has enough capacity
                        if originRouteIndex != targetRouteIndex:
                            # if the capacity of the target route is exceeded, continue
                            if rt2.capacity + B.demand > 150:
                                continue
                        # calculate the cost of the move
                        costAdded = cost_matrix[A.id][C.id] + cost_matrix[F.id][B.id] + cost_matrix[B.id][G.id]
                        costRemoved = cost_matrix[A.id][B.id] + cost_matrix[B.id][C.id] + cost_matrix[F.id][G.id]
                        # calculate the cost change of the origin and target routes
                        originRtCostChange = cost_matrix[A.id][C.id] - cost_matrix[A.id][B.id] - cost_matrix[B.id][C.id] 
                        targetRtCostChange = cost_matrix[F.id][B.id] + cost_matrix[B.id][G.id] - cost_matrix[F.id][G.id] + rt1.route[originNodeIndex].serv_time
                        # check if the time of the target route is not exceeded
                        if rt2.time + targetRtCostChange > 200:
                            continue 
                        # calculate the cost of the move
                        moveCost = costAdded - costRemoved
                        #print(moveCost)
                        
                        # if the move cost is better than the current best move, store it
                        if (moveCost < rm.moveCost):
                            StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)
        


def FindBestSwapMoveTabu(sm, route_list, cost_matrix, localSearchIterator, bestSolution):
        for firstRouteIndex in range(0, len(route_list)):
            rt1 = route_list[firstRouteIndex]
            for secondRouteIndex in range (firstRouteIndex,len(route_list)):
                #print("CHECKING ROUTE: ", firstRouteIndex, "WITH: ", secondRouteIndex)
                rt2 = route_list[secondRouteIndex]
                for firstNodeIndex in range (1, len(rt1.route) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range (startOfSecondNodeIndex, len(rt2.route) - 1):

                        
                        a1 = rt1.route[firstNodeIndex - 1]
                        b1 = rt1.route[firstNodeIndex]
                        c1 = rt1.route[firstNodeIndex + 1]

                        a2 = rt2.route[secondNodeIndex - 1]
                        b2 = rt2.route[secondNodeIndex]
                        c2 = rt2.route[secondNodeIndex + 1]

                        #print("CHECKING:", b1.id , "WITH: ", b2.id)
                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][b2.id] + cost_matrix[b2.id][c2.id]
                                costAdded = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][b1.id] + cost_matrix[b1.id][c2.id]
                                moveCost = costAdded - costRemoved


                            else:

                                costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                                costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                                costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                                costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            
                            #check for time violation
                            if rt1.time + moveCost > 200:
                                continue
                        
                        else:
                            if rt1.capacity - b1.demand + b2.demand > 150:
                                #print("DOES NOT FIT IN R1")
                                continue
                            if rt2.capacity - b2.demand + b1.demand > 150:
                                #print("DOES NOT FIT IN R2")
                                continue

                            costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                            costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                            costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                            costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]

                            costChangeFirstRoute = costAdded1 - costRemoved1  + b2.serv_time - b1.serv_time
                            costChangeSecondRoute = costAdded2 - costRemoved2 + b1.serv_time - b2.serv_time
                            
                            if rt1.time + costChangeFirstRoute > 200:
                                #print("TIME 1: ", rt1.time + costChangeFirstRoute)
                                #print("TIME VIOLATION IN ROUTE 1")
                                continue

                            if rt2.time + costChangeSecondRoute > 200:
                                #print("TIME 1: ", rt2.time + costChangeSecondRoute)
                                #print("TIME VIOLATION IN ROUTE 2")
                                continue

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            

                        if MoveIsTabu(b1, localSearchIterator, moveCost, route_list, cost_matrix, bestSolution) or MoveIsTabu(b2, localSearchIterator, moveCost, route_list, cost_matrix, bestSolution):
                            
                            continue

                        if moveCost < sm.moveCost:
                            StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

def FindBestSwapMove(sm, route_list, cost_matrix):
        for firstRouteIndex in range(0, len(route_list)):
            rt1 = route_list[firstRouteIndex]
            for secondRouteIndex in range (firstRouteIndex,len(route_list)):
                #print("CHECKING ROUTE: ", firstRouteIndex, "WITH: ", secondRouteIndex)
                rt2 = route_list[secondRouteIndex]
                for firstNodeIndex in range (1, len(rt1.route) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range (startOfSecondNodeIndex, len(rt2.route) - 1):

                        
                        a1 = rt1.route[firstNodeIndex - 1]
                        b1 = rt1.route[firstNodeIndex]
                        c1 = rt1.route[firstNodeIndex + 1]

                        a2 = rt2.route[secondNodeIndex - 1]
                        b2 = rt2.route[secondNodeIndex]
                        c2 = rt2.route[secondNodeIndex + 1]

                        #print("CHECKING:", b1.id , "WITH: ", b2.id)
                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][b2.id] + cost_matrix[b2.id][c2.id]
                                costAdded = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][b1.id] + cost_matrix[b1.id][c2.id]
                                moveCost = costAdded - costRemoved


                            else:

                                costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                                costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                                costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                                costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            
                            #check for time violation
                            if rt1.time + moveCost > 200:
                                continue
                        
                        else:
                            if rt1.capacity - b1.demand + b2.demand > 150:
                                #print("DOES NOT FIT IN R1")
                                continue
                            if rt2.capacity - b2.demand + b1.demand > 150:
                                #print("DOES NOT FIT IN R2")
                                continue

                            costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                            costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                            costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                            costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]

                            costChangeFirstRoute = costAdded1 - costRemoved1  + b2.serv_time - b1.serv_time
                            costChangeSecondRoute = costAdded2 - costRemoved2 + b1.serv_time - b2.serv_time
                            
                            if rt1.time + costChangeFirstRoute > 200:
                                #print("TIME 1: ", rt1.time + costChangeFirstRoute)
                                #print("TIME VIOLATION IN ROUTE 1")
                                continue

                            if rt2.time + costChangeSecondRoute > 200:
                                #print("TIME 1: ", rt2.time + costChangeSecondRoute)
                                #print("TIME VIOLATION IN ROUTE 2")
                                continue

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            

                        if moveCost < sm.moveCost:
                            StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)


def CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):

        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.route[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.capacity - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.route[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.capacity - rt2FirstSegmentLoad
        # print("ROUTE 1 NEW CAPACITY: ", rt1FirstSegmentLoad + rt2SecondSegmentLoad)
        # print("ROUTE 2 NEW CAPACITY: ", rt2FirstSegmentLoad + rt1SecondSegmentLoad)
        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > 150):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > 150):
            return True

        return False

def StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
    top.positionOfFirstRoute = rtInd1
    top.positionOfSecondRoute = rtInd2
    top.positionOfFirstNode = nodeInd1
    top.positionOfSecondNode = nodeInd2
    top.moveCost = moveCost


def FindBestTwoOptMoveTabu(top, route_list, cost_matrix, iterator, bestSolution):
        for rtInd1 in range(0, len(route_list)):
            rt1 = route_list[rtInd1]
            for rtInd2 in range(rtInd1, len(route_list)):
                rt2 = route_list[rtInd2]
                #print("CHECKING ROUTE: ", rtInd1, "WITH: ", rtInd2)
                for nodeInd1 in range(0, len(rt1.route) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.route) - 1):
                        moveCost = 10 ** 9

                        A = rt1.route[nodeInd1]
                        B = rt1.route[nodeInd1 + 1]
                        K = rt2.route[nodeInd2]
                        L = rt2.route[nodeInd2 + 1]
                        
                        #print("WORKING FOR NODES: ", A.id, "AND ", K.id)

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.route) - 2:
                                continue
                            costAdded = cost_matrix[A.id][K.id] + cost_matrix[B.id][L.id]
                            costRemoved = cost_matrix[A.id][B.id] + cost_matrix[K.id][L.id]
                            moveCost = costAdded - costRemoved
                            # check time violations
                            if rt1.time + moveCost > 200:
                                continue



                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.route) - 2 and  nodeInd2 == len(rt2.route) - 2:
                                continue

                            if CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                #print("CAPACITY VIOLATION")
                                continue
                            costAdded = cost_matrix[A.id][L.id] + cost_matrix[B.id][K.id]
                            costRemoved = cost_matrix[A.id][B.id] + cost_matrix[K.id][L.id]
                            moveCost = costAdded - costRemoved
                            
                            #check time constraints
                            relocatedSegmentOfRt1 = rt1.route[nodeInd1 + 1 :]
                            relocatedSegmentOfRt2 = rt2.route[nodeInd2 + 1 :]

                            TimeReloc1 = getTimeInRoute(relocatedSegmentOfRt1, cost_matrix)
                            remaining1 = rt1.time - TimeReloc1

                            TimeReloc2 = getTimeInRoute(relocatedSegmentOfRt2, cost_matrix)
                            remaining2 = rt2.time - TimeReloc2

                            if remaining1 + TimeReloc2 - cost_matrix[A.id][B.id] + cost_matrix[A.id][L.id] > 200:
                                continue
                            if remaining2 + TimeReloc1 - cost_matrix[K.id][L.id] +  cost_matrix[B.id][K.id] > 200:
                                continue

                        #print(moveCost)
                        if MoveIsTabu(A, iterator, moveCost, route_list, cost_matrix, bestSolution) or MoveIsTabu(K, iterator, moveCost,route_list, cost_matrix, bestSolution):
                            
                            continue   

                        if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                            StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)


def FindBestTwoOptMove(top, route_list, cost_matrix):
        for rtInd1 in range(0, len(route_list)):
            rt1 = route_list[rtInd1]
            for rtInd2 in range(rtInd1, len(route_list)):
                rt2 = route_list[rtInd2]
                #print("CHECKING ROUTE: ", rtInd1, "WITH: ", rtInd2)
                for nodeInd1 in range(0, len(rt1.route) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.route) - 1):
                        moveCost = 10 ** 9

                        A = rt1.route[nodeInd1]
                        B = rt1.route[nodeInd1 + 1]
                        K = rt2.route[nodeInd2]
                        L = rt2.route[nodeInd2 + 1]
                        
                        #print("WORKING FOR NODES: ", A.id, "AND ", K.id)

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.route) - 2:
                                continue
                            costAdded = cost_matrix[A.id][K.id] + cost_matrix[B.id][L.id]
                            costRemoved = cost_matrix[A.id][B.id] + cost_matrix[K.id][L.id]
                            moveCost = costAdded - costRemoved
                            # check time violations
                            if rt1.time + moveCost > 200:
                                continue



                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.route) - 2 and  nodeInd2 == len(rt2.route) - 2:
                                continue

                            if CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                #print("CAPACITY VIOLATION")
                                continue
                            costAdded = cost_matrix[A.id][L.id] + cost_matrix[B.id][K.id]
                            costRemoved = cost_matrix[A.id][B.id] + cost_matrix[K.id][L.id]
                            moveCost = costAdded - costRemoved
                            
                            #check time constraints
                            relocatedSegmentOfRt1 = rt1.route[nodeInd1 + 1 :]
                            relocatedSegmentOfRt2 = rt2.route[nodeInd2 + 1 :]

                            TimeReloc1 = getTimeInRoute(relocatedSegmentOfRt1, cost_matrix)
                            remaining1 = rt1.time - TimeReloc1

                            TimeReloc2 = getTimeInRoute(relocatedSegmentOfRt2, cost_matrix)
                            remaining2 = rt2.time - TimeReloc2

                            if remaining1 + TimeReloc2 - cost_matrix[A.id][B.id] + cost_matrix[A.id][L.id] > 200:
                                continue
                            if remaining2 + TimeReloc1 - cost_matrix[K.id][L.id] +  cost_matrix[B.id][K.id] > 200:
                                continue

                        #print(moveCost)
                        if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                            StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)


def ApplyTwoOptMoveTabu(top, route_list, cost_matrix, iterator):
    rt1 = route_list[top.positionOfFirstRoute]
    rt2 = route_list[top.positionOfSecondRoute]

    if rt1 == rt2:
        # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
        reversedSegment = reversed(rt1.route[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
        #lst = list(reversedSegment)
        #lst2 = list(reversedSegment)
        rt1.route[top.positionOfFirstNode + 1 : top.positionOfSecondNode + 1] = reversedSegment

        #reversedSegmentList = list(reversed(rt1.route[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
        #rt1.route[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

        SetTabuIterator(rt1.route[top.positionOfFirstNode], iterator)
        SetTabuIterator(rt1.route[top.positionOfSecondNode], iterator)

        rt1.time += top.moveCost

    else:
        #slice with the nodes from position top.positionOfFirstNode + 1 onwards
        relocatedSegmentOfRt1 = rt1.route[top.positionOfFirstNode + 1 :]

        #slice with the nodes from position top.positionOfFirstNode + 1 onwards
        relocatedSegmentOfRt2 = rt2.route[top.positionOfSecondNode + 1 :]

        del rt1.route[top.positionOfFirstNode + 1 :]
        del rt2.route[top.positionOfSecondNode + 1 :]

        rt1.route.extend(relocatedSegmentOfRt2)
        rt2.route.extend(relocatedSegmentOfRt1)

        SetTabuIterator(rt1.route[top.positionOfFirstNode], iterator)
        SetTabuIterator(rt2.route[top.positionOfSecondNode], iterator)

        #lathooooos
        UpdateRouteCostAndLoad(rt1, cost_matrix)
        UpdateRouteCostAndLoad(rt2, cost_matrix)

def ApplyTwoOptMove(top, route_list, cost_matrix):
    rt1 = route_list[top.positionOfFirstRoute]
    rt2 = route_list[top.positionOfSecondRoute]

    if rt1 == rt2:
        # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
        reversedSegment = reversed(rt1.route[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
        #lst = list(reversedSegment)
        #lst2 = list(reversedSegment)
        rt1.route[top.positionOfFirstNode + 1 : top.positionOfSecondNode + 1] = reversedSegment

        #reversedSegmentList = list(reversed(rt1.route[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
        #rt1.route[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

        rt1.time += top.moveCost

    else:
        #slice with the nodes from position top.positionOfFirstNode + 1 onwards
        relocatedSegmentOfRt1 = rt1.route[top.positionOfFirstNode + 1 :]

        #slice with the nodes from position top.positionOfFirstNode + 1 onwards
        relocatedSegmentOfRt2 = rt2.route[top.positionOfSecondNode + 1 :]

        del rt1.route[top.positionOfFirstNode + 1 :]
        del rt2.route[top.positionOfSecondNode + 1 :]

        rt1.route.extend(relocatedSegmentOfRt2)
        rt2.route.extend(relocatedSegmentOfRt1)

        #lathooooos
        UpdateRouteCostAndLoad(rt1, cost_matrix)
        UpdateRouteCostAndLoad(rt2, cost_matrix)



def UpdateRouteCostAndLoad(rt, cost_matrix):
    tc = 0
    tl = 0
    for i in range(0, len(rt.route) - 1):
        A = rt.route[i]
        B = rt.route[i+1]
        tc += cost_matrix[A.id][B.id]
        if i !=0:
            tc += A.serv_time
            tl += A.demand
    rt.capacity = tl
    rt.time = tc

# the LocalSearch function contains local search operators which are applied on the solution
# operator 0: Relocation Move
# operator 1: Swap Move
# operator 2: 2-opt Move
# operator 3: Pair Insertion Move
# operator 4: 2-Pair Exchange Move
# operator 5: TwoServedOneUnservedMove
# operator 6: OneServedOneUnservedMove
def LocalSearch(operator, route_list, cost_matrix, pairlist,pairlist2, pairserved,c_list):
        
        # create a copy of the solution to be used in the local search to avoid changing the original one
        bestSolution = copy.deepcopy(route_list)
        terminationCondition = False
        localSearchIterator = 0
        reloc = 0
        swaps = 0
        opt = 0 

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        count=0
        # while the termination condition is not met, apply the local search operators
        while terminationCondition is False:
            # initialize the operators object
            InitializeOperators(rm, sm, top)
            
            # relocation move: get a customer and change its position in the route
            if operator == 0:
                # find the best relocation move and store it in the rm object
                FindBestRelocationMove(rm, route_list, cost_matrix)
                # if the best relocation move improves the solution, apply it
                if rm.moveCost < 0:
                    ApplyRelocationMove(rm, route_list)
                   
                    reloc = reloc + 1
                else:
                    # there cannot be any further improvement using the relocation move operator
                    terminationCondition = True
            # swap move: get two customers and change their positions in the route
            elif operator == 1:
                # find the best swap move and store it in the sm object
                FindBestSwapMove(sm ,route_list, cost_matrix)
                # if the best swap move improves the solution, apply it
                if sm.moveCost < 0:
                    ApplySwapMove(sm, route_list)
                    
                    swaps = swaps +1
                else:
                    # there cannot be any further improvement using the swap move operator
                    terminationCondition = True
            # 2-opt move: get two customers and reverse the segment between them: it is used to untangle the routes
            elif operator == 2:
                # find the best 2-opt move and store it in the top object
                FindBestTwoOptMove(top,route_list, cost_matrix)
                # if the best 2-opt move improves the solution, apply it
                if top.moveCost < 0:
                    ApplyTwoOptMove(top, route_list, cost_matrix)
                    
                    opt = opt + 1
                else:
                    # there cannot be any further improvement using the 2-opt move operator
                    terminationCondition = True
            # pair insertion move: get a pair of customers and insert it in the route
            elif operator == 3:
                best: PairInsertionMove = PairInsertion(pairlist, route_list, cost_matrix)
                if best.profit_added > 0:
                        ApplyPairMove(best, route_list)
                       
                        opt = opt + 1
                else:
                    terminationCondition = True
            # 2-pair exchange move: get two pairs of customers and exchange them in the route 
            elif operator == 4:
                best: PairInsertionMove = TwoPairExchange(route_list, cost_matrix, pairlist2, pairserved)
                if best.profit_added > 0:
                        ApplyPairMoveServed(best, route_list)
                        opt = opt + 1
                else:
                    terminationCondition = True
            # two served one unserved move: replace two served customers with one unserved customer
            elif operator == 5:
                # find the best two served one unserved move and store it in the PairInsertionMove object
                best: PairInsertionMove = TwoServedOneUnservedExchange(route_list, cost_matrix, c_list, pairserved)
                # if the best two served one unserved move improves the solution, apply it
                if best.profit_added > 0:
                        ApplyPairMoveOneUnserved(best,route_list)
                        opt = opt + 1
                else:
                    # there cannot be any further improvement using the two served one unserved move operator
                    terminationCondition = True
            # one served one unserved move: replace one served customer with one unserved customer
            elif operator == 6:
                # find the best one served one unserved move and store it in the PairInsertionMove object
                best: PairInsertionMove = OneServedOneUnservedExchange(route_list, cost_matrix, c_list)
                # if the best one served one unserved move improves the solution, apply it
                if best.profit_added > 0:
                        count=count+1
                        ApplyOneNodeMove(best, route_list)
                        # add an upper bound to the number of iterations of this move 
                        opt = opt + 1
                        if count>3:
                          terminationCondition = True      
                else:
                    # there cannot be any further improvement using the one served one unserved move operator
                    terminationCondition = True
                    

            


           
            bestSolution = copy.deepcopy(route_list)
            prof = calclulateProfitRoute(bestSolution)
            total_prof = calclulatetotalProfit(prof)
            
            

            localSearchIterator = localSearchIterator + 1
       


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


Max_Time = 200
Max_Capacity = 150
Max_Profit = 35


#weigths
profit_weight = 0.56
demand_weight = 0.12
time_weight = 0.32


def generatePairs(cust_list):
    customers = []
    for x in cust_list:
        if (x.added == False):
            customers.append(x)

    combinationPairs = combinations(customers, 2)

    pairs = []
    for x in combinationPairs:
        candidate = CandidatePairs(x)
        pairs.append(candidate)

    return pairs

def generateServedPairs(cust_list):
    customers = []
    for x in cust_list:
        if (x.added == True):
            customers.append(x)

    combinationPairs = combinations(customers, 2)

    pairs = []
    for x in combinationPairs:
        candidate = CandidatePairs(x)
        pairs.append(candidate)

    return pairs


def IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix):
    best_insertion = OneRouteBi()
    for customer in candidateroute:
        if customer.added == False:

            for j in range(0, len(newrt.route) - 1):
                A = newrt.route[j].id
                B = newrt.route[j + 1].id
            
                costAdded = cost_matrix[A][customer.id] + cost_matrix[customer.id][B]
                costRemoved = cost_matrix[A][B]
                
                trialCost = costAdded - costRemoved + customer.serv_time

                    
                if trialCost < best_insertion.time:
                    best_insertion.customer = customer
                    best_insertion.position = j
                    best_insertion.time = trialCost 
                    
        else:
            continue
    return best_insertion



def ApplyInsertion(newrt, best):
    #updates time and capacity of the route
    newrt.capacity += best.customer.demand
    newrt.time +=  best.time 

    #adds the node to its new position
    r = newrt.route
    r.insert(best.position+1,best.customer)
    newrt.route = r

    best.customer.added = True
    

def ApplyPairMove(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change
    best.pair_added.customers[0].added = True
    best.pair_added.customers[1].added = True
    best.nodetoremove.added = False

def ApplyPairMoveServed(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change
    best.pair_added.customers[0].added = True
    best.pair_added.customers[1].added = True
    best.pservedremove.customers[0].added=False
    best.pservedremove.customers[1].added=False
    
def ApplyPairMoveOneUnserved(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change    
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
    #best.nodetoadd.added = True   
    #best.nodetoremove.added = False




def PairInsertion(pairlist, route_list, cost_matrix):
    
    best = PairInsertionMove()
    for pair in pairlist:
        #print("THE PAIR EVALUATING IS: ", pair.customers[0].id, pair.customers[1].id)
        if pair.customers[0].added == False and pair.customers[1].added == False:
            for route in route_list:
                rt = route.route
                #print("CHECKING ROUTE: ")
                #for i in rt:
                #    print(i.id ,end = " ")
                # print()

                for nodeIndextoremove in range(1,len(route.route)-1):
                    #print("NODE TO REMOVE IS: ", rt[nodeIndextoremove].id)
                    #check if the profit of the pair is better
                    if pair.totalProfit >  rt[nodeIndextoremove].profit:
                        #check if the pair can fit in the route demand wise
                        if route.capacity - rt[nodeIndextoremove].demand + pair.totalDemand > 150:
                            #print("CAPACITY ISSUE")
                            continue
                        if route.time - rt[nodeIndextoremove].serv_time + pair.totalServiceTime > 200 :
                            #print("CAPACITY ISSUE")
                            continue
                        
                        candidateroute = route.route[1:len(route.route)-1]
                        candidateroute.remove(rt[nodeIndextoremove])
                        for k in pair.customers:
                            candidateroute.append(k)
                        

                        newrt = getEmptyRoutes(1)[0]
                        #print("CANDIDATE ROUTE: ")
                        for i in candidateroute:
                            i.added = False
                            #print(i.id, end = " ")
                        #print()
                        
                        for i in range(0,len(candidateroute)):
                            best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                            ApplyInsertion(newrt, best_inser)

                        pair.customers[0].added = False
                        pair.customers[1].added = False
                        
                        
                        #check if the newroute's time is OK
                        
                        # print("THE NEW ROUTE TO EVALUATE IS: ")
                        # for i in newrt.route:
                        #     print(i.id ,end = " ")
                        # print()
                        profit =  pair.totalProfit - rt[nodeIndextoremove].profit 

                        if newrt.time > 200:
                            #print(gettotalTime(cost_matrix, newrt))
                            # print("THE TIME IS: ", newrt.time)
                            # print("                                                             THE NEW ROUTES TIME IS NOT OK ")
                            continue
                        
                        #print("                                                                     WE HAVE A NEW ROUTE")
                        if profit > best.profit_added:
                            best.profit_added = profit
                            best.route = route.id
                            best.route_list = newrt.route
                            best.route_time = newrt.time
                            best.pair_added = pair
                            best.nodetoremove = rt[nodeIndextoremove]
                            best.capacity_change = pair.customers[0].demand + pair.customers[1].demand - rt[nodeIndextoremove].demand
                            
    return best
           
    
def TwoPairExchange(route_list, cost_matrix, pairlist, pairserved): 
    best = PairInsertionMove()
    for pair in pairlist:       
        if pair.customers[0].added == False and pair.customers[1].added == False:
            for i in range(0,len(route_list)-1):                                
                for pserved in pairserved[i]:
                    if pserved.customers[0].added == True and pserved.customers[1].added == True:
                         if pair.totalProfit >  pserved.totalProfit: 
                             
                             if route_list[i].capacity - pserved.totalDemand + pair.totalDemand > 150:
                                 #print("CAPACITY ISSUE")
                                 continue
                             
                             if route_list[i].time - pserved.totalServiceTime + pair.totalServiceTime > 200 :
                                 #print("CAPACITY ISSUE")
                                 continue
                            
                             candidateroute = route_list[i].route[1:len(route_list[i].route)-1] 
                             if ( not pserved.customers[0] in route_list[i].route) or (not pserved.customers[1] in route_list[i].route):
                                 continue
                             candidateroute.remove(pserved.customers[0])
                             candidateroute.remove(pserved.customers[1])                             
                             for k in pair.customers:
                                 candidateroute.append(k)
                             newrt = getEmptyRoutes(1)[0]
                             for c in candidateroute:
                                 c.added = False
                             for j in range(0,len(candidateroute)):
                                 best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                                 ApplyInsertion(newrt, best_inser)
                             pair.customers[0].added = False
                             pair.customers[1].added = False
                             profit =  pair.totalProfit - pserved.totalProfit
                            
                             if newrt.time > 200:
                                 continue                             
                             if profit > best.profit_added:                                 
                                 best.profit_added = profit 
                                 best.route = route_list[i].id
                                 best.route_list = newrt.route
                                 best.route_time = newrt.time
                                 best.pair_added = pair
                                 best.pservedremove = pserved
                                 best.capacity_change = pair.customers[0].demand + pair.customers[1].demand - (pserved.customers[0].demand + pserved.customers[1].demand)
                                 
    return best


def OneServedOneUnservedExchange(route_list, cost_matrix, c_list): 
    best = PairInsertionMove()
    for c in c_list:       
        if c.added == False:
            for rt in route_list:
                for served in rt.route:
                    if served.added == True:
                        if c.profit >  served.profit:
                             if rt.capacity - served.demand + c.demand > 150:
                                 #print("CAPACITY ISSUE")
                                 continue
                             
                             if rt.time - served.serv_time + c.serv_time > 200 :
                                 #print("CAPACITY ISSUE")
                                 continue
                             
                             candidateroute = rt.route[1:len(rt.route)-1]                             
                             candidateroute.remove(served)
                             candidateroute.append(c)
                             newrt = getEmptyRoutes(1)[0]
                             for cand in candidateroute:
                                 cand.added = False
                             for j in range(0,len(candidateroute)):
                                 best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                                 ApplyInsertion(newrt, best_inser)
                             c.added=False
                             profit =  c.profit - served.profit                           
                             if newrt.time > 200:                                 
                                 continue
                             if profit > best.profit_added:                                 
                                 best.profit_added = profit 
                                 best.route = rt.id
                                 best.route_list = newrt.route
                                 best.route_time = newrt.time
                                 best.nodetoadd = c
                                 best.nodetoremove = served
                                 best.capacity_change = c.demand  - served.demand
                                                    
                        
                
                               
                
    return best



def TwoServedOneUnservedExchange(route_list, cost_matrix, c_list, pairserved): 
    best = PairInsertionMove()
    for c in c_list:       
        if c.added == False:
            for i in range(0,len(route_list)-1):                                
                for pserved in pairserved[i]:
                    if pserved.customers[0].added == True and pserved.customers[1].added == True:
                         if c.profit >  pserved.totalProfit: 
                             if route_list[i].capacity - pserved.totalDemand + c.demand > 150:
                                 #print("CAPACITY ISSUE")
                                 continue
                             
                             if route_list[i].time - pserved.totalServiceTime + c.serv_time > 200 :
                                 #print("CAPACITY ISSUE")
                                 continue
                             candidateroute = route_list[i].route[1:len(route_list[i].route)-1]                             
                             candidateroute.remove(pserved.customers[0])
                             candidateroute.remove(pserved.customers[1]) 
                             
                             candidateroute.append(c)
                             newrt = getEmptyRoutes(1)[0]
                             for cand in candidateroute:
                                 cand.added = False
                             for j in range(0,len(candidateroute)):
                                 best_inser = IdentifyMinimumCostInsertionInRoute(newrt,candidateroute, cost_matrix)
                                 ApplyInsertion(newrt, best_inser)
                             c.added=False
                             profit =  c.profit - pserved.totalProfit                             
                             if newrt.time > 200:                                 
                                 continue 
                             if profit > best.profit_added:                                 
                                 best.profit_added = profit 
                                 best.route = route_list[i].id
                                 best.route_list = newrt.route
                                 best.route_time = newrt.time
                                 best.nodetoadd = c
                                 best.pservedremove = pserved
                                 best.capacity_change = c.demand  - (pserved.customers[0].demand + pserved.customers[1].demand)                           
                                 
    return best
     
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

def VND(route_list, cost_matrix):
        bestSolution = copy.deepcopy(route_list)
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        k = 0

        while k <= kmax:
            InitializeOperators(rm, sm, top)
            if k == 0:
                FindBestRelocationMove(rm, route_list, cost_matrix)
               
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    ApplyRelocationMove(rm, route_list)
                   
                    
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            elif k == 1:
                FindBestSwapMove(sm ,route_list, cost_matrix)
               
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    ApplySwapMove(sm, route_list)
                   
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            elif k == 2:
                FindBestTwoOptMove(top,route_list, cost_matrix)
               
                if top.positionOfFirstRoute is not None and top.moveCost < 0:
                    ApplyTwoOptMove(top, route_list, cost_matrix)
                    
                    rt_time, rt_load, rt_profit = calculate_route_details(route_list[top.positionOfFirstRoute].route, cost_matrix)
                    # if rt_time > 200:
                    #     print("TIME VIOLATION")
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1

            bestSolution = copy.deepcopy(route_list)
            prof = calclulateProfitRoute(bestSolution)
            total_prof = calclulatetotalProfit(prof)
          

            
        


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
        operator = random.randint(0,2)
        InitializeOperators(rm, sm, top)
        
        # Relocations
        if operator == 0:
            FindBestRelocationMoveTabu(rm, localSearchIterator, route_list, cost_matrix, bestSolution)
            if rm.originRoutePosition is not None:
                ApplyRelocationMoveTabu(rm, route_list, localSearchIterator)
                
                
        # Swaps
        elif operator == 1:
            FindBestSwapMoveTabu(sm,route_list, cost_matrix, localSearchIterator, bestSolution)
            if sm.positionOfFirstRoute is not None:
                ApplySwapMoveTabu(sm, route_list, localSearchIterator)
                
        elif operator == 2:
            FindBestTwoOptMoveTabu(top,route_list, cost_matrix, localSearchIterator, bestSolution)
            if top.positionOfFirstRoute is not None:
                ApplyTwoOptMoveTabu(top,route_list, cost_matrix, localSearchIterator)
                

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

def MoveIsTabu(n, iterator, moveCost, route_list, cost_matrix, bestSolution):
        if moveCost + getTransferCost(route_list, cost_matrix) < getTransferCost(bestSolution, cost_matrix) - 0.001:
            return False
        if iterator < n.isTabuTillIterator:
            return True
        return False

def SetTabuIterator(n, iterator):
    # n.isTabuTillIterator = iterator + self.tabuTenure
    n.isTabuTillIterator = iterator + random.randint(50, 60)



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
    #best.nodetoadd = c
    #best.pservedremove = pserved
    
    best.capacity = newrt.capacity
    ApplyDestroy(best, route_list)





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
           
    
    candidates = generatePairs(cust_list)
    servedpairs=[]
    candidates2=[]
    
  
    for j in range(0,4):        
        randomRemoval(route_list[3],cost_matrix,20,route_list)
        randomRemoval(route_list[4],cost_matrix,40,route_list)      
        LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
        solve(cust_list, route_list, cost_matrix)        
           
        candidates = generatePairs(cust_list)
        servedpairs=[]
        candidates2=[]   
        candidates2 = generatePairs(cust_list)
        allservedpairs=[]
        allservedpairs=generateServedPairs(cust_list)    
        
        for r in route_list:
            servedpairs.append(generateServedPairs(r.route))
            
        LocalSearch(4, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)        
        LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
        solve(cust_list, route_list, cost_matrix)
        TabuSearch(0, route_list, cost_matrix, cust_list)
               
        
        
        
    candidates = generatePairs(cust_list)
    servedpairs=[]
    candidates2=[]   
    candidates2 = generatePairs(cust_list)
    allservedpairs=[]
    allservedpairs=generateServedPairs(cust_list)
    
    
    for r in route_list:
        servedpairs.append(generateServedPairs(r.route))
       
    LocalSearch(4, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)    
    LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
    
    solve(cust_list, route_list, cost_matrix)
       
    prof = calclulateProfitRoute(route_list)
    total_prof = calclulatetotalProfit(prof)
    
   
    f= open("solution.txt","w+")
    print("Total Profit")
    f.write("Total Profit\n")
    print("%d" %total_prof)
    f.write("%d\n" %total_prof)
    for i in range(0,len(route_list)):
        f.write("Route %d\n" %(i+1))
        print("Route %d" %(i+1))
        k=0
        for c in route_list[i].route:
            k=k+1
            if (k==len(route_list[i].route)):
                f.write("%d" %c.id)
            else:
                f.write("%d " %c.id)            
            print("%d" %c.id,end =" ")
        f.write("\n")
        print("")
    

   
   
       


solveProblem()