import random
import math

class Node:
    def __init__(self, idd, xx, yy, dem = 0, st = 0, profit = 0):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.isRouted = False
        self.st = st
        self.demand = dem
        self.profit = profit


def load_model(file_name):
    all_nodes = []
    all_lines = list(open(file_name, "r"))

    line_counter = 0
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep='\t')
    vehicles = int(no_spaces[1])

    line_counter += 1
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep='\t')
    capacity = int(no_spaces[1])

    line_counter += 1
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep='\t')
    time_limit = int(no_spaces[1])

    line_counter += 3
    ln = all_lines[line_counter]

    no_spaces = ln.split(sep='\t')
    x = float(no_spaces[1])
    y = float(no_spaces[2])
    depot = Node(0, x, y)
    all_nodes.append(depot)

    line_counter += 2
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep='\t')
    tot_customers = int(no_spaces[1])

    line_counter += 4

    for i in range(tot_customers):
        ln = all_lines[line_counter]
        no_spaces = ln.split(sep='\t')
        idd = int(no_spaces[0])
        x = float(no_spaces[1])
        y = float(no_spaces[2])
        demand = int(no_spaces[3])
        st = int(no_spaces[4])
        profit = int(no_spaces[5])
        customer = Node(idd, x, y, demand, st, profit)
        all_nodes.append(customer)
        line_counter += 1

    return all_nodes, vehicles, capacity, time_limit


def distance(from_node, to_node):
    dx = from_node.x - to_node.x
    dy = from_node.y - to_node.y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist


def calculate_route_details(nodes_sequence):
    rt_profit = 0
    rt_load = 0
    rt_time = 0
    for i in range(len(nodes_sequence) - 1):
        from_node = nodes_sequence[i]
        to_node = nodes_sequence[i+1]
        rt_profit += from_node.profit
        rt_load += from_node.demand
        rt_time += from_node.st
        travel_time = distance(from_node, to_node)
        rt_time += travel_time
    return rt_time, rt_load, rt_profit


def test_solution(file_name, all_nodes, vehicles, capacity, time_limit):
    all_lines = list(open(file_name, "r"))
    line = all_lines[1]
    profit_reported = int(line)
    profit_calculated = 0
    vehs_used = int((len(all_lines) - 2)/2)

    if vehs_used > vehicles:
        print('More than', vehicles, 'used in the solution')
        return

    line_counter = 3
    for i in range(vehs_used):
        ln = all_lines[line_counter]
        ln = ln.replace('\t', ' ')
        ln = ln.replace('\n', ' ')
        no_spaces = ln.split(sep=' ')
        if '' in no_spaces:
            no_spaces.remove('')
        ids = [int(no_spaces[i]) for i in range(len(no_spaces))]
        nodes_sequence = [all_nodes[idd] for idd in ids]
        rt_time, rt_load, rt_profit = calculate_route_details(nodes_sequence)
        if rt_time > time_limit:
            print('Time violation. Route', i, 'total time is', rt_time)
            return
        if rt_load > capacity:
            print('Capacity violation. Route', i, 'total load is', rt_time)
            return
        profit_calculated += rt_profit
        line_counter += 2
    if profit_calculated != profit_reported:
        print('Profit Inconsistency. Profit Reported', profit_reported, '--- Profit Calculated', profit_calculated)
        return
    print('Solution is οκ. Total Profit:', profit_calculated)


all_nodes, vehicles, capacity, time_limit = load_model('Instance.txt')
test_solution('sol_example.txt', all_nodes, vehicles, capacity, time_limit)