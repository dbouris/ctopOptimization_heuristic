import csv
import math
from SolutionDrawer import *
import copy
from itertools import combinations
import pprint



# Creation of classes


class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None
        self.moveCost = 10 ** 9


class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.timeChangeFirstRt = None
        self.timeChangeSecondRt = None
        self.moveCost = None
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
        self.moveCost = None
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
    



def identifyMinimumCostInsertion(rt_list,cust_list, cost_matrix):
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
                                best_insertion.time = trialCost 
                                best_insertion.cl = criterion
                            
                else:
                    continue
    return best_insertion


def getEmptyRoutes(trucks):
    apothiki = Customer(0,23.142,11.736,0,0,0,False)
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
    route_list[best_fit.route].time +=  best_fit.time
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

def getTransferCost(route_list, cost_matrix):
    transfer = []
    for i in route_list:
        transfer_cost = 0
        for j in range(0, len(i.route) - 1):
            A = i.route[j].id
            B = i.route[j + 1].id
            transfer_cost = transfer_cost + cost_matrix[A][B]
        transfer.append(transfer_cost)
    return transfer

def getServCost(route_list):
    serv_cost = []
    for i in route_list:
        cost = 0
        for k in i.route:
            cost = cost + k.serv_time
        serv_cost.append(cost)
    return serv_cost

def getTotalServCost(route_list, cost_matrix):
        c = 0
        for route in route_list:
            for j in range (0, len(route.route) - 1):
                a = route.route[j]
                b = route.route[j + 1]
                c += cost_matrix[a.id][b.id]
        return c



def DrawSolution(route_list, cust_list):
    SolDrawer.drawRoutes(route_list)
    SolDrawer.drawPointsUsed(cust_list)

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

def ApplyRelocationMove(rm, route_list):


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

        

def StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
    sm.positionOfFirstRoute = firstRouteIndex
    sm.positionOfSecondRoute = secondRouteIndex
    sm.positionOfFirstNode = firstNodeIndex
    sm.positionOfSecondNode = secondNodeIndex
    sm.timeChangeFirstRt = costChangeFirstRoute
    sm.timeChangeSecondRt = costChangeSecondRoute
    sm.moveCost = moveCost

def StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.timeChangeOriginRt = originRtCostChange
        rm.timeChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

def FindBestRelocationMove(rm, route_list, cost_matrix):
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
                        targetRtCostChange = cost_matrix[F.id][B.id] + cost_matrix[B.id][G.id] - cost_matrix[F.id][G.id]

                        if rt2.time + targetRtCostChange > 200:
                            continue 
                        
                       

                        moveCost = costAdded - costRemoved
                        #print(moveCost)

                        if (moveCost < rm.moveCost):
                            StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)
        


def FindBestSwapMove(sm, route_list, cost_matrix):
        for firstRouteIndex in range(0, len(route_list)):
            rt1 = route_list[firstRouteIndex]
            for secondRouteIndex in range (3,4):
                print("CHECKING ROUTE: ", firstRouteIndex, "WITH: ", secondRouteIndex)
                rt2 = route_list[secondRouteIndex]
                for firstNodeIndex in range (1, len(rt1.route) - 1):
                    startOfSecondNodeIndex = 1
                    if firstRouteIndex == secondRouteIndex:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range (startOfSecondNodeIndex, len(rt2.route) - 1):

                        
                        a1 = rt1.route[firstNodeIndex - 1]
                        b1 = rt1.route[firstNodeIndex]
                        c1 = rt1.route[firstNodeIndex + 1]

                        a2 = rt2.route[secondNodeIndex - 1]
                        b2 = rt2.route[secondNodeIndex]
                        c2 = rt2.route[secondNodeIndex + 1]

                        print("CHECKING:", b1.id , "WITH: ", b2.id)
                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if firstRouteIndex == secondRouteIndex:
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
                        else:
                            if rt1.capacity - b1.demand + b2.demand > 150:
                                print("DOES NOT FIT IN R1")
                                continue
                            if rt2.capacity - b2.demand + b1.demand > 150:
                                print("DOES NOT FIT IN R2")
                                continue

                            costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                            costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                            costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                            costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]

                            costChangeFirstRoute = costAdded1 - costRemoved1  + b2.serv_time - b1.serv_time
                            costChangeSecondRoute = costAdded2 - costRemoved2 + b1.serv_time - b2.serv_time
                            
                            if rt1.time + costChangeFirstRoute > 200:
                                print("TIME 1: ", rt1.time + costChangeFirstRoute)
                                print("TIME VIOLATION IN ROUTE 1")
                                continue

                            if rt2.time + costChangeSecondRoute > 200:
                                print("TIME 1: ", rt2.time + costChangeSecondRoute)
                                print("TIME VIOLATION IN ROUTE 2")
                                continue

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            print(moveCost)
                            
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
        print("ROUTE 1 NEW CAPACITY: ", rt1FirstSegmentLoad + rt2SecondSegmentLoad)
        print("ROUTE 2 NEW CAPACITY: ", rt2FirstSegmentLoad + rt1SecondSegmentLoad)
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
                        #print(moveCost)    
                        if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                            StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

def ApplyTwoOptMove(top, route_list):
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

        UpdateRouteCostAndLoad(rt1)
        UpdateRouteCostAndLoad(rt2)


def UpdateRouteCostAndLoad(rt, cost_matrix):
    tc = 0
    tl = 0
    for i in range(0, len(rt.route) - 1):
        A = rt.route[i]
        B = rt.route[i+1]
        tc += cost_matrix[A.id][B.id]
        tl += A.demand
    rt.capacity = tl
    rt.time = tc


def LocalSearch(operator, route_list, cost_matrix):
        bestSolution = copy.deepcopy(route_list)
        terminationCondition = False
        localSearchIterator = 0
        reloc = 0
        swaps = 0
        opt = 0 

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
       
        while terminationCondition is False:

            InitializeOperators(rm, sm, top)
            

            if operator == 0:
                FindBestRelocationMove(rm, route_list, cost_matrix)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        ApplyRelocationMove(rm, route_list)
                        print("                                                             MADE A RELOCATION")
                        reloc = reloc + 1
                    else:
                        terminationCondition = True
                        print(rm.moveCost)
                        print("FAILED")
            elif operator == 1:
                FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        ApplySwapMove(sm)
                        print("                                                             MADE A SWAP")
                        swaps = swaps +1
                    else:
                        terminationCondition = True
                        print("FAILED")
                        print(sm.moveCost)
            elif operator == 2:
                FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        ApplyTwoOptMove(top)
                        print("                                                             MADE A TWO OPT")
                        opt = opt + 1
                    else:
                        terminationCondition = True
                        print("FAILED")
                        print(top.moveCost)
            


            if (getTotalServCost(route_list,cost_matrix) < getTotalServCost(bestSolution, cost_matrix)):
                bestSolution = copy.deepcopy(route_list)

            localSearchIterator = localSearchIterator + 1
        print("RELOCATIONS: ", reloc)
        print("SWAPS: ", swaps)
        print("TWO OPT: ", opt)



def solve(cust_list, route_list, cost_matrix):
    keep_going = True
    while not_all_added(cust_list) and keep_going:
        best = identifyMinimumCostInsertion(route_list,cust_list , cost_matrix)
        if best.customer != None:
            InsertBestFit(best,route_list)
        else:
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




def solveProblem():
    route_list = getEmptyRoutes(6)
    cust_list = getCustomers("instance.csv")

    cost_matrix = getCost_Matrix(cust_list)

    solve(cust_list, route_list, cost_matrix)
    DrawSolution(route_list, cust_list)
    LocalSearch(0, route_list, cost_matrix)

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

    solve(cust_list, route_list, cost_matrix)
    prof = calclulateProfitRoute(route_list)
    total_prof = calclulateTotalProfit(prof)
    print(total_prof)

    for i in route_list:
        print("ROUTE ", i.id)
        for k in i.route:
            print(k.id, end = " ")
        print() 

    candidates = generatePairs(cust_list)
    for x in candidates:
        cust = x.customers
        print(cust[0].id, cust[1].id)
        print()
    print(len(candidates))
            


solveProblem()



def PairInsertion(pairlist, route_list):
    for pair in pairlist:
        for route in route_list:
            for nodetoremove in route.route:
                #check if the profit of the pair is better
                if pair.TotalProfit >  nodetoremove.profit:
                    #check if the pair can fit in the route demand wise
                    if pair.TotalDemand - nodetoremove.demand + route.capacity > 150:
                        continue
                    candidateroute = route.route
                    candidateroute.remove(nodetoremove)
                    for k in pair.Customers:
                        candidateroute.append(k)
                    
                    newrt = getEmptyRoutes(1)[0]
                    for i in range(0,len(candidateroute)):
                        IdentifyMinimumCostInsertionInRoute(newrt,candidateroute)
                        InsertBestFit(newrt)
                    






