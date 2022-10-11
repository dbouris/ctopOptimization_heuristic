# CTOP
## Constraints Team Orienteering Problem
<img src="Solution_1091.png" width="200" height="160" />
Given a central depot, a set of customers with different demands, serving time and profits and a fleet of vehicles with capacity and duration limitations we created an algorithm
that finds the most profitable customers and creates routes while satisfying the customers and vehicles constraints. All customers are represented as 
nodes in a Cartesian coordinate system. The [instance.csv](https://github.com/dbouris/optimization_methods_competition/blob/main/paradoteo/instance.csv) file 
contains each customer 𝑖 that has a product demand 𝑑, a required service time 𝑠𝑡 and a profit 𝑝. A fleet of 𝑘 car trucks is located in the central depot. 
Each of the vehicles has a product capacity equal to 𝑄. Vehicles start from the depot, serve customers and then return back to the central depot. Each 
vehicle performs one route. Each customer can be covered (it is not necessary how it will be covered) by one visit of a single vehicle. In this case, 
the customer returns his profit. The total time of a route (transition time and customer service time) cannot exceed a time limit 𝑇. At the end we will 
create 𝑘 routes that will maximize the total profit.

## Methodology

