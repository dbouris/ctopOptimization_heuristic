import copy

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

class Route:
  def __init__(self, route,capacity,id,time):
    self.route = route
    self.capacity  = capacity
    self.id = id
    self.time = time
    

class OneRouteBi(object):
    def __init__(self):
        self.time = 10*900
        self.customer = None
        self.position = None
        

    def Initialize(self):
        self.time = 10*900
        self.customer = None
        self.position = None


def InitializeOperators(rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()


# store the info for the swap move in the SwapMove object
# keep the target, origin route
# keep the target, origin node to be swapped
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
        

def FindBestSwapMove(sm, route_list, cost_matrix):
    # loop through all routes, as the first route
        for firstRouteIndex in range(0, len(route_list)):
            rt1 = route_list[firstRouteIndex]
            # loop through all routes, as the second route
            for secondRouteIndex in range (firstRouteIndex,len(route_list)):
                #print("CHECKING ROUTE: ", firstRouteIndex, "WITH: ", secondRouteIndex)
                rt2 = route_list[secondRouteIndex]
                # loop through all nodes in the first route, as the first node
                for firstNodeIndex in range (1, len(rt1.route) - 1):
                    startOfSecondNodeIndex = 1
                    # if the first and second route are the same, we can't swap the first node with itself
                    # so start from the second node
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    # loop through all nodes in the second route, as the second node
                    for secondNodeIndex in range (startOfSecondNodeIndex, len(rt2.route) - 1):

                        # get the first node, the previous node and the next node
                        a1 = rt1.route[firstNodeIndex - 1]
                        b1 = rt1.route[firstNodeIndex]
                        c1 = rt1.route[firstNodeIndex + 1]

                        # get the second node, the previous node and the next node
                        a2 = rt2.route[secondNodeIndex - 1]
                        b2 = rt2.route[secondNodeIndex]
                        c2 = rt2.route[secondNodeIndex + 1]

                        # calculate the cost of the move
                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        # if the first and second route are the same
                        if rt1 == rt2:
                            # if the nodes are consecutive
                            if firstNodeIndex == secondNodeIndex - 1:
                                # calculate the cost of the move
                                costRemoved = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][b2.id] + cost_matrix[b2.id][c2.id]
                                costAdded = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][b1.id] + cost_matrix[b1.id][c2.id]
                                moveCost = costAdded - costRemoved


                            else:
                                # calculate the cost of the move, mind that there will be two changes in the route
                                # and thus two removals and two additions
                                costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                                costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                                costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                                costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            
                            # check for time violation
                            if rt1.time + moveCost > 200:
                                continue
                        # if the first and second route are different
                        else:
                            # check if the move is feasible capacity wise for both the routes
                            if rt1.capacity - b1.demand + b2.demand > 150:
                                continue
                            if rt2.capacity - b2.demand + b1.demand > 150:
                                continue
                            # as above, there will be two cost additions and two removals
                            costRemoved1 = cost_matrix[a1.id][b1.id] + cost_matrix[b1.id][c1.id]
                            costAdded1 = cost_matrix[a1.id][b2.id] + cost_matrix[b2.id][c1.id]
                            costRemoved2 = cost_matrix[a2.id][b2.id] + cost_matrix[b2.id][c2.id]
                            costAdded2 = cost_matrix[a2.id][b1.id] + cost_matrix[b1.id][c2.id]
                            # calculate the cost of the move on both the routes
                            costChangeFirstRoute = costAdded1 - costRemoved1  + b2.serv_time - b1.serv_time
                            costChangeSecondRoute = costAdded2 - costRemoved2 + b1.serv_time - b2.serv_time
                            
                            # check for time violation on both  the routes
                            if rt1.time + costChangeFirstRoute > 200:
                                continue
                            if rt2.time + costChangeSecondRoute > 200:
                                continue
                            # calculate the overall cost of the move
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            
                        # if the move is better than the best move so far, store it
                        if moveCost < sm.moveCost:
                            StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)


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

        
        UpdateRouteCostAndLoad(rt1, cost_matrix)
        UpdateRouteCostAndLoad(rt2, cost_matrix)


# function to update the cost and load of a route
def UpdateRouteCostAndLoad(rt, cost_matrix):
    tc = 0
    tl = 0
    # iterate over all the nodes in the route
    for i in range(0, len(rt.route) - 1):
        A = rt.route[i]
        B = rt.route[i+1]
        # add the cost of the link between the two nodes
        tc += cost_matrix[A.id][B.id]
        # if the node is not the depot, add the load of the node
        if i !=0:
            tc += A.serv_time
            tl += A.demand
    # update the cost and load of the route
    rt.capacity = tl
    rt.time = tc

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

# keep the two opt move details in the best move object
def StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
    top.positionOfFirstRoute = rtInd1
    top.positionOfSecondRoute = rtInd2
    top.positionOfFirstNode = nodeInd1
    top.positionOfSecondNode = nodeInd2
    top.moveCost = moveCost

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



# find the best two opt move: break 2 routes and merge them in a different way
# this move is used to untangle the routes
def FindBestTwoOptMove(top, route_list, cost_matrix):
    # loop over all the routes, as the first route
    for rtInd1 in range(0, len(route_list)):
        rt1 = route_list[rtInd1]
        # loop over all the routes, as the second route
        for rtInd2 in range(rtInd1, len(route_list)):
            rt2 = route_list[rtInd2]
            # loop over all the nodes in the first route, as the first breaking point
            for nodeInd1 in range(0, len(rt1.route) - 1):
                start2 = 0
                # if the two routes are the same, start the second breaking point from the next node
                if (rt1 == rt2):
                    start2 = nodeInd1 + 2
                # loop over all the nodes in the second route, as the second breaking point
                for nodeInd2 in range(start2, len(rt2.route) - 1):
                    moveCost = 10 ** 9
                    # get the node ids at the breaking points
                    A = rt1.route[nodeInd1]
                    B = rt1.route[nodeInd1 + 1]
                    K = rt2.route[nodeInd2]
                    L = rt2.route[nodeInd2 + 1]
                    
                    # if the two routes are the same
                    if rt1 == rt2:
                        # if the breaking points are adjacent, skip the move
                        if nodeInd1 == 0 and nodeInd2 == len(rt1.route) - 2:
                            continue
                        # calculate the cost of the move
                        costAdded = cost_matrix[A.id][K.id] + cost_matrix[B.id][L.id]
                        costRemoved = cost_matrix[A.id][B.id] + cost_matrix[K.id][L.id]
                        moveCost = costAdded - costRemoved
                        # check for time violation
                        if rt1.time + moveCost > 200:
                            continue
                    # if the two routes are different
                    else:
                        # if the points to break are the first ones of each route, skip the move
                        if nodeInd1 == 0 and nodeInd2 == 0:
                            continue
                        if nodeInd1 == len(rt1.route) - 2 and  nodeInd2 == len(rt2.route) - 2:
                            continue
                        # check if the capacity constraint is violated for both the routes
                        if CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                            #print("CAPACITY VIOLATION")
                            continue
                        # calculate the cost of the move
                        costAdded = cost_matrix[A.id][L.id] + cost_matrix[B.id][K.id]
                        costRemoved = cost_matrix[A.id][B.id] + cost_matrix[K.id][L.id]
                        moveCost = costAdded - costRemoved
                        
                        # get the segments of each route to break
                        relocatedSegmentOfRt1 = rt1.route[nodeInd1 + 1 :]
                        relocatedSegmentOfRt2 = rt2.route[nodeInd2 + 1 :]
                        # calculate the time of the first segment to relocate for both the routes
                        TimeReloc1 = getTimeInRoute(relocatedSegmentOfRt1, cost_matrix)
                        remaining1 = rt1.time - TimeReloc1

                        TimeReloc2 = getTimeInRoute(relocatedSegmentOfRt2, cost_matrix)
                        remaining2 = rt2.time - TimeReloc2

                        # check if the time constraint is violated for both the routes
                        # importan to add and remove the new links cost
                        if remaining1 + TimeReloc2 - cost_matrix[A.id][B.id] + cost_matrix[A.id][L.id] > 200:
                            continue
                        if remaining2 + TimeReloc1 - cost_matrix[K.id][L.id] +  cost_matrix[B.id][K.id] > 200:
                            continue

                    # if the move is better than the best move so far, store it
                    if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                        StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

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
           
# find the best two pair exchange move    
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


def ApplyOneNodeMove(best : PairInsertionMove,route_list):
    route_list[best.route].route = best.route_list
    route_list[best.route].time = best.route_time
    route_list[best.route].capacity = route_list[best.route].capacity + best.capacity_change
    best.nodetoadd.added = True   
    best.nodetoremove.added = False


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
       
