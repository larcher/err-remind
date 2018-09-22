from errbot import BotPlugin, botcmd
import uuid
import pytz
import parsedatetime
from datetime import datetime
from pytz import utc

DEFAULT_POLL_INTERVAL = 60 * 1  # one minute
DEFAULT_LOCALE = 'en_CA' # CHANGE THIS TO YOUR LOCALE

class Remind(BotPlugin):
    """Reminded plugin for errbot"""

    @botcmd
    def remind(self, msg, args):
        """save a new reminder. Usage: !remind <date/time> -> <thing>"""

        if "->" not in args:
            return "Usage: !remind <date/time> -> <thing>. For example: !remind tomorrow 12:00 -> Lunch with the dudebros to be reminded to eat lunch with the dudebros at noon the next day."

        pdt = parsedatetime.Calendar(parsedatetime.Constants(self.config['LOCALE'] if self.config else DEFAULT_LOCALE))
        date_end = args.index('->')
        date_list = args[:date_end]
        date_struct = pdt.parse(date_list, datetime.now().timetuple())

        if date_struct[1] == 0:
            return "Your date seems malformed: {date}".format(date=date_string)

        date = pytz.utc.localize(datetime(*(date_struct[0])[:6]))
        message = args[date_end + 1:]
        is_user = msg.is_direct
        target = msg.frm
#            self.add_reminder(date, message, target, is_user)
        return "Reminder set to \"{message}\" at {date}.".format(message=message, date=date)
