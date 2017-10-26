# TODO: put ``daemonize=True`` or other things in notifier's
# instanciation
# 
# Example: daemonize pyinotify's notifier.
# rm /tmp/pyinotify.*
# python3 daemon.py
# cat /tmp/pyinotify.pid
# cat /tmp/pyinotify.log # maybe kill -9 PID
# cat /tmp[TAB]
# cat /tmp/pyinotify.log
#
import sys
import pyinotify

counter = int()

def on_loop(notifier):
    """
    Dummy function called after each event loop, this method only
    ensures the child process eventually exits (after 5 iterations).
    """
    if counter > 40:
        # Loop 40 times before daemon is killed
        print("Exit\n")
        notifier.stop()
        sys.exit(0)
    else:
        print("-------------------Loop %d\n" % counter)
        globals()["counter"] += 1

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.add_watch('/home/ubuntu-gnome', pyinotify.ALL_EVENTS)

# Notifier instance spawns a new process when daemonize is set to True. This
# child process' PID is written to /tmp/pyinotify.pid (it also automatically
# deletes it when it exits normally). Note that this tmp location is just for
# the sake of the example to avoid requiring administrative rights in order
# to run this example. But by default if no explicit pid_file parameter is
# provided it will default to its more traditional location under /var/run/.
# Note that in both cases the caller must ensure the pid file doesn't exist
# before this method is called otherwise it will raise an exception.
# /tmp/pyinotify.log is used as log file to dump received events. Likewise
# in your real code choose a more appropriate location for instance under
# /var/log (this file may contain sensitive data). Finally, callback is the
# above function and will be called after each event loop.
try:
    notifier.loop(daemonize=True, callback=on_loop,
                  pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
except pyinotify.NotifierError as err:
    print(err)
