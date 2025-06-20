from ai import *

rain = Symbol("rain")
david = Symbol("david")
michael = Symbol("michael")

knowledge = And(
    Implication(Not(rain), david),
    Or(david, michael),
    Not(And(michael, david)),
    michael
)

print(knowledge.formula()) #that gives us to logical formula of kb
print(model_check(knowledge, david))

