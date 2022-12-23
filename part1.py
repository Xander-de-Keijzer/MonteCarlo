from mt import MersenneTwister

class Part1:
    """
    A class that simulates the results of a football (soccer) league 
    using a simplified model. The probability of each team winning, 
    tying, or losing a match is determined by pre-defined win-tie-loss ratios. 
    The results of the simulations are used to determine the final league 
    standings and the percentage likelihood of each team finishing in each 
    possible position.
    """

    def __init__(self, sims=10_000):
        """
        Initialize a Part1 instance with the given number of simulations.
        
        Parameters
        ----------
        sims : int, optional
            The number of simulations to run. Default is 10_000.
        """
        self.clubs = ["Ajax", "Feyenoord", "PSV", "FC Utrecht", "Willem II"]
        self.win_tie_loss = {
            "Ajax":         {                       "Feyenoord": [65, 17, 18], "PSV": [54, 21, 25], "FC Utrecht": [74, 14, 12], "Willem II": [78, 13,  9] },
            "Feyenoord":    { "Ajax": [30, 21, 49],                            "PSV": [37, 24, 39], "FC Utrecht": [51, 22, 27], "Willem II": [60, 21, 19] },
            "PSV":          { "Ajax": [39, 22, 39], "Feyenoord": [54, 22, 24],                      "FC Utrecht": [62, 20, 18], "Willem II": [62, 22, 16] },
            "FC Utrecht":   { "Ajax": [25, 14, 61], "Feyenoord": [37, 23, 40], "PSV": [29, 24, 47],                             "Willem II": [52, 23, 25] },
            "Willem II":    { "Ajax": [17, 18, 65], "Feyenoord": [20, 26, 54], "PSV": [23, 24, 53], "FC Utrecht": [37, 25, 38]                            }
        }
        self.results = {
            "Ajax":       [0,0,0,0,0], 
            "Feyenoord":  [0,0,0,0,0],
            "PSV":        [0,0,0,0,0],
            "FC Utrecht": [0,0,0,0,0], 
            "Willem II":  [0,0,0,0,0],
        }

        self.mt = MersenneTwister(5489)
        self.sims = sims

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

                wtl = self.win_tie_loss[home][away]
                rand = self.mt.next_int(0, 100)

                if rand < wtl[0]:
                    scores[home] += 3
                elif rand < (wtl[0] + wtl[1]):
                    scores[home] += 1
                    scores[away] += 1
                else:
                    scores[away] += 3

        result = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        for i, (k, _) in enumerate(result.items()):
            self.results[k][i] += 1
