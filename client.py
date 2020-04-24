from websocket import create_connection


# test
ws = create_connection("ws://127.0.0.1:30066/log_tail")
print("client start...")
while True:
    result = ws.recv()
    print(result)
