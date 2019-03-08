class Parser(object):

    def __init__(self, client, triggers):
        self.client = client
        self.triggers = triggers
        self.commands = []

    async def execute(self, message):
        for command in self.commands:
            await command.execute(message)
        
    def match(self, message):
        for command in self.commands:
            x = command.match(message)
            if x:
                return x

    def getio(self, message):
        for command in self.commands:
            x = command.match(message)
            if x:
                return command.getio()
        return 0

    def add(self, cmd): 
        if not cmd.client:
            cmd.client = self.client
        if not cmd.triggers:
            cmd.triggers = self.triggers
            cmd.compile()
        self.commands.append(cmd)