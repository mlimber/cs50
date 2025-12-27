from collections import namedtuple
import pytest
import degrees as deg

TH = "Tom Hanks"
TC = "Tom Cruise"
VG = "Valeria Golino"
KB = "Kevin Bacon"
EW = "Emma Watson"
CE = "Cary Elwes"

MOVIE = 0
PERSON = 1


@pytest.fixture
def small():
    deg.load_data('small')
    ew = deg.person_id_for_name(EW)
    tc = deg.person_id_for_name(TC)
    th = deg.person_id_for_name(TH)
    vg = deg.person_id_for_name(VG)
    kb = deg.person_id_for_name(KB)
    ce = deg.person_id_for_name(CE)
    assert ew and tc and th and vg and kb and ce

    SmallData = namedtuple('SmallData', ['ew', 'tc', 'th', 'vg', 'kb', 'ce'])
    return SmallData(ew=ew, tc=tc, th=th, vg=vg, kb=kb, ce=ce)


def test_emma(small):
    for other in [small.tc, small.th, small.vg, small.kb, small.ce]:
        assert deg.shortest_path(small.ew, other) is None
        assert deg.shortest_path(other, small.ew) is None


def test_self(small):
    for person in [small.ew, small.tc, small.th, small.vg, small.kb, small.ce]:
        assert 0 == len(deg.shortest_path(person, person))


def test_cruise_to_hanks(small):
    path = deg.shortest_path(small.tc, small.th)

    assert len(path) == 2

    assert deg.movies[path[0][MOVIE]]["title"] == "A Few Good Men"
    assert deg.people[path[0][PERSON]]["name"] == KB

    assert deg.movies[path[1][MOVIE]]["title"] == "Apollo 13"
    assert deg.people[path[1][PERSON]]["name"] == TH


def test_golino_to_elwes(small):
    path = deg.shortest_path(small.vg, small.ce)

    assert len(path) == 5


def test_hanks_to_bacon(small):
    path = deg.shortest_path(small.th, small.kb)

    assert len(path) == 1

    assert deg.movies[path[0][MOVIE]]["title"] == "Apollo 13"
    assert deg.people[path[0][PERSON]]["name"] == KB
