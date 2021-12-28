
from .logitem import LogItem
from .verbosity import Verbosity, DEFAULT, MOST_VERBOSE

class Log:
    
    def __init__(self) -> None:
        self._history: list[LogItem] = []
    
    @staticmethod
    def _conditionalPrint(item: LogItem, category: str=None, verbosity:Verbosity=None) -> bool:
        """If the logger should print this particular item, prints it
        
        * By default (no category or verbosity specified), it checks whether the
          item's categories are in the watched categories. If so, it will print
          out if the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.
          Otherwise it will print out if the verbosity is less than the given
          verbosity, or the `logger.max_verbosity` setting if that isn't 
          provided.
        * If a category is specified, it will print if the item is in that
          category and the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.

        Args:
        * `item` (`LogItem`): item to check
        * `category` (`str`, optional): category  to filter by. Defaults to `None`.
        * `verbosity` (`Verbosity`, optional): greatest verbosity to print. Defaults to `None`.
        
        Returns:
        * `bool`: whether it was printed
        """
        # Make sure we log things, even if the context isn't loaded
        # They will still (hopefully) be recallable later
        try:
            context = common.getContext()
        except common.contextmanager.MissingContextException:
            verbosity = DEFAULT
        else:
            if verbosity is None:
                if item.category in context.settings.get("logger.watched_categories"):
                    verbosity = context.settings.get("logger.max_watched_verbosity")
                else:
                    verbosity = context.settings.get("logger.max_verbosity")
        
        assert(verbosity is not None)
        if item.verbosity <= verbosity:
            print(item)
            return True
        else:
            return False

    def recall(self, category: str, verbosity: Verbosity = DEFAULT, number: int = -1):
        """
        Recall and print all matching log entries for the provided category at 
        the given verbosity level or higher, with the latest item being logged
        first

        ### Args:
        * `category` (`str`): category to match
        * `verbosity` (`Verbosity`, optional): verbosity level. Defaults to `DEFAULT`.
        * `number` (`int`): number of values to recall
        """
        num_prints = 0
        for item in reversed(self._history):
            # Print if required
            if self._conditionalPrint(item, category, verbosity):
                num_prints += 1
            if num_prints == number:
                break
    
    def details(self, itemNumber: int):
        """
        Print the details of a log entry.

        ### Args:
        * `itemNumber` (`int`): entry number
        """
        self._history[itemNumber].printDetails()

    def __call__(self, category: str, msg: str, verbosity: Verbosity = DEFAULT) -> None:
        """
        Add a message to the log

        The message is stored in the log history, as well as being printed if
        it falls under one of the printable categories, or is at a verbosity
        level high enough to demand attention

        ### Args:
        * `category` (`str`): category to log under
        * `msg` (`str`): message to log
        * `verbosity` (`Verbosity`, optional): verbosity to log under. Defaults to `DEFAULT`.
        """
        # TODO: Maybe get traceback
        item = LogItem(category, msg, verbosity, len(self._history))
        self._history.append(item)
        # Print if required
        self._conditionalPrint(item)

log = Log()

import common
