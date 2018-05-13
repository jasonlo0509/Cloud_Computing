import pyinotify

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        if not (".sw") in event.pathname:
                print "CLOSE_WRITE event:", event.pathname
def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('./', pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()
