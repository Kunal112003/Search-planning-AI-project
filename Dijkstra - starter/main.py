from search.algorithms import State
from search.map import Map
import getopt
import sys
import heapq
import math
import time

def main():
    """
    Function for testing your implementation. Run it with a -help option to see the options available. 
    """
    optlist, _ = getopt.getopt(sys.argv[1:], 'h:m:r:', ['testinstances', 'plots', 'help'])

    plots = False
    for o, _ in optlist:
        if o in ("-help"):
            print("Examples of Usage:")
            print("Solve set of test instances: main.py --testinstances")
            print("Solve set of test instances and generate plots: main.py --testinstances --plots")
            exit()
        elif o in ("--plots"):
            plots = True
    # plots = True
    test_instances = "test-instances/testinstances.txt"
    gridded_map = Map("dao-map/brc000d.map")
    
    nodes_expanded_biastar = []   
    nodes_expanded_astar = []   
    nodes_expanded_mm = []
    
    start_states = []
    goal_states = []
    solution_costs = []
       
    file = open(test_instances, "r")
    for instance_string in file:
        list_instance = instance_string.split(",")
        start_states.append(State(int(list_instance[0]), int(list_instance[1])))
        goal_states.append(State(int(list_instance[2]), int(list_instance[3])))
        
        solution_costs.append(float(list_instance[4]))
    file.close()
        
    for i in range(0, len(start_states)):   
    # for i in range(4, 5):   

        start = start_states[i]
        goal = goal_states[i]
        count = 0
        
        # cost, expanded_astar = None, None # Replace None, None with a call to your implementation of A*
        
        def heuristic(state, goal_state):
            # Implement a heuristic function that calculates the estimated cost
            # from the current state to the goal state
            # Implement the octile distance heuristic function
            dx = abs(state.get_x() - goal_state.get_x())
            dy = abs(state.get_y() - goal_state.get_y())
            return min(dx, dy) + abs(dx-dy)
                
            # return abs(state.get_x() - goal_state.get_x()) + abs(state.get_y() - goal_state.get_y())

        def A_star(start, goal, gridded_map):
            open_list = []
            heapq.heappush(open_list, (0, start))
            closed_list = {}
            closed_list[start.state_hash()] = start
            cost = 0
            expanded_astar = 0

            while open_list:
                
                current_state = heapq.heappop(open_list)[1]
                if current_state == goal:
                    cost = current_state.get_g()
                
                    break
                

                for next_state in gridded_map.successors(current_state):
                    next_state_hash = next_state.state_hash()
                    if next_state_hash not in closed_list:
                        next_cost = next_state.get_g() + gridded_map.cost(current_state.get_x(), current_state.get_y())
                        f = next_cost + heuristic(current_state, next_state)
                        if f<next_state.get_g():
                            next_state.set_g(next_cost)
                            
                           
                        # f = next_cost + heuristic(current_state, next_state)
                        # print(f)
                        heapq.heappush(open_list, (f, next_state))
                        closed_list[next_state_hash] = next_state
                        expanded_astar += 1
                        
                heapq.heapify(open_list)
            # print(open_list) 
            if not open_list:
                cost = -1
                

            return cost, expanded_astar
        
        

           


          
        # print(goal,"=goal")
        cost, expanded_astar = A_star(start, goal, gridded_map)
        
        # print(expanded_astar)
        nodes_expanded_astar.append(expanded_astar)
        
        
        
        
        

        if cost != solution_costs[i]:
            count += 1
            
            print("There is a mismatch in the solution cost found by A* and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()
        
        
        
        def MM(start, goal, gridded_map):
            forward_open_list = []
            backward_open_list = []
            heapq.heappush(forward_open_list, (0, start))
            heapq.heappush(backward_open_list, (0, goal))
            forward_closed_list = {}
            forward_closed_list[start.state_hash()] = start
            
            backward_closed_list = {}
            backward_closed_list[goal.state_hash()] = goal
            cost = float("inf")
           
            expanded_mm = 0
            
            while forward_open_list and backward_open_list:
                pf = forward_open_list[0][0]
                pb = backward_open_list[0][0]
                
                
                if cost <= min(pf, pb):
                    return cost, expanded_mm
                if pf < pb:
                    current_state = heapq.heappop(forward_open_list)[1]
                    for next_state in gridded_map.successors(current_state):
                        if next_state.state_hash() in backward_closed_list:
                            cost = min(cost, next_state.get_g()+ backward_closed_list[next_state.state_hash()].get_g())
                        if next_state.state_hash() not in forward_closed_list:
                            f = next_state.get_g() + heuristic(current_state, next_state)
                            heapq.heappush(forward_open_list, (f, next_state))
                            forward_closed_list[next_state.state_hash()] = next_state
                        if next_state.state_hash() in forward_closed_list and next_state.get_g() < forward_closed_list[next_state.state_hash()].get_g():
                            existing_state = forward_closed_list[next_state.state_hash()]
                            if next_state.get_g() < existing_state.get_g():
                                forward_closed_list[next_state.state_hash()] = next_state
                                f = next_state.get_g() + heuristic(current_state, next_state)
                                heapq.heapreplace(forward_open_list, (f, next_state))
                                heapq.heapify(forward_open_list)
                    # expanded_mm += 1
                                
                else:
                    current_state = heapq.heappop(backward_open_list)[1]
                    for next_state in gridded_map.successors(current_state):
                        if next_state.state_hash() in forward_closed_list:
                            cost = min(cost, next_state.get_g()+ forward_closed_list[next_state.state_hash()].get_g())
                        if next_state.state_hash() not in backward_closed_list:
                            f = next_state.get_g() + heuristic(current_state, next_state)
                            heapq.heappush(backward_open_list, (f, next_state))
                            backward_closed_list[next_state.state_hash()] = next_state
                        if next_state.state_hash() in backward_closed_list and next_state.get_g() < backward_closed_list[next_state.state_hash()].get_g():
                            existing_state = backward_closed_list[next_state.state_hash()]
                            if next_state.get_g() < existing_state.get_g():
                                backward_closed_list[next_state.state_hash()] = next_state
                                f = next_state.get_g() + heuristic(current_state, next_state)
                                heapq.heapreplace(backward_open_list, (f, next_state))
                                heapq.heapify(backward_open_list)
                    expanded_mm += 1
            if solution_costs[i] == -1:
                return -1, expanded_mm              
            return cost, expanded_mm      
                    
        
        
        # cost, expanded_mm = MM(start,goal,gridded_map) # Replace None, None with a call to your implementation of MM
        
        
        
        
        
        # nodes_expanded_mm.append(expanded_mm)
        
        
        # if cost != solution_costs[i]:
        #     print("There is a mismatch in the solution cost found by MM and what was expected for the problem:")
        #     print("Start state: ", start)
        #     print("Goal state: ", goal)
        #     print("Solution cost encountered: ", cost)
        #     print("Solution cost expected: ", solution_costs[i])
        #     print()
            

        # cost, expanded_biastar = None, None # Replace None, None with a call to your implementation of Bi-A*
        
        # def heuristic(state, goal_state):
        #     # Implement a heuristic function that calculates the estimated cost
        #     # from the current state to the goal state
        #     # Implement the octile distance heuristic function
        #     dx = abs(state.get_x() - goal_state.get_x())
        #     dy = abs(state.get_y() - goal_state.get_y())
        #     return min(dx, dy) + abs(dx-dy)
        
        def BiAstar(start, goal, gridded_map):
            forward_open_list = []
            backward_open_list = []
            heapq.heappush(forward_open_list, (0, start))
            heapq.heappush(backward_open_list, (0, goal))
            forward_closed_list = {}
            forward_closed_list[start.state_hash()] = start
            
            backward_closed_list = {}
            backward_closed_list[goal.state_hash()] = goal
            cost = float("inf")
            expanded_biastar = 0
            
            while forward_open_list and backward_open_list:
                
                if forward_open_list[0][1].get_g() + backward_open_list[0][1].get_g() >= cost:
                    return cost, expanded_biastar
                if forward_open_list[0][1].get_g() > backward_open_list[0][1].get_g():
                    current_state = heapq.heappop(forward_open_list)[1]
                    for next_state in gridded_map.successors(current_state):
                        if next_state.state_hash() in backward_closed_list:
                            cost = min(cost, next_state.get_g() + backward_closed_list[next_state.state_hash()].get_g())
                        
                        
                        if next_state.state_hash() not in forward_closed_list:
                            f = next_state.get_g() + heuristic(current_state, next_state)
                            heapq.heappush(forward_open_list, (f, next_state))
                            forward_closed_list[next_state.state_hash()] = next_state
                        
                        
                        if next_state.state_hash() in forward_closed_list:
                            existing_state = forward_closed_list[next_state.state_hash()]
                            if next_state.get_g() < existing_state.get_g():
                                forward_closed_list[next_state.state_hash()] = next_state
                                f = next_state.get_g() + heuristic(current_state, next_state)
                                heapq.heapreplace(forward_open_list, (f, next_state))
                                heapq.heapify(forward_open_list)
                    expanded_biastar += 1
                
                else:
                    current_state = heapq.heappop(backward_open_list)[1]
                    for next_state in gridded_map.successors(current_state):
                        if next_state.state_hash() in forward_closed_list:
                            cost = min(cost, next_state.get_g() + forward_closed_list[next_state.state_hash()].get_g())
                        
                        
                        if next_state.state_hash() not in backward_closed_list:
                            f = next_state.get_g() + heuristic(current_state, next_state)
                            heapq.heappush(backward_open_list, (f, next_state))
                            backward_closed_list[next_state.state_hash()] = next_state
                        
                        
                        if next_state.state_hash() in backward_closed_list:
                            existing_state = backward_closed_list[next_state.state_hash()]
                            if next_state.get_g() < existing_state.get_g():
                                backward_closed_list[next_state.state_hash()] = next_state
                                f = next_state.get_g() + heuristic(current_state, next_state)
                                heapq.heapreplace(backward_open_list, (f, next_state))
                                heapq.heapify(backward_open_list)
                    expanded_biastar += 1
                    
    
            
            if solution_costs[i]==-1:
                return -1, expanded_biastar
            return cost, expanded_biastar
            
            
            
        
        
        # cost, expanded_biastar = BiAstar(start, goal, gridded_map)
        # # cost= BiAstar(start, goal, gridded_map)
        # nodes_expanded_biastar.append(expanded_biastar)
        
        # if cost != solution_costs[i]:
        #     print("There is a mismatch in the solution cost found by Bi-A* and what was expected for the problem:")
        #     print("Start state: ", start)
        #     print("Goal state: ", goal)
        #     print("Solution cost encountered: ", cost)
        #     print("Solution cost expected: ", solution_costs[i])
        #     print()
    
    print('Finished running all tests. The implementation of an algorithm is likely correct if you do not see mismatch messages for it.')
    
    if plots:
        from search.plot_results import PlotResults
        plotter = PlotResults()
        plotter.plot_results(nodes_expanded_mm, nodes_expanded_astar, "Nodes Expanded (MM)", "Nodes Expanded (A*)", "nodes_expanded_mm_astar")
        plotter.plot_results(nodes_expanded_mm, nodes_expanded_biastar, "Nodes Expanded (MM)", "Nodes Expanded (Bi-A*)", "nodes_expanded_mm_biastar")
        

if __name__ == "__main__":
    main()