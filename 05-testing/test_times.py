import datetime
import times
import pytest
import yaml

# def test_given_input():
#     large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
#     short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
#     result = times.overlap_time(large, short)
#     expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
#     assert result == expected

# def test_class_time():
#     large = times.time_range("2019-10-31 10:00:00" , "2019-10-31 13:00:00")
#     short = times.time_range("2019-10-31 10:05:00", "2019-10-31 12:55:00", 3, 600)
#     # two breaks, therefore 3 blocks
#     result = times.overlap_time(large, short) 
#     assert result == short
#     # smaller time encompasses the bigger one (small time in a big time)
#     # expected results is the shorter time range

def test_20_min():
    large = times.time_range("2019-01-01 00:00:00", "2019-01-01 23:50:00", 24, 10 * 60)
    short = times.time_range("2019-01-01 00:30:00", "2019-01-01 23:55:00", 24, 35 * 60)
    result = times.overlap_time(large, short)
    assert all([(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S") -
    datetime.datetime.strptime(t0, "%Y-%m-%d %H:%M:%S")).total_seconds() == 20 * 60 for t0, t1 in result])

# def test_no_overlap():
#     large = times.time_range("2019-01-01 00:00:00", "2019-01-01 23:50:00")
#     short = times.time_range("2019-01-02 00:30:00", "2019-01-02 23:55:00")
#     result = times.overlap_time(large, short)
#     assert len(result) == 0

# def test_touching_edges():
#     large = times.time_range("2019-10-31 00:00:00", "2019-10-31 00:50:00", 3, 600)
#     short = times.time_range("2019-10-31 00:10:00", "2019-10-31 01:00:00", 3, 600)
#     result = times.overlap_time(large, short)
#     assert result == [] # I expect to get an empty list.



# Testing-08
# @pytest.mark.parametrize('test_input, expected', [
#     #(input ranges, expected ranges)
#     # given input
#     ([["2010-01-12 10:00:00", "2010-01-12 12:00:00"], ["2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60]], [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]),
#     # class time
#     ([["2019-10-31 10:00:00", "2019-10-31 13:00:00"], ["2019-10-31 10:05:00", "2019-10-31 12:55:00", 3, 600]], times.time_range("2019-10-31 10:05:00", "2019-10-31 12:55:00", 3, 600)),
#     # no overlap
#     ([["2019-01-01 00:00:00", "2019-01-01 23:50:00"], ["2019-01-02 00:30:00", "2019-01-02 23:55:00"]], []),
#     # touching edges
#     ([["2019-10-31 00:00:00", "2019-10-31 00:50:00", 3, 600], ["2019-10-31 00:10:00", "2019-10-31 01:00:00", 3, 600]], []),
# ])
# def test_many(test_input, expected):
#     large = times.time_range(*test_input[0])
#     short = times.time_range(*test_input[1])
#     result = times.overlap_time(large, short)
#     assert result == expected



# Testing-09
with open("05-testing/fixture.yaml", 'r') as yamlfile:
    fixture = yaml.safe_load(yamlfile)


@pytest.mark.parametrize('test_name', fixture) # fixture is a list of dictionaries [{'given':...}, {'class':...}, ]
def test_many(test_name):
    # test_name is a dictionary like: {'name': {'test_input':..., 'expected':...}
    properties = list(test_name.values())[0] # We know there's only one element inside 'name'
    # get the input and expected values for each test
    test_input = properties['test_input']
    expected = properties['expected']
    large = times.time_range(*test_input['interval_1'])
    short = times.time_range(*test_input['interval_2'])
    result = times.overlap_time(large, short)
    if isinstance(expected, list):
        # If expected is a list when we've writen the results on the yaml
        if expected:
            # If it's not an empty list we need to convert a list of lists into a list of tuples.
            expected = [(start, stop) for start, stop in expected]
        assert result == expected
    else:
        # If it's not a list, then `expected` is the name of one of the inputs
        assert result == times.time_range(*test_input[expected])




# Testing-10
def test_range_backwards():
    with pytest.raises(ValueError, match=r"Stopping date should happen after than starting date"):
        times.time_range("2019-10-31 00:00:00", "2019-10-30 00:50:00", 3, 600)




# Testing-12
from unittest import mock

class ISS_response:
    '''
    This class provides "hardcoded" return values to mock the calls to the online API.
    '''
    @property
    def status_code(self):
        return 200

    def json(self):
        '''
        mocks the bit from the json output we need from querying the API.
        '''
        now = datetime.datetime.now().timestamp()
        return {'message': 'success',
                'request': {'altitude': 10.0, 'datetime': now, 'latitude': 51.5074, 'longitude': -0.1278, 'passes': 5},
                'response': [{'duration': 446, 'risetime': now + 88433},
                             {'duration': 628, 'risetime': now + 94095},
                             {'duration': 656, 'risetime': now + 99871},
                             {'duration': 655, 'risetime': now + 105676},
                             {'duration': 632, 'risetime': now + 111480}]}

def test_iss_passes():
    with mock.patch("requests.get", new=mock.MagicMock(return_value=ISS_response())) as mymock:
        iss_seen = times.iss_passes(51.5074, -0.1278)
        mymock.assert_called_with("http://api.open-notify.org/iss-pass.json",
                                  params={
                                      "lat": 51.5074,
                                      "lon": -0.1278,
                                      "n": 5})
        assert len(iss_seen) == 5
        # Create a range from yesterday to next week whether the overlap ranges are still 5
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        next_week = datetime.datetime.now() + datetime.timedelta(days=7)
        large = times.time_range(f"{yesterday:%Y-%m-%d %H:%M:%S}", f"{next_week:%Y-%m-%d %H:%M:%S}")
        assert times.overlap_time(large, iss_seen) == iss_seen
