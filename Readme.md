Scrapes waste disposal schedule and serves them as ical.
Caches is enabled and set to two hours.

**requirements.txt**

```
Flask
Flask-Caching
requests
beautifulsoup4
icalendar
```

**README.md**

# Flask iCalendar App

This Flask application serves an iCalendar string containing waste disposal dates for Aschach a.d. Steyr, Austria.

## Installation

1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python app.py
```

## Usage

The application serves the iCalendar string on the '/' route:
```
http://localhost:5000/
```


## Production

copy initscript to `/etc/init.d/gunicorn.sh`

`sudo chmod +x /etc/init.d/gunicorn.sh`

`sudo service gunicorn start
sudo service gunicorn stop
sudo service gunicorn reload`

## Cache

The iCalendar string is cached in an in-memory cache for 2 hours. This means that the iCalendar string will only be generated from scratch every 2 hours, reducing the load on the server and improving performance.

## Contributing

Please feel free to contribute to this project by submitting pull requests.
