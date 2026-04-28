import sock

class LlmMockAgent:

    def __init__(self):
        self.rpc = sock.Server()
        self.rpc.start()

    def __del__(self):
        self.rpc.stop()

    def chat(self, content):
        self.rpc.send(content)
        return self.rpc.read_line()




