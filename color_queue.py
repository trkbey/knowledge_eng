from ai import *
from travel import knowledge

colors = ["black", "white", "blue", "green", "purple"]
symbols = []

for i in range(5):
    for c in colors:
        symbols.append(Symbol(f"{c}{i}"))

knowledge = And()

for c in colors:
    knowledge.add(Or(
        Symbol(f"{c}0"),
        Symbol(f"{c}1"),
        Symbol(f"{c}2"),
        Symbol(f"{c}3"),
        Symbol(f"{c}4"),
    ))

for c in colors:
    for i in range(5):
        for j in range(5):
            if i != j:
                knowledge.add(Implication(
                    Symbol(f"{c}{i}"),
                    Not(Symbol(f"{c}{j}"))
                ))

for i in range(5):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication(
                    Symbol(f"{c1}{i}"),
                    Not(Symbol(f"{c2}{i}"))
                ))

knowledge.add(Or(
    And(),

))