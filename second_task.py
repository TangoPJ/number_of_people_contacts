import json
from collections import Counter
import datetime
import pandas as pd


def read_json(path):
    """Loads JSON from a fileclear

   :param path: absolute path to a JSON file
   :return: data, containing JSON data
    """

    with open(path, encoding='utf8') as f:
        contacts = json.load(f)
    return contacts


def is_valid_contact(s_to, s_from):
    """Checks the time difference of 5 minutes or more

    :param s_to: Initial contact time
    :param s_from: Finish contact time
    :return: boolean value True or False

    """

    time_date_to = datetime.datetime.strptime(s_to, "%d.%m.%Y %H:%M:%S")
    time_date_from = datetime.datetime.strptime(s_from, "%d.%m.%Y %H:%M:%S")

    return time_date_to - time_date_from >= datetime.timedelta(minutes=5)


# counting persons
def count_persons(data):
    """Counts the number of contacts of each person

    :param data: data of people in JSON format
    :return: dictionary of people, key(str)=ID, value(int)=Number of contacts

    """

    general_number = Counter(v['Member1_ID'] for v in data if is_valid_contact(v["To"], v["From"])) \
                     + Counter(v['Member2_ID'] for v in data if is_valid_contact(v["To"], v["From"]))
    return dict(sorted(general_number.items(), key=lambda x: x[1], reverse=True))


def search_persons(per, ids):
    """ Searches persons by ID from small_data_persons.json

    :param per data of persons
    :param ids: data of IDs
    :return: list of dicts
    """

    output = []
    for key, value in ids.items():
        for i in per:
            if key == i['ID']:
                output.append({"Name": i["Name"], "ID": key, "Number of contacts": value})

    return list(sorted(output, key=lambda x: x["Number of contacts"], reverse=True))

def write__to_excel(data, file):
    df = pd.DataFrame.from_dict(data)
    df.to_excel(file)


def main():
    contacts_data = 'small_data_contacts.json'
    persons_data = 'small_data_persons.json'
    result = 'result.xlsx'

    contacts = read_json(contacts_data)
    persons = read_json(persons_data)

    write__to_excel(search_persons(persons, count_persons(contacts)), result)


if __name__ == '__main__':
    main()
