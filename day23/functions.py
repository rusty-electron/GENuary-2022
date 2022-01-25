axiom = 'AB'

rules = {
            'A': 'AB',
            'B': 'A',
        }

class L_System:
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules
        self.current_sentence = axiom

    def generate(self):
        next_sentence = ""
        for ch in self.current_sentence:
            found = False
            for k, v in self.rules.items():
                if k == ch:
                    found = True
                    next_sentence += v
                    break
            if not found:
                next_sentence += ch
        self.current_sentence = next_sentence
        return next_sentence

if __name__ == "__main__":
    lsys = L_System(axiom, rules)
    for _ in range(5):
        print(lsys.current_sentence)
        lsys.generate()
