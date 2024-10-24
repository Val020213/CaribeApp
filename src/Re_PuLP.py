import pulp

def add_constraint(problem:pulp.LpProblem, name:str, constraint:callable) -> pulp.LpProblem:
    problem_copy = problem.copy()
    constraint(problem_copy)

    problem_copy.solve(pulp.PULP_CBC_CMD(timeLimit=30, msg=False))

    if pulp.LpStatus[problem_copy.status] == "Optimal":
        return problem_copy
    else:
        print(f"Constraint {name} Failed")
        return problem

def solve(
    faculties: list[str],
    athletes: dict[str, int],
    fixed: dict[str, int],
    ranking: dict[str, int],
    available_pullovers: dict[str, int],
    preferences: dict[str, list[str]] = None,
):

    ## Variable declaration
    colors = [color for color in available_pullovers.keys()]
    fixed_institutions = [participant for participant in fixed]
    institutions = faculties[:] + fixed_institutions[:]
    total_pullovers = sum(amount for amount in available_pullovers.values())
    extra_pullovers = sum(amount for amount in fixed.values())

    ## Create a new LP problem
    problem = pulp.LpProblem("Pullovers Distribution", pulp.LpMinimize)

    ## Create the variables
    # Amount of pullovers for each faculty
    x = {
        i: pulp.LpVariable(f'x_{i}', lowBound=0, cat="Integer")
        for i in faculties
    }

    xx = {
        i: pulp.LpVariable(f'x_{i}', lowBound=0, cat="Integer")
        for i in fixed_institutions
    }

    # The color of the pullovers for each faculty
    y = {
        (i, j): pulp.LpVariable(f'y_{i}_{j}', cat="Binary")
        for i in institutions
        for j in colors
    }

    # Amount of pullovers of each color for each institution
    z = {
        (i, j): pulp.LpVariable(f'z_{i}_{j}', lowBound=0 ,cat="Integer")
        for i in institutions
        for j in colors
    }

    # The difference between the amount of pullovers of the consecutive ranking places
    difference = {
        i: pulp.LpVariable(f'difference_{i}', lowBound=0)
        for i in faculties
    }

    ## Hard Constrains
    # All pullovers must be distributed
    if sum(athletes.values()) + extra_pullovers > total_pullovers:
        problem += pulp.lpSum(x[i] for i in faculties) + extra_pullovers == total_pullovers
    else:
        problem += pulp.lpSum(x[i] for i in faculties) == sum(athletes.values())

    for i in faculties:
        # Each faculty must have all pullovers of one color
        problem += pulp.lpSum(y[i, j] for j in colors) == 1
        # Each faculty must have at least 10 pullovers
        problem += x[i] >= 1
        # All distributed pullovers must be assigned to a color
        problem += sum(z[i, j] for j in colors) == x[i]

    for i in fixed_institutions:
        # Each institution must have all pullovers of one color
        problem += pulp.lpSum(y[i, j] for j in colors) == 1
        # Each institution must have exactly the amount of pullovers provided
        problem += xx[i] == fixed[i]
        # All distributed pullovers must be assigned to a color
        problem += sum(z[i, j] for j in colors) == xx[i]

    for j in colors:
        # The amount of pullovers of each color must be less or equal to the available pullovers
        problem += pulp.lpSum(z[i, j] for i in institutions) <= available_pullovers[j]

    # The amount of pullovers of each color must be less or equal to the available pullovers if
    # the color is the assigned one else it must be 0
    for i in institutions:
        for j in colors:
            problem += z[i, j] <= y[i, j] * total_pullovers

    # The difference between the amount of pullovers of the consecutive ranking places must be the difference
    # between proportions of the assigned pullovers to the faculties and the amount of athletes in the faculty
    for i in faculties:
        if not ranking[i] + 1 in ranking.values():
            problem += difference[i] == 0

        for f in faculties:
            if ranking[i] == ranking[f] + 1:
                problem += x[i] * athletes[f] - x[f] * athletes[i] >= difference[i] * athletes[i] * athletes[f]
                problem += x[f] * athletes[i] - x[i] * athletes[f] >= difference[i] * athletes[i] * athletes[f]


    ## Objective Function
    # Minimize sum of absolute differences between the amount of pullovers of the consecutive ranking places
    problem += pulp.lpSum(difference[i] for i in faculties)

    ## Soft Constrains
    # All faculties must have at least 10 pullovers or fewer if the amount of athletes is less than 10
    def constraint_min_pullovers(p):
        for f1 in faculties:
            p += x[f1] >= min(athletes[f1], 10)

    # If faculty a has better ranking than faculty b then it must have more pullovers
    def constraint_brmp(p):
        for f1 in faculties:
            for f2 in faculties:
                if ranking[f1] > ranking[f2]:
                    p += x[f1] >= x[f2]

    # If faculty a has more athletes than faculty b then it must have more pullovers
    def constraint_mamp(p):
        for f1 in faculties:
            for f2 in faculties:
                if athletes[f1] > athletes[f2]:
                    p += x[f1] >= x[f2]

    def constraint_color_soft(p):
        for f1 in faculties:
            if not preferences:
                break

            preference = preferences.get(f1, None)
            if preference:
                p += sum(y[f1, c] for c in preference) == 1

    def constraint_color_hard(p):
        for f1 in faculties:
            if not preferences:
                break

            preference = preferences.get(f1, None)
            if preference:
                p += y[f1, preference[0]] == 1

    ordered_constraints = [
        ("set min pullovers", constraint_min_pullovers),
        ("best ranking more pullovers", constraint_brmp),
        ("more athletes more pullovers", constraint_mamp),
        ("color soft", constraint_color_soft),
        ("color hard", constraint_color_hard),
    ]

    ## Get problem solution
    # for name, constraint in ordered_constraints:
    #     problem = add_constraint(problem, name, constraint)

    problem.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[problem.status] != 'Optimal':
        return None

    ## Extract solution info
    final_distribution = {
        "Solution": {
            i: {c: pulp.value(z[i, c]) for c in colors}
            for i in institutions
        },
        "Binary": {
            i: {c: pulp.value(y[i, c]) for c in colors}
            for i in institutions
        },
        "Faculties": {
            i: pulp.value(x[i])
            for i in faculties
        },
        "Fixed_Institutions": {
            i: pulp.value(xx[i])
            for i in fixed_institutions
        },
    }

    return final_distribution