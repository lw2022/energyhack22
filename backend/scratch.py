

# # agents = []
# # for i in range(2):
# #     agents.append(Agent(Hex(0, 0, 0), Hex(0, -1, 1), 1, 0))
# # grid, agents, schedule = create_custom(agents, radius = 2)

# for i, ag in enumerate(agents):
#     ag._id = i

def optimal_solver(grid, agents, schedule, Tf = 20, weights=False):
    Tf = Tf

    # Create variables w for all flights, times, sectors 
    # variables have Agent, Sector (only on path), Time (only after takeoff), Layer (0, 1, 2)
    # for each flight iterate
    vars = []
    departures = {}     # hex : id  where hex is the takeoff and id is agent
    travel = {}         # hex: [(id, next, time, layer)] where next is next hex and time is the first time it's active and layer is the next step layer we care about

    # Variable definition
    # define only for sectors agent will travel in, including start and end
    # define for all times after agent departure
    for ag in agents:
        indices = []

        for i, h in enumerate(ag.steps):

            # create entries in travel
            if h not in travel:
                travel[h] = []
            if i + 1 >= len(ag.steps):
                travel[h].append((ag.id, ag.steps[-1], ag.depart, 2))     ## CHANGE ag.depart to have logic when # var defs are shrunk
            else:
                travel[h].append((ag.id, ag.steps[i+1], ag.depart, 1))


            # create the variables  
            # ## NOTE when # var defs shrunk, must define variable one time-step before it actually can be filled, so that capacity constraints make sense
            for t in range(ag.depart, Tf+1):
                indices.append((ag.id, h, t, 1))

        for t in range(ag.depart, Tf+1): 
            # start and end layers
            indices.append((ag.id, ag.steps[0], t, 0))
            indices.append((ag.id, ag.steps[-1], t, 2))

        vars += indices   

    ### Create model
    m = ConcreteModel()
    m.vars = Set(initialize = vars)
    m.w = Var(m.vars, domain=Binary)    # indexing is (id, q, r, s, time, layer)


    ## set boundary conditions - initialization, ending, and everything layer 1 and 2 at time 0 is 0
    m.boundary = ConstraintList()
    for ag in agents:
        # initialization - enters layer 0
        m.boundary.add(m.w[ag.id, ag.steps[0], ag.depart, 0] == 1)

        # ending - has to be in layer 2 by the end
        m.boundary.add(m.w[ag.id, ag.steps[-1], Tf, 2] == 1)

        # initial empty - all the 1's are not filled when the agent departs
        # the first 1 that exist basically
        for s in ag.steps:
            m.boundary.add(m.w[ag.id, s, ag.depart, 1] == 0)
        
        # initial empty - 2's are not filled when the agent departs
        m.boundary.add(m.w[ag.id, ag.steps[-1], ag.depart, 2] == 0)
        


    # capacity (4)  ## SKIPPING FOR ONE AGENT 
    m.capacity = ConstraintList()
    # movement constraints - for a hex, go through all times - at each time go through all agents, figure out who maters, and put them into constraint
    for cur, data in travel.items():
        for t in range(Tf+1):
            sum = None
            for agid, next, time, layer in data:
                if t < time: continue       # the variable doesn't exist yet and isn't defined for current t

                sum += m.w[agid, cur, t, 1] - m.w[agid, next, t, layer]

            if sum is not None:     # if something has been added to the sum
                m.capacity.add(sum <= 1)

    # takeoff constraints - a form of capacity essentially

    # continuity (5) - for every step in agent, step after must be taken after step is taken and time has passed
    m.cont = ConstraintList()
    for ag in agents:
        for i in range(len(ag.steps) - 1):
            cur_step = ag.steps[i]
            next_step = ag.steps[i+1]

            # iterate through all times except time 0 - set time 0 to == 0 b/c physically impossible but can't tie to a previous step
            for t in range(ag.depart, Tf):     # not Tf+1 b/c of t+1 below
                m.cont.add(m.w[ag.id, next_step, t+1, 1] - m.w[ag.id, cur_step, t, 1] <= 0)

        # do the 0 and 2 layers, for all times
        for t in range(ag.depart, Tf):
            # can't be in 1 until you're in origin 0
            m.cont.add(m.w[ag.id, ag.steps[0], t+1, 1] - m.w[ag.id, ag.steps[0], t, 0] <= 0)

            # can't be in 2 until you're in destination 1
            m.cont.add(m.w[ag.id, ag.steps[-1], t+1, 2] - m.w[ag.id, ag.steps[-1], t, 1] <= 0)


    # time constraints (7) - for every time of every sector of every flight
    # if t is 1, then t' >= t must be 1
    m.time = ConstraintList()
    for ag in agents:
        for s in ag.steps:
            for t in range(ag.depart, Tf):  # not Tf+1 b/c of t+1 below
                    m.time.add(m.w[ag.id, s, t+1, 1] - m.w[ag.id, s, t, 1] >= 0)

        # handle 0 and 2 layer
        for t in range(ag.depart, Tf):
            m.time.add(m.w[ag.id, ag.steps[0], t+1, 0] - m.w[ag.id, ag.steps[0], t, 0] >= 0)
            m.time.add(m.w[ag.id, ag.steps[-1], t+1, 2] - m.w[ag.id, ag.steps[-1], t, 2] >= 0)

    # objective
    def objective(m):
        sum = 0
        for ag in agents:
            end = ag._steps[-1]

            for t in range(ag.depart, Tf):
                if weights:
                    sum += t * ag.cost * (m.w[ag.id, end, t+1, 2] - m.w[ag.id,end, t, 2])
                else:
                    sum += t * (m.w[ag.id, end, t+1, 2] - m.w[ag.id,end, t, 2])
            
            if weights:
                sum -= ag.scheduled * ag.cost
            else:
                sum -= ag.scheduled
        
        return sum

    m.obj = Objective(rule=objective, sense=minimize)

    #solve
    SolverFactory('gurobi').solve(m)
    # m.w.pprint()


    return value(m.obj), m.w


