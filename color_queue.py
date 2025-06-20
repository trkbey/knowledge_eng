from ai import *
from travel import knowledge

colors = ["black", "white", "blue", "purple"]
symbols = []

for i in range(4):
    for c in colors:
        symbols.append(Symbol(f"{c}{i}"))

knowledge = And()

for c in colors:
    knowledge.add(Or(
        Symbol(f"{c}0"),
        Symbol(f"{c}1"),
        Symbol(f"{c}2"),
        Symbol(f"{c}3"),

    ))

for c in colors:
    for i in range(4):
        for j in range(4):
            if i != j:
                knowledge.add(Implication(
                    Symbol(f"{c}{i}"),
                    Not(Symbol(f"{c}{j}"))
                ))

for i in range(4):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication(
                    Symbol(f"{c1}{i}"),
                    Not(Symbol(f"{c2}{i}"))
                ))

knowledge.add(Or(
And(Symbol("black0"), Symbol("white1"), Not(Symbol("blue2")), Not(Symbol("purple3"))),
    And(Symbol("black0"), Symbol("blue2"), Not(Symbol("white1")), Not(Symbol("purple3"))),
    And(Symbol("black0"), Symbol("purple3"), Not(Symbol("white1")), Not(Symbol("blue2"))),
    And(Symbol("white1"), Symbol("blue2"), Not(Symbol("black0")), Not(Symbol("purple3"))),
    And(Symbol("white1"), Symbol("purple3"), Not(Symbol("black0")), Not(Symbol("blue2"))),
    And(Symbol("blue2"), Symbol("purple3"), Not(Symbol("black0")), Not(Symbol("white1")))

))

knowledge.add(And(
    Not(Symbol("white0")),
    Not(Symbol("black1")),
    Not(Symbol("blue2")),
    Not(Symbol("purple3"))
))

for  s in symbols:
    if model_check(knowledge, s):
        print(s)