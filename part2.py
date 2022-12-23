from mt import MersenneTwister
import numpy as np

class Part2:
    """
    A class that simulates the results of a football (soccer) 
    league using a more advanced model. The probability of a 
    team scoring a goal is determined by statistical data on 
    the team's home and away scoring and conceding averages. 
    The results of the simulations are used to determine the 
    final league standings and the percentage likelihood of 
    each team finishing in each possible position.
    """
    
    def __init__(self, sims=10_000, goal_sims=10):
        """
        Initialize a Part2 instance with the given number of simulations and number of goals to simulate.
        
        Parameters
        ----------
        sims : int, optional
            The number of simulations to run. Default is 10_000.
        goal_sims : int, optional
            The number of goals to simulate for each match. Default is 10.
        """
        self.clubs =             [ "Ajax",               "Feyenoord",               "PSV",               "FC Utrecht",               "Willem II"               ]
        self.stats = {
            "HS":           { "Ajax": 3.2,          "Feyenoord": 2.4,          "PSV": 2.1,          "FC Utrecht": 1.9,          "Willem II": 1.4          },
            "HC":           { "Ajax": 0.9,          "Feyenoord": 1.1,          "PSV": 0.7,          "FC Utrecht": 1.2,          "Willem II": 1.7          },
            "AS":           { "Ajax": 3.1,          "Feyenoord": 2.2,          "PSV": 1.8,          "FC Utrecht": 3,            "Willem II": 1            },
            "AC":           { "Ajax": 0.6,          "Feyenoord": 0.8,          "PSV": 1.3,          "FC Utrecht": 2.4,          "Willem II": 1.5          }
        }
        self.results =           { "Ajax": [0,0,0,0,0],  "Feyenoord": [0,0,0,0,0],  "PSV": [0,0,0,0,0],  "FC Utrecht": [0,0,0,0,0],  "Willem II": [0,0,0,0,0]  }

        self.mt = MersenneTwister(5489)
        self.sims = sims
        self.goal_sims = goal_sims

    def run_simulations(self):
        """
        Run the simulations and print the results.
        """
        for _ in range(self.sims):
            self.run_simulation()

        for key in self.results:
            self.results[key] = [x / self.sims * 100 for x in self.results[key]]
            print(f"{key:<10}: {self.results[key][0]:.2f}%    {self.results[key][1]:.2f}%    {self.results[key][2]:.2f}%    {self.results[key][3]:.2f}%    {self.results[key][4]:.2f}%")


    def run_simulation(self):
        """
        Run a single simulation and update the results.
        """
        scores = {"Ajax": 0, "Feyenoord": 0, "PSV": 0, "FC Utrecht": 0, "Willem II": 0}
        for home in self.clubs:
            for away in self.clubs:
                if home == away:
                    continue

                home_power = (self.stats["HS"][home] + self.stats["AC"][away]) / 2
                away_power = (self.stats["HC"][home] + self.stats["AS"][away]) / 2
                home_goals = [(home_power**k) / np.math.factorial(k) * (np.e**(-home_power)) for k in range(self.goal_sims)]
                away_goals = [(away_power**k) / np.math.factorial(k) * (np.e**(-away_power)) for k in range(self.goal_sims)]

                home_randf = self.mt.next_float(0.0,1.0)
                away_randf = self.mt.next_float(0.0,1.0)
                home_score = 0
                away_score = 0

                for i in range(self.goal_sims):
                    home_score = i
                    if home_randf < sum(home_goals[:i+1]):
                        break

                for i in range(self.goal_sims):
                    away_score = i
                    if away_randf < sum(away_goals[:i+1]):
                        break

                if home_score > away_score:
                    scores[home] += 3
                if home_score == away_score:
                    scores[home] += 1
                    scores[away] += 1
                if home_score < away_score:
                    scores[away] += 1

        result = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        for i, (k, _) in enumerate(result.items()):
            self.results[k][i] += 1
