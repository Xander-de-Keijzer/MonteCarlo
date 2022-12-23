from part1 import Part1
from part2 import Part2

def main():
    inp = input("Type '1' or '2' to run that part or type anyting else to exit: ")
    if inp == "1":
        sims = input("How many sims to run (default 10_000): ")
        try:
            sims = int(sims)
        except:
            sims = 10_000
        p1 = Part1(sims)
        p1.run_simulations()
    elif inp == "2":
        sims = input("How many sims to run (default 10_000): ")
        try:
            sims = int(sims)
        except:
            sims = 10_000
        goals = input("Max goals scored to simulate (default 10): ")
        try:
            goals = int(goals)
        except:
            goals = 10
        p2 = Part2(sims, goals)
        p2.run_simulations()
    else:
        return
    main()


if __name__ == "__main__":
    main()