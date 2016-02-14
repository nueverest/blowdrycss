# builtins
import logging
from time import sleep
# plugins
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent, FileDeletedEvent
from watchdog.observers import Observer
# custom
from blowdrycss.utilities import print_blow_dryer
from blowdrycss import blowdry
import blowdrycss_settings as settings


class FileEditEventHandler(PatternMatchingEventHandler):
    """ Child of PatternMatchingEventHandler that only runs blowdry.main() during file 'modified' or 'deleted' events.
    The 'modified' case handles both the 'created' and 'moved' case. When a file is created or moved/copy/pasted
    into the project_directory, 'modified' is triggered. This reduces a number of unnecessary calls to blowdry.main().

    """
    @staticmethod
    def print_status():
        file_types = '(' + ', '.join(settings.file_types) + ')'

        print()
        print('-' * 96)
        print(
            'The blowdrycss watchdog is watching all', file_types, 'files',
            '\nin the project directory:', settings.project_directory
        )
        print('-' * 96)
        print('Pressing Ctrl + C stops the process.')
        print()

    @staticmethod
    def excluded(src_path=''):
        """
        :param src_path:
        :return: (*bool*) -- Return True if ``src_path`` ends with a file in ``excluded_files``

        """
        excluded_files = ('clashing_aliases.html', 'property_aliases.html')
        for excluded_file in excluded_files:
            if src_path.endswith(excluded_file):
                return True
        return False

    def on_modified(self, event):
        """ Called when a file or directory is modified. Only FileModifiedEvents trigger action.

        :type event: :class:`watchdog.event.DirModifiedEvent` or :class:`watchdog.event.FileModifiedEvent`
        :param event: Event representing file modification.

        """
        if type(event) == FileModifiedEvent and not self.excluded(src_path=event.src_path):
            logging.debug('  ' + event.event_type + ' :: ' + str(event.key))
            blowdry.main()
            self.print_status()

    def on_deleted(self, event):
        """ Called when a file or directory is deleted. Only FileDeletedEvents triggers blowdry.main().

        :type event: :class:`watchdog.event.DirDeletedEvent` or :class:`watchdog.event.FileDeletedEvent`
        :param event: Event representing file deletion.

        """
        if type(event) == FileDeletedEvent and not self.excluded(src_path=event.src_path):
            logging.debug('  ' + event.event_type.ljust(8) + ' :: ' + str(event))
            blowdry.main()
            self.print_status()


def main():
    """ If ``settings.auto_generate == True`` indefinitely run blowdrycss inside of the watchdog wrapper.
    The wrapper creates and attaches an file event handler to an observer. When a file is modified or
    deleted it triggers blowdry.main().

    Else, blowdry.main() is run once.

    :return: None

    **Example**

    >>> from blowdrycss import watchdogwrapper
    >>> # blowdrycss_settings.auto_generate = True
    >>> watchdogwrapper.main()
    ------------------------------------------------------------------------------------------------
    blowdry_watchdog is now watching all (.html) files
    in the project directory: <project directory>
    ------------------------------------------------------------------------------------------------
    Pressing Ctrl + C stops the process.
    >>> # blowdrycss_settings.auto_generate = True
    >>> watchdogwrapper.main()
    ☴ blowdrycss started ☴
    ...

    """
    if settings.auto_generate:
        # logging.basicConfig(level=logging.DEBUG)                  # Uncomment for testing

        event_handler = FileEditEventHandler(
                patterns=list(settings.file_types),
                ignore_patterns=[],
                ignore_directories=True
        )

        observer = Observer()
        observer.schedule(event_handler, settings.project_directory, recursive=True)
        observer.start()

        event_handler.print_status()

        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print_blow_dryer()

        observer.join()
    else:
        blowdry.main()


if __name__ == '__main__':
    main()
