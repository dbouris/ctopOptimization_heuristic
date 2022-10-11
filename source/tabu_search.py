
import math
from shutil import move
from typing import NewType
#from SolutionDrawer import *
import copy
from itertools import combinations
import pprint
import random
import timeit


def SetTabuIterator(n, iterator):
    # n.isTabuTillIterator = iterator + self.tabuTenure
    n.isTabuTillIterator = iterator + random.randint(50, 60)


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


def StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.timeChangeOriginRt = originRtCostChange
        rm.timeChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost



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

def StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
    sm.positionOfFirstRoute = firstRouteIndex
    sm.positionOfSecondRoute = secondRouteIndex
    sm.positionOfFirstNode = firstNodeIndex
    sm.positionOfSecondNode = secondNodeIndex
    sm.timeChangeFirstRt = costChangeFirstRoute
    sm.timeChangeSecondRt = costChangeSecondRoute
    sm.moveCost = moveCost


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



def StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
    top.positionOfFirstRoute = rtInd1
    top.positionOfSecondRoute = rtInd2
    top.positionOfFirstNode = nodeInd1
    top.positionOfSecondNode = nodeInd2
    top.moveCost = moveCost

def getTimeInRoute(route, cost_matrix):
    c = 0
    for j in range (0, len(route) - 1):
        a = route[j]
        b = route[j + 1]
        c += cost_matrix[a.id][b.id]
        c += a.serv_time
    return c

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


def MoveIsTabu(n, iterator, moveCost, route_list, cost_matrix, bestSolution):
        if moveCost + getTransferCost(route_list, cost_matrix) < getTransferCost(bestSolution, cost_matrix) - 0.001:
            return False
        if iterator < n.isTabuTillIterator:
            return True
        return False

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