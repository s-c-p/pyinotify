# sudo python3 chain.py
#
# ls /tmp
# echo "Hello Moto!" >> /tmp/random-file.txt
#
# ^C
# cat /var/log/pyinotify_log
import pyinotify

class Log(pyinotify.ProcessEvent):
    def my_init(self, fileobj):
        """ unfortunately, this lib was written before with...as.. contruct
        was introduced and uses a hackish way :-(
        super's __init__ call proprietary `my_init` of all derived classes
        Method automatically called from ProcessEvent.__init__(). Additional
        keyworded arguments passed to ProcessEvent.__init__() are then
        delegated to my_init(). This is the case for fileobj.
        """
        self._fileobj = fileobj

    def process_default(self, event):
        self._fileobj.write(str(event) + '\n')
        self._fileobj.flush()

class ModificationAlert(pyinotify.ProcessEvent):
    """ prints a msg for all events on FileSystem but goes beyond that and
    prints a detailed prompt whenever an IN_MODIFY (i.e. file modified)
    operation takes place
    """
    def my_init(self, msg):
        self._msg = msg

    def process_default(self, event):
        print(self._msg)

    def process_IN_MODIFY(self, event):
        # TODO: improve the print message
        print('IN_MODIFY')

with open('/var/log/pyinotify_log', 'wt') as fo:
    # It is important to pass named extra arguments like 'fileobj'.
    eventHandler = ModificationAlert(Log(fileobj=fo), msg='An operation happened on FS')
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, default_proc_fun=eventHandler)
    wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
    notifier.loop()

