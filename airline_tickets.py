'''Skeleton app for airline ticket REST API

To set up the development environment:

    - Put this file wherever you want.  (It shouldn't be in the
      same directory as the virtualenv you will be creating in just
      a moment.)

    - Install pip (if needed); see http://pip.readthedocs.org/en/latest/installing.html

    - Install virtualenv (if needed):
      % pip install virtualenv

    - Create a virtualenv for this project and activate it:
      % mkdir ~/virtualenvs
      % virtualenv ~/virtualenvs/mobius_project
      % . ~/virtualenvs/mobius_project/bin/activate

    - Install Flask:
      % pip install flask

    - Run this app:
      % python airline_tickets.py

    You can now access the REST API at http://localhost:5000.  Changes made to this
    file while the Flask server is running are not automatically picked up, so you'll
    have to kill and restart the process (^C in the terminal will work).
'''

import random, json, copy
from datetime import datetime
from flask import Flask, jsonify, redirect, request, url_for
from flaskext.genshi import Genshi, render_response, render_template

app = Flask(__name__)
genshi = Genshi(app)

app.debug = True

flight_data = json.load(open('flights.json'))

@app.route('/', methods=['GET'])
def root():
    '''Gets to homepage'''
    flights = flight_data['flights']
    return render_response('index.html', dict(flights = flights, format_date = format_date, format_money = format_money))

@app.route('/flights', methods=['GET'])
def flights():
    '''Displays flight data'''
    return jsonify(flight_data)

@app.route('/mynameis/<userid>', methods=['POST'])
def mynameis(userid):
    '''POST and named param in route example'''
    return jsonify({
        'name': request.form.get('name', 'No name given'),
        'userid': userid,
    })

@app.route('/flight/book', methods=['POST'])
def book():
    confirmation = {'first_name' : request.form['first_name'],
                    'last_name' :  request.form['last_name'],
                    'bags' : request.form['bags'],
                    'flight_number' : request.form['flight_number']}
    booking_status = confirmBooking(request.form['flight_number'])
    if booking_status:
        booked_flight = find_flight_by_number(request.form['flight_number'])
        booked_flight['arrives']['when'] = format_date(booked_flight['arrives']['when'])
        booked_flight['departs']['when'] = format_date(booked_flight['departs']['when'])
        booked_flight['cost'] = format_money(booked_flight['cost'])
        return render_template('success.html', dict(confirmation = confirmation, code = booking_status, flight = booked_flight), method=None)
    else:
        return render_template('failure.html')

# For your convenience
def confirmBooking(_flight_num):
    '''Attempt to confirm a booking.

        :param _flight_num: Flight number that the customer is attempting to book.  This is not actually used.
        :type _flight_num: str
        :returns: Either a confirmation code (6 character string) or None if the flight is full.
        :rtype: str | None
    '''
    if random.random() < 0.5:
        # Flight is available, return confirmation code.
        return ''.join(random.choice('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(6))
    else:
        # Flight is unavailable.
        return None

def find_flight_by_number(flight_number):
    '''Takes a flight number as input and returns a copy of the full flight dictionary object'''
    for flight in flight_data['flights']:
        if flight['number'] == flight_number:
            return copy.deepcopy(flight)

def format_date(utc_string):
    '''Changes utc string to a more readable format, returns as a string'''
    date = datetime.strptime(utc_string, "%Y-%m-%dT%H:%M:%S" )
    return date.strftime("%a %B%e, %Y - %r")

def format_money(raw):
    raw = int(raw * 100)
    dollars = raw / 100
    cents = raw % 100
    formatted = "${dollars}.{cents}".format(dollars=dollars, cents=cents)
    if cents < 10:
        formatted += "0"
    return formatted

if __name__ == '__main__':
    # Listens on http://localhost:5000
    app.run()
