from ortools.sat.python import cp_model
import time

#Read input
classes = {}
rooms = {}
teachers = []
inputFile = 'data.txt'
with open(inputFile, "r") as f:
    lines = f.readlines()
    N, M = [int(x) for x in lines[0].split()]
    for i in range(N):
        t, g, s = lines[i+1].split()
        classes[i] = (int(t), g, int(s))
        if g not in teachers: teachers.append(g)
    for j in range(len(lines[N+1].split())):
        rooms[j+1] = int(lines[N+1].split()[j])


g={}
for i in teachers:
  g[int(i)]=[j for j in classes if classes[j][1]== i]

#Modelling
model= cp_model.CpModel()
session = 10
period = 6

x = {}
for i in classes:
        for m in rooms:
            for k in range(1, session+1):
                for b in range(1, period+1):
                    x[i, m, k, b] = model.NewIntVar(0, 1, f'x[{i},{m},{k},{b}]')
y = [model.NewIntVar(0, 1, f'y[{i}]') for i in range(N)]

#Constraint: If a class studies in 1 room, number of students less or equal to the  room capacity
for k in range(1, session + 1):
    for b in range(1, period + 1):
        for i in classes:
            t, g, s = classes[i]
            for m in rooms:
                model.Add(s <= rooms[m]).OnlyEnforceIf(x[(i, m, k, b)])


# Constraint: Two classes have the same teacher need to schedule seperately
for teacher in teachers:
    for k in range(1, session + 1):
        for b in range(1, period + 1):
            teacher_variables = [x[(i, m, k, b)] for i in classes for m in rooms if classes[i][1] == teacher]
            model.Add(sum(teacher_variables) <= 1)

#Constraint: One room contains one class at each session
for k in range(1, session + 1):
    for b in range(1, period + 1):
        for m in rooms:
            model.Add(sum(x[(i, m, k, b)] for i in classes) <= 1)

# Constraint: When assign class to a start period, t next periods of that room are blocked
for k in range(1, session + 1):
    for m in rooms:
        for i in classes:
            t, g, s = classes[i]
            for b in range(1, period + 1 - t):
                model.Add(sum(x[(i, m, k, b_)] for b_ in range(b, b + t)) == x[
                    (i, m, k, b)] * t).OnlyEnforceIf(x[(i, m, k, b)])

# Constraint: One class assigned once a week and has to be assigned
for i in classes:
    PeriodInWeek = 0
    t, g, s = classes[i]
    for k in range(1, session + 1):
        for b in range(1, period + 1):
            for m in rooms:
                PeriodInWeek += x[(i, m, k, b)]

    model.Add(PeriodInWeek == t)

# Constraint: Class can not be assigned in 2 separated sessions
for i in classes:
    t, g, s = classes[i]
    for k in range(1, session + 1):
        z = model.NewBoolVar("")
        class_period_block = 0
        for m in rooms:
            for b in range(1, period + 1):
                class_period_block += x[(i, m, k, b)]

        model.Add(class_period_block == t).OnlyEnforceIf(z)
        model.Add(class_period_block == 0).OnlyEnforceIf(z.Not())

#Objective function
for i in classes:
        c = model.NewBoolVar('c')
        model.Add(y[i] == 1).OnlyEnforceIf(c)
        model.Add(y[i] == 0).OnlyEnforceIf(c.Not())
        model.Add(sum(x[i, m, k, b] for m in rooms for k in range(1,session+1) for b in range(1,period+1)) == classes[i][0]).OnlyEnforceIf(c)
        model.Add(sum(x[i, m, k, b] for m in rooms for k in range(1,session+1) for b in range(1,period+1)) <= classes[i][0]).OnlyEnforceIf(c.Not())
model.Maximize(sum(y[i] for i in classes))

start = time.time()
#Create solver
solver = cp_model.CpSolver()
status= solver.Solve(model)
end= time.time()
#Print solution:

if status == cp_model.OPTIMAL:
    print("Solution: ")
    for i in classes:
        for m in rooms:
            for k in range(1,session+1):
                for b in range(1,period+1):
                    if solver.Value(x[i, m, k, b]):
                        print(f'Class {i+1} is assigned to room {m} at period {b} of session {k}')
    print(f'Number of class that can be scheduled: {int(solver.ObjectiveValue())}')
else:
    print("No feasible solution.")
print(f'Runtime: {end-start}')
