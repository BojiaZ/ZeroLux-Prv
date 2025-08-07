import ipc

def handle_event(event):
    print(f"收到事件: {event}")

ipc.listen_events(handle_event)

input("监听中，随时发送事件（按回车退出）...\n")
