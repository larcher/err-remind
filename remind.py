from errbot import BotPlugin, botcmd
import uuid
import pytz
import parsedatetime
from datetime import datetime
from pytz import utc 

DEFAULT_POLL_INTERVAL = 60 * 1  # one minute
DEFAULT_LOCALE = 'en_CA' # CHANGE THIS TO YOUR LOCALE

class Remind(BotPlugin):
    """Reminder plugin for errbot"""

    def activate(self):
        super(Remind, self).activate()
        self.send_reminders()
        self.start_poller(
            self.config['POLL_INTERVAL'] if self.config else DEFAULT_POLL_INTERVAL,
            self.send_reminders
        )

    def send_reminders(self):
        if 'REMINDER_IDS' not in self:
            self['REMINDER_IDS'] = []

        for reminderKey in self['REMINDER_IDS']:
            reminder = self[reminderKey]
            if (datetime.now(pytz.timezone('US/Pacific'))).replace(tzinfo=None) > reminder['date'].replace(tzinfo=None) and not reminder['sent']:
                message_type = 'chat' if reminder['is_user'] else 'groupchat'
                self.send(
                    self.build_identifier(reminder['target']),
                    "Hello {nick}, here is your reminder: {message}".format(nick=reminder['target'],
                                                                            message=reminder['message']),
                )
                reminder['sent'] = True
            elif reminder['sent'] is True:
                oldKeys = self['REMINDER_IDS']
                oldKeys.remove(reminder["id"])
                self['REMINDER_IDS'] = oldKeys

                del self[reminderKey]

            self[reminderKey] = reminder

    def add_reminder(self, date, message, target, is_user=True):
        reminder = {
            'id': uuid.uuid4().hex,
            'date': date,
            'message': message,
            'target': str(target),
            'is_user': is_user,
            'sent': False
        }
        self.store_reminder(reminder)
        return reminder

    def store_reminder(self, reminder):
        self[reminder["id"]] = reminder

        try:
            oldKeys = self['REMINDER_IDS']
            oldKeys.append(reminder["id"])
            self['REMINDER_IDS'] = oldKeys
        except KeyError:
            self['REMINDER_IDS'] = [reminder["id"]]

    @botcmd
    def remind(self, msg, args):
        """save a new reminder. Usage: !remind <date/time> -> <thing>"""

        if "->" not in args:
            return "Usage: !remind <date/time> -> <thing>. For example: !remind tomorrow 12:00 -> Lunch with the dudebros to be reminded to eat lunch with the dudebros at noon the next day."

            # if (datetime.now()).astimezone(pytz.timezone('US/Pacific')) > reminder['date'] and not reminder['sent']:
        pdt = parsedatetime.Calendar(parsedatetime.Constants(self.config['LOCALE'] if self.config else DEFAULT_LOCALE))
        date_end = args.index('->')
        date_list = args[:date_end]
        date_struct = pdt.parse(date_list, datetime.now().astimezone(pytz.timezone('US/Pacific')).timetuple())

        if date_struct[1] == 0:
            return "Your date seems malformed: {date}".format(date=date_string)

        date = (datetime(*(date_struct[0])[:6]))
        message = args[date_end + 1:]
        is_user = msg.is_direct
        target = str(msg.frm)

        if not is_user:
            head, sep, tail = target.partition('/')
            target = head

        self.add_reminder(date, message, target, is_user)

        return "Reminder set to \"{message}\" at {date}.".format(message=message, date=date)
