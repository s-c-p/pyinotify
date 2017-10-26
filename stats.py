# Example: prints statistics.
#
import pyinotify

class Identity(pyinotify.ProcessEvent):
    """ think of this as a collection of suite-of-functions that are executed
    whenever a FS-event occours. If it needs anything from outside at the time
    of instanciation, define it in my_init IFF that thing is defined under the
    ProcessEvent class (e.g. pyinotofy.Stats()) you can skip it directly
    """
    def process_default(self, event):
        # Does nothing, just to demonstrate how stuffs could trivially
        # be accomplished after having processed statistics.
        print 'I am called after stats are calculated'

def on_loop(notifier):
    s_inst = notifier.proc_fun().nested_pevent()
    print repr(s_inst), '\n-----\n', s_inst, '\n---------------\n'


# Stats is a subclass of ProcessEvent provided by pyinotify
# for computing basics statistics.
s = pyinotify.Stats()
proc_function = Identity(s)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(
    wm,
    read_freq=1,
    default_proc_fun=proc_function # calls the suite of functions defined in Identity
)
wm.add_watch(
    '/var/log',
    rec=True,
    auto_add=True,
    mask=pyinotify.ALL_EVENTS
)
notifier.loop(callback=on_loop)

