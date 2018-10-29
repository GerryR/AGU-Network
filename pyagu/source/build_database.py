from agu_api import AguApi
import string
import math
import json

# Export path
# out_path = 'database/'
out_path = '../../app/private/'

# Export only if flag is true
exp_abstracts = True
exp_programs = True
exp_sessions = True

years = [2017] # [2014, 2015, 2016]

# these programs do not contain abstracts
# exclude_program_ids = [92, 100, 113] # for 2016
exclude_program_ids = [307, 308, 315, 316, 335, 336] # for 2017

# in 2017 data the list of authors is inverted
# set this variable to -1 if you want to reverse the list
#                   to +1 if you want to keep the order
authors_order = -1

# get an instance of the API
api = AguApi()

# Export abracts
if exp_abstracts:
    data = []

    for year in years:

        authors = api.authors(year)

        # build authors dictionary
        authors_dict = {}
        for author in authors:
            authors_dict[author['personId']] = author

        abstracts = api.abstracts(year)
        export_keys = {'abstractId', 'text', 'title', 'sessionId', 'roomId'}
        for abstract in abstracts:
            abstract_doc = {k:v for k,v in abstract.items() if k in export_keys}
            # Add authors
            people = []
            for person in abstract['abstractRoles'][::authors_order]:
                p_id = person['authorId']
                person_data = {}
                person_data['firstName']  = authors_dict[p_id]['firstName']
                person_data['middleName'] = authors_dict[p_id]['middleName']
                person_data['lastName']   = authors_dict[p_id]['lastName']
                person_data['presenter']  = person['presenter']

                people.append(person_data)

            abstract_doc['authors'] = people
            data.append(abstract_doc)

    out_file = out_path + 'abstracts-DB.json'
    print("EXPORT {} ABSTRACTS TO {}".format(len(data), out_file))
    with open(out_file, 'w') as f:
        json.dump(data, f)

# Export programs
if exp_programs:

    data = []
    for year in years:
        programs = api.programs(year)
        export_keys = {'programId', 'title'}

        for program in programs:

            if program['programId'] in exclude_program_ids:
                continue

            program_doc = {k:v for k,v in program.items() if k in export_keys}
            program_doc['year'] = year
            data.append(program_doc)

    out_file = out_path + 'programs-DB.json'
    print("EXPORT {} PROGRAMS TO {}".format(len(data), out_file))
    with open(out_file, 'w') as f:
        json.dump(data, f)

# Export sessions
if exp_sessions:
    data = []
    for year in years:
        sessions = api.sessions(year)
        export_keys = {'sessionId', 'title', 'finalSessionNumber', 'programId', 'sessionRoles', 'roomId'}
        for session in sessions:
            data.append({k:v for k,v in session.items() if k in export_keys})

    out_file = out_path + 'sessions-DB.json'
    print("EXPORT {} SESSIONS TO {}".format(len(data), out_file))
    with open(out_file, 'w') as f:
        json.dump(data, f)
