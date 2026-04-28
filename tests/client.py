import sock

if __name__ == "__main__":
    client = sock.SockClient.singleton()
    client.connect()
    msg = client.chat("Hello Max!")
    assert msg.strip() == "Hello Dan!", f"Unexpected message from server: {msg}"
