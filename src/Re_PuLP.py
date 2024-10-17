import pulp

# Tasks:
# 1. Verify how to insert in code pullovers that receive a certain amount of pullovers
# Idea: Create a new variable for the institutions that receive a fixed amount of pullovers


def solve(
    faculties: list[str],
    athletes: dict[str, int],
    ranking: dict[str, int],
    available_pullovers: dict[str, int],
    pullovers_for_referees: int,
    pullovers_for_teachers: int,
    pullovers_for_athletes: int,
    color_for_referees: str = None,
    color_for_teachers: str = None,
    color_for_athletes: str = None,
    preferences: dict[str, list[str]] = None,
):

    ## Variable declaration
    colors = [color for color in available_pullovers.keys()]
    total_pullovers = sum(amount for amount in available_pullovers.values())
    extra_pullovers = pullovers_for_referees + pullovers_for_teachers + pullovers_for_athletes

    ## Create a new LP problem
    problem = pulp.LpProblem("Pullovers Distribution", pulp.LpMinimize)

    ## Create the variables
    # Amount of pullovers for each faculty
    x = {
        i: pulp.LpVariable(f'x_{i}', lowBound=0, cat="Integer")
        for i in faculties
    }

    # The color of the pullovers for each faculty
    y = {
        (i, j): pulp.LpVariable(f'y_{i}_{j}', cat="Binary")
        for j in colors
        for i in faculties
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
        problem += pulp.lpSum(x[i] for i in faculties) == sum(athletes.values()) + extra_pullovers

    for i in faculties:
        # Each faculty must have all pullovers of one color
        problem += pulp.lpSum(y[i, j] for j in colors) == 1
        # Each faculty must have at least 10 pullovers
        problem += x[i] >= 10

    for j in colors:
        # The amount of pullovers of each color must be less or equal to the available pullovers
        problem += pulp.lpSum(x[i] * y[i, j] for i in faculties) <= available_pullovers[j]

    # The difference between the amount of pullovers of the consecutive ranking places must be the difference
    # between proportions of the assigned pullovers to the faculties and the amount of athletes in the faculty
    for i in faculties:
        if not ranking[i] + 1 in ranking.values():
            problem += difference[i] == 0

        for f in faculties:
            if ranking[i] == ranking[f] + 1:
                problem += x[i] * athletes[f] - x[f] * athletes[i] >= difference[i] * athletes[i] * athletes[f]
                problem += x[f] * athletes[i] - x[i] * athletes[f] >= difference[i] * athletes[i] * athletes[f]

    ## Soft Constrains


    ## Objective Function
    # Minimize sum of absolute differences between the amount of pullovers of the consecutive ranking places
    problem += pulp.lpSum(difference[i] for i in faculties)
