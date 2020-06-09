import second_task
import datetime
from collections import defaultdict


def count_time(data):
    """Counts total time for each person

    :param data: data of people in JSON format
    :return: dict of IDs persons
    """

    for i in data:
        time_date_to = datetime.datetime.strptime(i["To"], "%d.%m.%Y %H:%M:%S")
        time_date_from = datetime.datetime.strptime(i["From"], "%d.%m.%Y %H:%M:%S")
        total_time = time_date_to - time_date_from

        i["Total_time"] = int(total_time.seconds / 60)

    result = defaultdict(int)

    for value in data:
        result[value['Member1_ID']] += value['Total_time']

    return dict(result)


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
                output.append({"Name": i["Name"], "ID": key, "Total_time": value})

    return list(sorted(output, key=lambda x: x["Total_time"], reverse=True))


def main():
    contacts_file = 'small_data_contacts.json'
    persons_file = 'small_data_persons.json'
    file = 'output.xlsx'

    contacts = second_task.read_json(contacts_file)
    persons = second_task.read_json(persons_file)

    count_time(contacts)
    wf = search_persons(persons, count_time(contacts))

    second_task.write__to_excel(wf, file)


if __name__ == '__main__':
    main()
