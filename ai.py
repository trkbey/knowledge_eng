class Sentence():

    # evauates the sentence
    def evaluate(self, model):
        raise Exception("nothing to evaluate")

    #returns the formula repsenting logical sentence
    def formula(self):
        return ""

    #returns a set of all symbols in the logical sentence
    def symbols(self):
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    #parenthesize an expression if not
    def parenthesize(cls, s):
        #checks if a string has balanced parentheses
        def balanced(s):
            count = 0
            for c in s:
                if c == '(':
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])):
            return s
        else:
            return f"({s})"

class Symbol(Sentence):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise EvaluationException(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts):
        for con in conjuncts:
            Sentence.validate(con)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self):
        return hash(
            ("and", tuple(hash(con) for con in self.conjuncts))
        )

    def __repr__(self):
        conjuctions = ", ".join([str(con) for con in self.conjuncts])
        return f"And({conjuctions})"

    def add(self, con):
        Sentence.validate(con)
        self.conjuncts.append(con)

    def evaluate(self, model):
        return all(con.evaluate(model) for con in self.conjuncts)

    def formula(self):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(con.formula()) for con in self.conjuncts])

    def symbols(self):
        return set.union(*[con.symbols() for con in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts):
        for dis in disjuncts:
            Sentence.validate(dis)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(
            ("or", tuple(hash(dis) for dis in self.disjuncts))
        )

    def __repr__(self):
        disjuncts = ", ".join([str(dis) for dis in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        return any(dis.evaluate(model) for dis in self.disjuncts)

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨ ".join([Sentence.parenthesize(dis.formula()) for dis in self.disjuncts])

    def symbols(self):
        return set.union(*[dis.symbols() for dis in self.disjuncts])


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (isinstance(other, Implication)
                and self.antecedent == other.antecedent
                and self.consequent == other.consequent)

    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        return ((not self.antecedent.evaluate(model))
                or self.consequent.evaluate(model))

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Biconditional)
                and self.left == other.left
                and self.right == other.right)

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))

    def formula(self):
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())

#checks if knowledge base entails query
def model_check(knowledge, query):
    #checks if knowledge base entails query given a particular model
    def check_all(knowledge, query, symbols, model):
        if not symbols:
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:
            #choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            #create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            #create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            #ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    #get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())
    #check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())
