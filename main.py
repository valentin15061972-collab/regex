import re
import csv


with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

processed_contacts = []
header = contacts_list[0]
for contact in contacts_list[1:]:
    name_parts = ' '.join(contact[:3]).split()
    full_contact = name_parts + contact[3:]
    while len(full_contact) < len(header):
        full_contact.append('')
    processed_contacts.append(full_contact)
new_contacts_list = [header] + processed_contacts


phone_pattern = (r"(\+7|8)?\s*(\(?\d{3}\)?)?[\s\-]?(\d{3})[\s\-]?"
                 r"(\d{2})[\s\-]?(\d{2,4})(?:\s*(\(?доб\.?)\s*(\d+))?\)?")
phone_replace = lambda x: (f"+7({x.group(2).strip('()')}){x.group(3)}-{x.group(4)}-{x.group(5)} "
                           f"доб. {x.group(7)}") if x.group(7) else \
                           f"+7({x.group(2).strip('()')}){x.group(3)}-{x.group(4)}-{x.group(5)}"

for contact in processed_contacts:
    for i, field in enumerate(contact):
        if isinstance(field, str):
            contact[i] = re.sub(phone_pattern, phone_replace, field)


merged_contacts = {}
for contact in processed_contacts:
    lastname, firstname = contact[0], contact[1]
    key = (lastname, firstname)

    if key not in merged_contacts:
        merged_contacts[key] = contact[:]
    else:
        existing = merged_contacts[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

final_contacts = [header] + list(merged_contacts.values())


with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',', lineterminator='\n')
    datawriter.writerows(final_contacts)
