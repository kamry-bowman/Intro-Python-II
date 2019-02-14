class Item:
    def __init__(
        self, name, desc=None, verb='use', verb_past='used', func=None, life=1
    ):
        self.name = name
        self.desc = desc or 'a ' + name
        self.verb = verb
        self.verb_past = verb_past
        self.func = func
        self.original_life = life
        self.life = life

    def use(self, user):
        string = f'{user.name} {self.verb_past} {self.name}\n'
        if self.func:
            string += self.func(self, user) or ''
        self.life -= 1
        if self.life == 0:
            string += user.use_up(self) or ''
        return string

    def on_drop(self):
        pass


class LightSource(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_drop(self):
        return "It's not wise to drop your light source."
