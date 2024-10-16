from numpy import random as rnd

class Solver:
    def __init__(
            self,
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
            heuristic_function: callable = lambda x: 0
    ):
        self.faculties = faculties
        self.athletes = athletes
        self.ranking = ranking
        self.available_pullovers = available_pullovers
        self.pullovers_for_referees = pullovers_for_referees
        self.pullovers_for_teachers = pullovers_for_teachers
        self.pullovers_for_athletes = pullovers_for_athletes
        self.color_for_referees = color_for_referees
        self.color_for_teachers = color_for_teachers
        self.color_for_athletes = color_for_athletes
        self.preferences = preferences
        self.heuristic_function = heuristic_function

    def solve(self, seed=None):
        if seed is None:
            seed = rnd.randint(0, 1000)

        rnd.seed(seed)
        solution = self.get_best_distribution()

        return solution, seed

    def get_best_distribution(self):

        distribution = self.get_random_distribution()
        score = self.heuristic_function(distribution)

        return distribution, score

    def get_random_distribution(self):
        distribution = {
            'referees': (self.pullovers_for_referees, self.color_for_referees),
            'teachers': (self.pullovers_for_teachers, self.color_for_teachers),
            'athletes': (self.pullovers_for_athletes, self.color_for_athletes),
        }

        return distribution

