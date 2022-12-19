data = []

opp_map = dict(
    A="Rock",
    B="Paper",
    C="Scissors"
)

scores = dict(
    Rock=1,
    Paper=2,
    Scissors=3
)

superior = dict(
    Rock="Paper",
    Scissors="Rock",
    Paper="Scissors"
)

inferior = dict((v,k) for k,v in superior.items())

you_map = dict(
    X="A",
    Y="B",
    Z="C"
)

def score(opp, you):
    """
    Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
    Rock > Scissors
    Scissors > Paper
    Paper > Rock

    The winner of the whole tournament is the player with the highest score. 
    Your total score is the sum of your scores for each round. 
    The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
    plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
    """
    sup = superior[opp]
    score = 0 # Loss
    if you == opp: # Draw
        score = 3
    elif you == sup: # Win
        score = 6
    return score + scores[you] # Outcome + Shape
    


total = 0

with open("day02.txt") as fp:
    for line in fp:
        opp, you = line.strip().split()
        data.append((opp_map[opp], opp_map[you_map[you]]))
        opp, you = data[-1]
        total += score(opp, you)

print(f"{total=}")

decisions = dict(
    X="Lose",
    Y="Draw",
    Z="Win"
)

def choice(opp, decision):
    if decision == "Draw":
        return opp
    if decision == "Win":
        return superior[opp]
    return inferior[opp]



total = 0
with open("day02.txt") as fp:
    for line in fp:
        opp, decision = line.strip().split()
        opp = opp_map[opp]
        decision = decisions[decision]
        you = choice(opp, decision)
        # data.append((opp_map[opp], opp_map[you_map[you]]))
        total += score(opp, you)
    
print(f"{total=}")


