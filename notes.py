candidates = generatePairs(cust_list)
    servedpairs=[]
    candidates2=[]
    candidates2 = generatePairs(cust_list)
    allservedpairs=[]
    allservedpairs=generateServedPairs(cust_list)
    
    
    for r in route_list:
        servedpairs.append(generateServedPairs(r.route))   

    LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)

    prof = calclulateProfitRoute(route_list)
    total_prof = calclulatetotalProfit(prof)
    print(total_prof)
    for k in route_list:
        print("ROUTE " , k.id ,"LEN: " , len(k.route), "TIME: ", k.time, "CAPACITY: ", k.capacity, "PROFIT: ", prof[k.id])
        

    
    solve(cust_list, route_list, cost_matrix)
    prof = calclulateProfitRoute(route_list)
    total_prof = calclulatetotalProfit(prof)
    print(total_prof)

   
    
    
    LocalSearch(4, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
    
    solve(cust_list, route_list, cost_matrix)
    LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
    solve(cust_list, route_list, cost_matrix)
    #LocalSearch(0, route_list, cost_matrix, candidates,candidates2,servedpairs,cust_list)
    
    
    

   

    prof = calclulateProfitRoute(route_list)
    total_prof = calclulatetotalProfit(prof)
    print(total_prof)
    
    #TwoServedOneUnservedExchange(route_list, cost_matrix, cust_list, servedpairs)


    f= open("sol.txt","w+")
    print("Total Profit")
    f.write("Total Profit\n")
    print("%d" %total_prof)
    f.write("%d\n" %total_prof)
    for i in range(0,len(route_list)):
        f.write("Route %d\n" %(i+1))
        print("Route %d" %(i+1))
        for c in route_list[i].route:            
            f.write("%d " %c.id)
            print("%d" %c.id,end =" ")
        f.write("\n")
        print("")
        
   
    for k in route_list:
        print("ROUTE " , k.id ,"LEN: " , len(k.route), "TIME: ", k.time, "CAPACITY: ", k.capacity, "PROFIT: ", prof[k.id])
    
     