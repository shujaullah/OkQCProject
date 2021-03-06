#!/usr/bin/env python3

"""lib file for commands"""
"""Process the text that is returned by Google Assistant"""
import re
import db_query

# Main for testing purposes
def main():
    print(get_daytime("Introduction To Programming"))

def lookup_prof_class(vtext):
    """
    Get classname from query before looking up professor
    Pre: Voice text from user passed to this function
    Post: Returns classname from text, assuming valid class
    """
    #classname = re.sub(r'^.*teaching ', "", vtext)
    classnameresult = re.match('who is teaching (.*)', vtext)
    print('lookup_prof_class:', classnameresult.group(1))
    return(classnameresult.group(1))

def lookup_prof(classname):
    """
    Get professor names for the class being taught
    Pre: This function gets a valid class
    Post: Returns a tuple that contains information
    """
    print('lookup_prof:')
    return(db_query.search(classname, "LAST"))

def get_classnum_class(vtext):
    """
    Get classname from query before looking up class id/course #
    Pre: Voice text from user passed to this function
    Post: Returns classname from text, assuming valid class
    """
    #classname = re.sub(r'^.*course number for ', "", vtext)
    classnameresult = re.match('(.*) course number for (.*)', vtext)
    print('get_classnum_class:', classnameresult.group(2))
    #return(classname)
    return(classnameresult.group(2))

def get_classnuminfo(classinfo, numresult):
    """
    Get classnum/course # info based on classname
    Pre: Assumes valid classname passed to this function
    Post: Returns course # info according to valid classname
    """
    #classes are always in this format CSI 116 01
    # 1 -> course type designation ex: CSI
    # 2 -> course number ex: 116
    # 3 -> section number ex: 01
    classnumresult = re.match(r"(\D{3})  (\d{3})  ([F0-9][0-9])", classinfo.upper())
    print('get_classnuminfo:', classnumresult.group(numresult))
    return(classnumresult.group(numresult))

def get_classnum(classname):
    """
    Get class number associated with the classname
    Pre: Assume a valid classname is passed to the function
    Post: Returns result based on the classname
    """
    print('get_classnum:')
    return(db_query.search(classname, "CODE"))

def remove_classsectnum(classnum):
    """
    # Removes class section number associated with the class
    Pre: Assumes a valid course # (that should include section #) is provided
    Post: Returns course # with the section # removed
    """
    #classnumresult = re.match(r"([A-Z][A-Z][A-Z])  ([0-9][0-9][0-9])  ([F0-9][0-9])", classnum.upper())
    #return(classnumresult.group(1) + ' ' + classnumresult.group(2))
    print('remove_classsectnum:', get_classnuminfo(classnum, 1), get_classnuminfo(classnum, 2))
    return(get_classnuminfo(classnum, 1) + ' ' + get_classnuminfo(classnum, 2))

def get_roomnum_class(vtext):
    """
    Get class name before getting room number
    Pre: Assumes good voice text input
    Post: Returns classname
    """
    #classname_result = re.match(r'Where is (.*) section ([F0-9][0-9]) being taught?', vtext)
    classname_result = re.match(r'where is (.*) being', vtext)
    #print(classname_result.group(1))
    print('get_roomnumclass:', classname_result.group(1))
    return(classname_result.group(1))

def get_roomnum(classname):
    """
    Get room number based on classname
    Pre: Assumes valid classname
    Post: Returns room # info
    """
    #classname_result = re.match(r'Where is (.*) section ([F0-9][0-9]) being taught?', classname)
    print('get_roomnum:')    
    return(db_query.search(classname, "ROOM"))

def fix_roomnumtext(roomnum):
    """
    Fix room number for text-to-voice converter
    Pre: Assumes valid course num
    Post: Returns complete room info (text replacement)
    """
    upperroomnum = roomnum.upper()
    print('fix_roomnumtext:')
    PPlace = 'PP'
    PPlaceVal = "President\'s Place"
    Sav = 'S'
    SavVal = 'Saville Hall'
    newroomnum = ''
    for somechar in upperroomnum:
        if somechar.isdigit():
            newroomnum = newroomnum + ' ' + somechar
        else:
            newroomnum = newroomnum + somechar
            
    if PPlace in upperroomnum:
        #roomnumresult = re.match(r"[P][P][0-9][0-9][0-9]", roomnum)
        newroomnum = re.sub(PPlace, PPlaceVal, newroomnum)
        return(newroomnum)
    elif Sav in upperroomnum:
        newroomnum = re.sub(Sav, SavVal, newroomnum)
        return(newroomnum)
    else:
        print("Not a valid room")

def report_time(atime):
    """
    Converts internal time convention (on the Excel Spreadsheet) into AM/PM
    Pre: Assumes data is from spreadsheet in military time format HH:MM
    Post: Returns time in "verbally useful" format - ex: 9 25 AM
    """
    reached_colon = False
    hour_digit = ''
    minute_digit = ''
    ampm = ''
    cur_time = ''
    for cur_string in atime:
        cur_time = cur_string
        
    #for curdigit in atime:
        #print(curdigit)
        #if (curdigit == ':'):
            #reached_colon = True
        #elif (reached_colon == True):
            #minute_digit = minute_digit + curdigit
        #else:
            #hour_digit = hour_digit + curdigit
    hour_digit = cur_time[0:2]
    minute_digit = cur_time[3:5]
    hour_digit = int(hour_digit)
    #minute_digit = int(minute_digit)
    if (hour_digit >= 12):
        ampm = 'PM'
        if (hour_digit != 12):
            hour_digit = hour_digit - 12
    else:
        ampm = 'AM'
        if (hour_digit == 0):
            hour_digit = hour_digit + 12
    return(str(hour_digit) + ' ' + minute_digit + ' ' + ampm)

def report_days(aday):
    """
    Converts internal day convention into actual days of week
    Pre: Assumes data is from spreadsheet based on QC abbreviated day format
    MTWRFSU = Monday, Tuesday, Wednesday, Thursday, Friday,
    Saturday, Sunday (respectively)
    Post: Returns appropriate days based on listed letters
    """
    print("report_days: ", aday)
    
    daysofweek = ''
    for day in aday:
        if 'M' in day:
            daysofweek = daysofweek + "Monday" + ' '
        if 'T' in day:
            daysofweek = daysofweek + "Tuesday" + ' '
        if 'W' in day:
            daysofweek = daysofweek + "Wednesday" + ' '
        if 'R' in day:
            daysofweek = daysofweek + "Thursday" + ' '
        if 'F' in day:
            daysofweek = daysofweek + "Friday" + ' '
        if 'S' in day:
            daysofweek = daysofweek + "Saturday" + ' '
        if 'U' in day:
            daysofweek = daysofweek + "Sunday" + ' '
    return(daysofweek)

def strip_section(asection):
    """
    Get section numbers from course
    Pre: Assumes data is class info (section is embedded)
    expected format: CSI  116  01
    Post: Returns strictly section number
    """
    print("strip_section: ", asection)
    for data in asection:
        print(data[10:])
        return(data[10:])

def report_section(asection):
    """
    Report usable data from section number
    Pre: Assumes data is stripped out from class info
    expected variations: 01, F1, F1 S, F5 3, F7 2
    Post: Returns verbal friendly information
    """
    section_text = ''
    print("report_section: ", asection)
    if 'F' in asection:
        if (asection[1] == '1'):
            section_text = "Section " + asection + " 10 Week Class"
        elif (asection[1] == '5'):
            section_text = "Section " + asection + " 5 Week Class"
        elif (asection[1] == '7'):
            section_text = "Section " + asection + " 7 Week Class"
    else:
        section_text = "Section"
        count = 0
        for some_section in asection:
            section_text = section_text + ' ' + some_section
            count = count + 1
            if count == 2:
                break
    return(section_text)

def get_daytime_class(vtext):
    """
    Get class name before getting day+time of class
    Pre: Assumes good voice text input
    Post: Returns classname
    """
    classnameresult = re.match(r'when is (.*) being run', vtext)
    print('get_daytime_class:', classnameresult.group(1))
    return(classnameresult.group(1))

def get_daytime(classname):
    """
    Get days and times based on class
    Pre: Assumes valid classname
    Post: Returns list of tuples containing class day and times
    """
    print('get_daytime:')
#may want a customized function for obvious reasons
    section_tuple = db_query.search(classname, "CODE")
    dayofweek_tuple = db_query.search(classname, "DAY")
    begintime_tuple = db_query.search(classname, "BEG2")
    endtime_tuple = db_query.search(classname, "ND3")
    total_len = len(dayofweek_tuple)
    
    daytime_tuple = ()
    
    for x in range(total_len):
        new_daytime_tuple = (report_section(strip_section(section_tuple[x])), report_days(dayofweek_tuple[x]), report_time(begintime_tuple[x]), report_time(endtime_tuple[x]))
        daytime_tuple = daytime_tuple + new_daytime_tuple

    return(daytime_tuple)

if __name__ == '__main__':
    main()
