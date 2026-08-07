from threading import Thread

def worker():
    print("Worker thread started")
    print("Worker thread finished")

thread = Thread(target=worker)

thread.start()

print("Main thread working")