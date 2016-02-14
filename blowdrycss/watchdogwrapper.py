# builtins
from time import sleep
# plugins
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
# custom
import blowdrycss.blowdrycss_settings as settings
from blowdrycss import blowdry


import logging
logging.basicConfig(level=logging.DEBUG)


class FileEditEventHandler(PatternMatchingEventHandler):
    """ Child of PatternMatchingEventHandler
    """
    def on_any_event(self, event):
        logging.debug(event)
        # blowdry.main()

event_handler = FileEditEventHandler(
        patterns=list(settings.file_types),
        ignore_patterns=[],
        ignore_directories=True
)

observer = Observer()
observer.schedule(event_handler, settings.project_directory, recursive=True)
observer.start()

print('-' * 96)
print(
    'Watchdog is now watching all files of type:', settings.file_types,
    '\nin the project directory:', settings.project_directory
)
print('-' * 96)
print('Press Ctrl + C to exit.')

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
