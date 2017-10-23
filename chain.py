# Example: monitors events and logs them into a log file.
#
import pyinotify

class Log(pyinotify.ProcessEvent):
    def my_init(self, fileobj):
        """
        Method automatically called from ProcessEvent.__init__(). Additional
        keyworded arguments passed to ProcessEvent.__init__() are then
        delegated to my_init(). This is the case for fileobj.
        """
        self._fileobj = fileobj

    def process_default(self, event):
        self._fileobj.write(str(event) + '\n')
        self._fileobj.flush()

class ModificationAlert(pyinotify.ProcessEvent):
    def my_init(self, msg):
        self._msg = msg

    def process_default(self, event):
        print(self._msg)

    def process_IN_MODIFY(self, event):
        print('IN_MODIFY')

with open('/var/log/pyinotify_log', 'wt') as fo:
    # It is important to pass named extra arguments like 'fileobj'.
    eventHandler = ModificationAlert(Log(fileobj=fo), msg='An operation happened on FS')
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, eventHandler)
    wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
    notifier.loop()
