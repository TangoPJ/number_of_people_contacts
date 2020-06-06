import json
from collections import Counter
import datetime


def read_data_from_file(file):
    """This function reads data from JSON file

    :param file: contains the absolute path to the JSON file
    :return: The json object. A JSON object contains data in the form of key/value pair.
    The keys are strings and the values are the JSON types

    """

    with open(file, encoding='utf8') as f:
        contacts = json.load(f)
    return contacts


def is_valid_contact(s_to, s_from):
    """This function checks the time difference of 5 minutes or more

    :param s_to: Initial contact time
    :param s_from: Finish contact time
    :return: boolean value True or False

    """

    time_date_to = datetime.datetime.strptime(s_to, "%d.%m.%Y %H:%M:%S")
    time_date_from = datetime.datetime.strptime(s_from, "%d.%m.%Y %H:%M:%S")

    return time_date_to - time_date_from >= datetime.timedelta(minutes=5)


# counting persons
def counting_persons(data):
    """This function counts the number of contacts of each person

    :param data: data of people in JSON format
    :return: dictionary of people, key(str)=ID, value(int)=Number of contacts

    """

    general_number = Counter(v['Member1_ID'] for v in data if is_valid_contact(v["To"], v["From"])) \
                     + Counter(v['Member2_ID'] for v in data if is_valid_contact(v["To"], v["From"]))
    return dict(sorted(general_number.items(), key=lambda x: x[1], reverse=True))


def main():
    contacts_data = 'small_data_contacts.json'

    contacts = read_data_from_file(contacts_data)
    print(counting_persons(contacts))


if __name__ == '__main__':
    main()
