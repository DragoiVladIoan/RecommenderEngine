import random
import time
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dateutil.relativedelta import relativedelta
from datetime import datetime

calendar_month_names = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12

}


class Location:
    def __init__(self, id, name, city, address, maximum_number_of_seats):
        self.id = id
        self.name = name
        self.city = city
        self.address = address
        self.maximum_number_of_seats = maximum_number_of_seats

    def to_dict(self):
        return {
            'LOCATION_ID': self.id,
            'NAME': self.name,
            'CITY': self.city,
            'ADDRESS': self.address,
            'MAXIMUM_NUMBER_OF_SEATS': self.maximum_number_of_seats

        }


class Event:
    def __init__(self, id, title, content, date_posted, organizer, event_date, location):
        self.id = id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.organizer = organizer
        self.approved = True
        self.event_date = event_date
        self.pending_approval = False
        self.location = location

    def to_dict(self):
        return {
            'EVENT_ID': self.id,
            'TITLE': self.title,
            'CONTENT': self.content,
            'DATE_POSTED': self.date_posted,
            'ORGANIZER': self.organizer,
            'APPROVED': self.approved,
            'EVENT_DATE': self.event_date,
            'PENDING_APPROVAL': self.pending_approval,
            'LOCATION': self.location
        }


def get_specific_tag_value(primary_tag, primary_class_tag, secondary_tag, secondary_tag_class):
    events = []
    for tag in soup.find_all(primary_tag, class_=primary_class_tag):
        try:
            value = tag.find(secondary_tag, class_=secondary_tag_class).getText().strip()
        except AttributeError:
            value = "No Details added"
        events.append(value)
    return events


def clean_date(date):
    dates = date.split(' ')
    dates[1] = calendar_month_names[dates[1]]
    return str(dates[0]) + '-' + str(dates[1]) + '-' + str(dates[2])


def some_weeks_later(date):
    target_time = datetime.strptime(date, '%d-%m-%Y')
    random_week = random.randint(1, 4)
    event_time = target_time + relativedelta(weeks=random_week)
    return event_time


url = 'https://eventslist.org/find-an-event.html'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome("/Users/vladdragoi/Downloads/chromedriver")
driver.get(url)
time.sleep(3)
page = driver.page_source
driver.quit()
soup = BeautifulSoup(page, 'html.parser')

event_title_list = get_specific_tag_value('div', 'col-lg-8 col-md-9', 'p', 'event-info')

event_content_list = get_specific_tag_value('div', 'col-lg-2 event-button-col', 'div', 'category-badge')

date_posted_list = get_specific_tag_value('div', 'd-none d-md-block col-lg-2 col-md-3', 'p', 'event-info date')

event_date_list = []
for i in range(0, len(date_posted_list)):
    date_posted_list[i] = clean_date(date_posted_list[i])
    event_date = some_weeks_later(date_posted_list[i])
    event_date_list.append(event_date)

locations_name = get_specific_tag_value('div', 'col-lg-4 col-md-4 ng-star-inserted', 'p', 'event-info')
cities_name = get_specific_tag_value('div', 'col-lg-4 col-md-4 ng-star-inserted', 'p', 'event-info')
addresses_name = get_specific_tag_value('div', 'ng-star-inserted', 'p', 'event-info-details')
maximum_number_of_seats = []
for i in range(0, len(locations_name)):
    seats = random.randint(100, 10000)
    maximum_number_of_seats.append(seats)

locations = []
for i in range(0, len(locations_name)):
    locations.append(Location(i, locations_name[i], cities_name[i], addresses_name[i], maximum_number_of_seats[i]))

events = []
for i in range(0, len(event_title_list)):
    events.append(Event(i, event_title_list[i], event_content_list[i], date_posted_list[i], 0, event_date_list[i], locations[i].id))


df_locations = pd.DataFrame.from_records([location.to_dict() for location in locations])
df_events = pd.DataFrame.from_records([event.to_dict() for event in events])

df_locations.to_csv('data/Locations.csv', index=False)
df_events.to_csv('data/Events.csv', index=False)

