class Hero:
    def __init__(self, name):
        self.name = name
        self.badAgainsts = []
        self.goodAgainsts = []
        self.matchups = []
    def toDict(self):
        return {
            'name': self.name,
            'badAgainsts': self.badAgainsts,
            'goodAgainsts': self.goodAgainsts,
            'matchups': self.matchups
        }