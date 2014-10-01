import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from apiclient import errors

import calparse
import sys

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
    client_id='FILLMEIN',
    client_secret='FILLMEIN',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='calendar-add/0.1')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='FILLMEIN')

def main():
  date_time = calparse.parse_schedule()
  calendar_events = build_calendar_events(date_time)
  count = 0
  for event in calendar_events:
    print event
    count += 1
    print count
    try:
      # The Calendar API's events().list method returns paginated results, so we
      # have to execute the request in a paging loop. First, build the
      # request object. The arguments provided are:
      #   primary calendar for user
      # request = service.events().list(calendarId='primary')
      # # Loop until all pages have been processed.
      # while request != None:
      #   # Get the next page.
      #   response = request.execute()
      #   # Accessing the response like a dict object with an 'items' key
      #   # returns a list of item objects (events).
      #   for event in response.get('items', []):
      #     # The event object is a dict object with a 'summary' key.
      #     print repr(event.get('summary', 'NO SUMMARY')) + '\n'
      #   # Get the next request object by passing the previous request object to
      #   # the list_next method.
      #   request = service.events().list_next(request, response)
          created_event = service.events().insert(calendarId='76fiofd3fona8r59v4d3d9dk20@group.calendar.google.com', body=event).execute()
          print created_event['id']

    except ValueError:
      # The AccessTokenRefreshError exception is raised if the credentials
      # have been revoked by the user or they have expired.
      # Could not load Json body.
      
      print 'HTTP Status code: %d' % e.resp.status
      print 'HTTP Reason: %s' % e.resp.reason

def build_calendar_events(date_time): 
  event_list = []
  for date, events in date_time.items():
    for event, event_dict in events.items():
      material = ""
      summary = ""
      location = ""

      try:
        material = event_dict["materials"]
      except KeyError:
        pass
      try:
        summary = event_dict["summary"]
      except KeyError:
        pass
      try:
        location = event_dict["location"]
      except KeyError:
        pass
      

      add_event = {
        'summary': event,
        'location': location,
        'start': {
          'dateTime': event_dict["time"][0],
          'timeZone': "America/Chicago"
        },
        'end': {
          'dateTime': event_dict["time"][1],
          'timeZone': "America/Chicago"
        },
        'description': ""
      }
      event_list.append(add_event)
  return event_list


if __name__ == '__main__':
  main()
