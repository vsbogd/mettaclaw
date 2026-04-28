import sock
import time

if __name__ == "__main__":
    server = sock.SockServer.singleton()
    msg = server.read_line()
    assert msg == "Hello Max!", f"Unexpected message from client: {msg}"
    time.sleep(10)
    server.send("Hello Dan!")
