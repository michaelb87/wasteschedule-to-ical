from flask import Flask, Response
from flask_caching import Cache
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import icalendar
import time
import uuid

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

cache_timeout = 7200  # 2 hours in seconds

def get_html():
    print('Fetching HTML...')
    # Retrieve the data
    r = requests.get('https://www.aschach-steyr.at/Buergerservice/Abfall_Termine/Kalender')
    return r.text

def generate_ical():
    # Parse the HTML
    html = get_html()
    soup = BeautifulSoup(html, 'html.parser')

    # Get the table
    table = soup.find('table', class_='ris_table')

    # Get the calendar events
    events = []
    for row in table.find_all('tr')[1:]:
        date_str = row.find('td', class_='td_kal').text.strip()
        event_str = row.find('a').text.strip()
        event_type = row.find('span').text.strip()

        # Remove the weekday from the date string
        date_str = date_str.split(' ')[0]

        date = datetime.strptime(date_str, '%d.%m.%Y')

        # Create an event with all-day setting
        event = icalendar.Event()
        event.add('dtstart', date)
        event.add('dtend', date + timedelta(days=1))
        event.add('x-prop-allday', '1')

        # Add DTSTAMP property
        event.add('dtstamp', datetime.utcnow())

        # Add UID property
        event.add('uid', str(uuid.uuid4()))  # Generate a unique UID using UUID

        # Add summary, location, and other event details
        event.add('summary', event_str)
        event.add('location', 'Aschach an der Steyr, Austria')

        # Create and add reminder
        reminder = icalendar.Alarm()
        reminder.add('action', 'DISPLAY')
        reminder.add('trigger', date - timedelta(hours=6))
        reminder.add('description', 'Reminder: ' + event_str)
        event.add_component(reminder)

        events.append(event)

    # Create the iCal calendar
    cal = icalendar.Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//Google Inc//iCal4j 1.0//EN')
    cal.add('method', 'PUBLISH')
    cal.add('name', 'Abfall Termine')
    cal.add('description', 'Abfall Termine für Aschach an der Steyr, Österreich')
    cal.add('x-wr-calname', 'Abfall Termine')
    cal.add('x-wr-timezone', 'Europe/Vienna')
    cal.add('x-wr-caldesc', 'Abfall Termine für Aschach an der Steyr, Österreich')
    cal.add('x-published-ttl', 'PT12H')

    # Add events to the calendar
    for event in events:
        cal.add_component(event)

    # Generate the iCal string
    ical_string = cal.to_ical()
    return ical_string

@app.route('/')
@cache.cached(timeout=cache_timeout)
def get_ical():
    ical_string = generate_ical()
    return Response(ical_string, mimetype='text/calendar')

if __name__ == '__main__':
    app.run(debug=True)
