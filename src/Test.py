from exceptiongroup import print_exc

from Re_PuLP import solve
import json

separator = '=' * 20


def load_from_json(filename="data.json"):
    # Read data from the JSON file
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    # Extract the variables from the data
    faculties = data.get("faculties", [])
    athletes = data.get("athletes", {})
    fixed = data.get("fixed", {})
    ranking = data.get("ranking", {})
    available_pullovers = data.get("available_pullovers", {})
    preferences = data.get("preferences", None)  # Use None if preferences is not present

    return faculties, athletes, fixed, ranking, available_pullovers, preferences

def main():

    solution = test2()

    if solution is None:
        print("Incompatible problem")
        return 0

    for category in solution.keys():
        print(f"{separator}\n{category}\n{separator}")
        for i, j in solution[category].items():
            print(f"{i}: {j}\n")

def test1():

    faculties = ['A', 'B', 'C']
    athletes = {'A': 10, 'B': 20, 'C': 30}
    fixed = {'D': 40, 'E': 50}
    ranking = {'A': 1, 'B': 2, 'C': 3}
    available_pullovers = {'red': 90, 'blue': 30, 'green': 30}

    return solve(faculties, athletes, fixed, ranking, available_pullovers)

def test2():

    faculties, athletes, fixed, ranking, available_pullovers, preferences = load_from_json(filename="./test_cases/test2.json")
    print(faculties)
    print(athletes)
    print(fixed)
    print(ranking)
    print(available_pullovers)
    print(preferences)

    for f in faculties:
        if f not in athletes:
            print(f"{separator}\nFaculty {f} is not in athletes\n{separator}")
        if f not in ranking:
            print(f"{separator}\nFaculty {f} is not in ranking\n{separator}")
    for c in preferences.values():
        if c[0] not in available_pullovers:
            print(f"{separator}\nColor {c[0]} is not in preferences\n{separator}")

    return solve(faculties, athletes, fixed, ranking, available_pullovers, preferences)



if __name__ == '__main__':
    main()