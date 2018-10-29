import requests
import json

# Python interface for the AGU API
class AguApi:

    # Current token
    _token = ''

    # AGU API URL
    _api_url = 'https://api.developer.agu.org:8443/api/{}'

    # Nothing happens here
    def __init__(self):
        pass

    # Return the program ids given the year
    def programsIds(self, year=2016):

        # Update this dictionary with new meetings id
        id_map = {2014: 8, 2015: 9, 2016: 10, 2017: 11}

        if year in id_map:
            data = self._loadAll('meetings')
            meeting_id = id_map[year]
            for c in data:
                if c['id'] == meeting_id:
                    return c['programs']

        print('ERROR: {} programs not found.'.format(year))
        return None

    # Return the programs given the year
    def programs(self, year=2016):

        program_ids = set(self.programsIds(year))

        return self._loadAll('programs', lambda c: c['programId'] in program_ids)

    # Return the sessions given the year and programId
    # If programId is null, return all the sessions of the year
    def sessions(self, year=2016, programId=None):

        if programId == None:
            programs_ids = set(self.programsIds(year))
        else:
            programs_ids = {programId}

        return self._loadAll('sessions', lambda c: c['programId'] in programs_ids)

    # Return the session ids given the year and programId
    # If programId is null, return all the session ids of the year
    def _sessionsIds(self, year=2016, programId=None):
        return [s['sessionId'] for s in self.sessions(year, programId)]

    # Return the abstracts given the year and programId
    # If programId is null, return all the abstracts of the year
    def abstracts(self, year=2016, programId=None):

        sessions_ids = set(self._sessionsIds(year, programId))

        return self._loadAll('abstracts', lambda c: c['sessionId'] in sessions_ids)

    # Return the authors given the year and programId
    # If programId is null, return all the authors of the year
    def authors(self, year=2016, programId=None):

        abstracts_data = self.abstracts(year, programId)

        # ids of people that presented something in this year
        person_ids = set()
        for abstract in abstracts_data:
            for person in abstract['abstractRoles']:
                person_ids.add(person['authorId'])

        return self._loadAll('people', lambda c: c['personId'] in person_ids)

    # Load all data from the api
    # value = data to be loaded (abstracts, sessions, etc.)
    # filt  = function used to filter data
    # debug = if True, print some information
    def _loadAll(self, value, filt=lambda c: True, debug=False):

        result = []
        done = False
        page = 0
        size = 1000
        if debug:
            print('Load {}...'.format(value))

        while not done:
            # If it is in the cache, use it
            cache_file = 'cache/{}_{}_{}.json'.format(value, size, page)
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                if 'content' not in data:
                    raise Exception('Cache is corrupted')
            except:
                data = self._apiRequest(value, {'page': page, 'size': size})
                # Store the result in the cache
                with open(cache_file, 'w') as f:
                    json.dump(data, f)

            result.extend(c for c in data['content'] if filt(c))
            if debug:
                print('Loaded page {} of {}'.format(page+1, data['totalPages']))

            page += 1
            if page == data['totalPages']:
                done = True

        if debug:
            print('DONE!')

        return result

    # Build header for the API request
    def _buildHeaders(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': self._token
        }
        return headers

    # Api GET request
    # value = data to be loaded (abstracts, sessions, etc.)
    # param = dictionary containing the parameters for the GET request
    def _apiRequest(self, value, param={}):

        # build parameters string
        p = ''
        if param:
            p = '?' + '&'.join('{}={}'.format(k, param[k]) for k in param)

        message_received = False
        while not message_received:
            print('Get {}'.format(self._api_url.format(value) + p))

            r = requests.get(self._api_url.format(value) + p,
                         headers = self._buildHeaders())

            if r.status_code == 200:
                message_received = True
            else:
                # If not succed, try to get a valid token (it expires after 1 hour)
                print('ERROR: status code of {} is {}.'.format(self._api_url.format(value), r.status_code))
                self._token = input('Insert a valid token: ')

        return r.json()


if __name__ == '__main__':
    # Usage example
    api = AguApi()

    pIds = api.programsIds()

    for p in pIds:
        print(p,len(api.abstracts(2016, p)))
