import pyomo.environ as pyo

# Create a model
model = pyo.ConcreteModel(name="Designer_Allocation")

model.I = pyo.Set(initialize=['Designer1', 'Designer2', 'Designer3'])
model.J = pyo.Set(initialize=['ProjectA', 'ProjectB', 'ProjectC', 'ProjectD'])

# Parameters
scores = {
    ('Designer1', 'ProjectA'): 90,
    ('Designer1', 'ProjectB'): 80,
    ('Designer1', 'ProjectC'): 10,
    ('Designer1', 'ProjectD'): 50,
    ('Designer2', 'ProjectA'): 60,
    ('Designer2', 'ProjectB'): 70,
    ('Designer2', 'ProjectC'): 50,
    ('Designer2', 'ProjectD'): 65,
    ('Designer3', 'ProjectA'): 70,
    ('Designer3', 'ProjectB'): 40,
    ('Designer3', 'ProjectC'): 80,
    ('Designer3', 'ProjectD'): 85,}

requirements = {
    'ProjectA': 70,
    'ProjectB': 50,
    'ProjectC': 85,
    'ProjectD': 35,}

availability = 80

model.x = pyo.Var(model.I, model.J, domain=pyo.NonNegativeReals)

# Objective: Maximize total score
def objective_rule(model):
    return sum(scores[i, j] * model.x[i, j] for i in model.I for j in model.J)
model.objective = pyo.Objective(rule=objective_rule, sense=pyo.maximize)

def supply_rule(model, i):
    return sum(model.x[i, j] for j in model.J) <= availability
model.supply_con = pyo.Constraint(model.I, rule=supply_rule)

def demand_rule(model, j):
    return sum(model.x[i, j] for i in model.I) >= requirements[j]
model.demand_con = pyo.Constraint(model.J, rule=demand_rule)

solver = pyo.SolverFactory('glpk')
results = solver.solve(model)

# Display results
print("Optimization Status:", results.solver.status)
print(f"Maximum Total Score: {pyo.value(model.objective)}")
print("\nAllocation (Hours):")
for i in model.I:
    for j in model.J:
        val = pyo.value(model.x[i, j])
        if val > 0:
            print(f"Designer {i} to Project {j}: {val} hours")