#parser for calendar
import pprint
from datetime import datetime, date, time
import time

#Global pprint object 
pp = pprint.PrettyPrinter(indent=4)

def parse_schedule():
    """
    Turn a schedule in the form of 
    ----------------
    #Date
    ##Event Name
    *Location: ...
    *Time: ...
    *Materials: ...
    *Summary: ...
    ---------------
    Into a dictionary mapping date to list of events for that day 
    {date: 
        [ [event, 
                {
                    location:...,
                    time:...,
                    materials:...,
                    summary:... 
                }
          ]
        ] 
    }
    """

    date_event = {}
    line_number = 0
    with open("FILLMEIN.txt") as f:
        current_date = ""
        current_event = ""
        current_heading = ""
        for line in f:
            line_number += 1
            #hack to skip the first line which is a key error
            if line.rstrip() == "" or line_number == 1:
                continue
            #Heading Logic
            if line[0] == "#":
                #Date heading 
                if line[1] == "#":
                    #remove the two hashes, strip /r/n, remove colon
                    current_date = line[2::].rstrip()[:-1]
                    date_event[current_date] = {}
                #Event heading
                else:
                    current_event = line[1::].rstrip() 
                    date_event[current_date][current_event] = {}
            #Event information
            else:
                #strip Location: and Time: to their information
                if "Location:" in line:
                    location = line[get_last_pos(line, "Location:")::].rstrip()
                    date_event[current_date][current_event]["location"] = \
                        location
                    current_heading = "location"
                elif "Time:" in line:
                    time_p = line[get_last_pos(line, "Time:")::].rstrip()
                    date_event[current_date][current_event]["time"] = \
                        start_end_datetime(time_p, current_date)
                    current_heading = "time"
                #Leave "Materials:" and "Summary:" because both will be
                #combined in the calendar notes
                elif "Materials:" in line:
                    materials = line[line.index("Materials:")::].rstrip()
                    date_event[current_date][current_event]["materials"] = \
                        materials
                    current_heading = "materials"
                elif "Summary:" in line:
                    summary = line[line.index("Summary:")::].rstrip()
                    date_event[current_date][current_event]["summary"] = \
                        summary
                    current_heading = "summary"
                #parse the multiline comments that come from bulleted lists
                #in the materials
                else:
                    if current_heading == "location" or \
                        current_heading == "time":
                        print "Location and Time format error"
                        print line.rstrip(), line_number
                    else:
                        try: 
                            date_event[current_date][current_event]\
                            [current_heading] += line.rstrip()
                        except KeyError:
                            print "KeyError"
                            print line.rstrip(), line_number
    return date_event

def get_last_pos(line, string):
    """
    Given an input string, find the location of the last character
    plus a space. get_last_pos("This: is cool", "This:") returns 6
    """
    return line.index(string) + len(string) + 1

def start_end_datetime(time_p, current_date):
    """
    Turn standard time_p format in to datetime formatted (start, end) tuples
    to be used in the google calendar input. Turn into rfc3339, which is a 
    gigantic huge pain  
    """
    ##Parse time_p
    #split into start, end
    start, end = time_p.split("-")
    start = "".join(start.split())
    end = "".join(end.split())

    #logic for handling missing pm and am
    if not "am" in start and not "pm" in start:
        if "am" in end:
            start += "am"
        elif "pm" in end:
            start += "pm"
        else:
            print "There is no am or pm in end time_p"
            print (start, end)

    #make sure everything has a start and end
    if not("am" in start or "pm" in start and \
        "am" in end or "pm" in end): 
        print "Error in time_p"
        print (start,end)

    ##Parse Date
    day, date = current_date.split(",")
    date = "".join(date.split()) + "/2014"
    

    
    start = datetime.strptime( start + date, "%I:%M%p%m/%d/%Y")
    end = datetime.strptime( end + date, "%I:%M%p%m/%d/%Y")

    return tuple(  map(lambda x: x.isoformat("T"), (start, end) )  )
