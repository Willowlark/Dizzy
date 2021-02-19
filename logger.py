from os.path import join
from os import makedirs

class Classic_Log(object):
    
    def __init__(self, root_path):
        self.root_path = root_path
        
    def log(self, message):
        path = join(self.root_path, message.channel.name)
        makedirs(path, exist_ok=1)
        with open(join(path,message.created_at.date().isoformat()+'.txt'), 'a') as f:
            try:
                name = message.author.nick
                assert name is not None
            except:
                name = message.author.name
            f.write(name + ": " + message.content + '\n')
            print(message.channel.name.upper() + ": " + name + ": " + message.content)
            
REFERENCE = {
    'Classic_Log': Classic_Log
}