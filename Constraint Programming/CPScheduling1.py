from ortools.sat.python import cp_model
import time
# Read input
classes = {}
rooms = {}
teachers = []
inputFile = 'data.txt'
with open(inputFile, "r") as f:
    lines = f.readlines()
    N, M = [int(x) for x in lines[0].split()]
    for i in range(1, N + 1):
        t, g, s = lines[i].split()
        classes[i] = (int(t), g, int(s))
        if g not in teachers: teachers.append(g)
    for j in range(len(lines[N+1].split())):
        rooms[j+1] = int(lines[N+1].split()[j])

# Modelling
model = cp_model.CpModel()

DecisionVar = {}
session = 10
period = 6

for i in classes:
    t, g, s = classes[i]
    for m in rooms:
        for k in range(1, session + 1):
            for b in range(1, period + 1):
                DecisionVar[(i, m, k, b)] = model.NewBoolVar(
                    f"Assign class {i} in room {m} at slot {b} of session {k}")

# Constraint: If a class studies in 1 room, number of students less or equal to the  room capacity
for k in range(1, session + 1):
    for b in range(1, period + 1):
        for i in classes:
            t, g, s = classes[i]
            for m in rooms:
                model.Add(s <= rooms[m]).OnlyEnforceIf(DecisionVar[(i, m, k, b)])

# Constraint: Sum of periods by teacher of each block <= max period
for teacher in teachers:
    for k in range(1, session + 1):
        TeachPeriod = 0
        for m in rooms:
            for i in classes:
                t, g, s = classes[i]
                if g == teacher:
                    for b in range(1, period + 1):
                        TeachPeriod += DecisionVar[(i, m, k, b)]
        model.Add(TeachPeriod <= period)

# Constraint: Each teacher at each period teaches one class only
for teacher in teachers:
    for k in range(1, session + 1):
        for b in range(1, period + 1):
            teacher_variables = [DecisionVar[(i, m, k, b)] for i in classes for m in rooms if classes[i][1] == teacher]
            model.Add(sum(teacher_variables) <= 1)

# Constraint: One room contains one class at each session
for k in range(1, session + 1):
    for b in range(1, period + 1):
        for m in rooms:
            model.Add(sum(DecisionVar[(i, m, k, b)] for i in classes) <= 1)

# Constraint: One class assigned once a week and has to be assigned
for i in classes:
    PeriodInWeek = 0
    t, g, s = classes[i]
    for k in range(1, session + 1):
        for b in range(1, period + 1):
            for m in rooms:
                PeriodInWeek += DecisionVar[(i, m, k, b)]

    model.Add(PeriodInWeek == t)

# Constraint: Class can not be assigned in 2 separated sessions
for i in classes:
    t, g, s = classes[i]
    for k in range(1, session + 1):
        x = model.NewBoolVar("")
        class_period_block = 0
        for m in rooms:
            for b in range(1, period + 1):
                class_period_block += DecisionVar[(i, m, k, b)]

        model.Add(class_period_block == t).OnlyEnforceIf(x)
        model.Add(class_period_block == 0).OnlyEnforceIf(x.Not())


# Constraint: When assign class to a start period, t next periods of that room are blocked
for k in range(1, session + 1):
    for m in rooms:
        for i in classes:
            t, g, s = classes[i]
            for b in range(1, period + 1 - t):
                model.Add(sum(DecisionVar[(i, m, k, b_)] for b_ in range(b, b + t)) == DecisionVar[
                    (i, m, k, b)] * t).OnlyEnforceIf(DecisionVar[(i, m, k, b)])
start =time.time()
#Create solver
solver = cp_model.CpSolver()

# Solve the model
status = solver.Solve(model)
end= time.time()
# Check if the solver successfully found a solution
if status == cp_model.OPTIMAL:
    print("Solution:")

    assignments = []

    for k in range(1, session + 1):
        for b in range(1, period + 1):
            for m in rooms:
                for i in classes:
                    if solver.BooleanValue(DecisionVar[(i, m, k, b)]):
                        assignments.append((i, m, b, k))

    assignments.sort()

    for assignment in assignments:
        i, m, b, k = assignment
        print(f'Class {i} is assigned to room {m} at period {b} of session {k}')

else:
    print("No feasible solution.")
print(f'Runtime: {end-start}')