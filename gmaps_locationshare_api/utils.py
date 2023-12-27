import json
from gmaps_locationshare_api.types import Person, Location


def _parse_raw_data(data: str) -> list[Person]:
    '''
    Parses raw RPC response from Google's location sharing API.
    people_array = data[0] contains info on all people
    people_info = people_array[n]

    person_info = people_info[0] contains detailed info on person
    numeric_id? = person_info[0]
    profile_pic_url = person_info[1]
    full_name = person_info[3]
    alphanumeric_id? = person_info[7]

    location_info = people_info[1] contains detailed location info on person

    long_lat = location_info[1] contains long and lat of location
    long = long_lat[1]
    lat = long_lat[2]

    numeric_id? = location_info[2] dunno what this is
    random_number = location_info[3] dunno what this is
    address = location_info[4] String address of current location
    country_code = location_info[6]
    random_number2 = location_info[7] dunno what this is
    random_number3 = location_info[8] dunno what this is

    random_number = people_info[2] dunno what this is
    alphanumeric_id? = people_info[4]

    person_info2 = people_info[6] Less detailed info on person
    numeric_id? = person_info2[0] Same as numeric id in detailed person info
    profile_pic_url = person_info2[1] same profile pic url
    full_name = person_info2[2]
    short_name = person_info2[3] Either first name or nickname

    random_number2 = people_info[7] dunno what this is

    battery_info = people_info[13] Battery info
    random_number = battery_info[0] dunno what this is
    battery_percent = battery_info[1] (Can sometimes not show up, check array length to be sure)

    random_number3 = people_info[14] dunno what this is
    people_info[16, 17, 18] are arrays containing 1 or no numbers. No idea, last array (ind 18) seems to be empty always
    '''
    json_data = json.loads(data[4:])
    return list(map(lambda x: Person(
        id=x[0][0],
        profile_pic_url=x[0][1],
        fullname=x[0][3],
        nickname=x[6][3],
        battery=int(x[13][1]) if len(x[13]) == 2 else -1,
        location=Location(
            longitude=float(x[1][1][1]),
            latitude=float(x[1][1][2]),
            address=x[1][4]
        )
    ), json_data[0]))

