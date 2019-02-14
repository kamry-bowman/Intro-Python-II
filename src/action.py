class Action:
    def __init__(self, key, act, desc, **kwargs):
        self.key = key
        self.act = act
        self.desc = desc
        self.target_string = kwargs.get('target_string') or False

    def announce(self):
        if self.target_string:
            return f'{self.key} <{self.target_string}>: {self.desc}\n'
        else:
            return f'{self.key}: {self.desc}\n'
