#test/test_logic.py

from logic import check_lifecycle_status

def test_check_lifecycle_status_obsolete():
    """
    Docstring for test_check_lifecycle_status_obsolete
    IF a part description contains 'OBS', it should be flagged as obsolete
    """

    status, notes = check_lifecycle_status("X-99", "OBSOLETE VGA CHIP")
    assert status == "OBSOLETE"
    assert "Critical"in notes

def test_check_lifecycle_status_active():
    """
    Docstring for test_check_lifecycle_status_active
    Standard parts should be active
    """

    status, notes = check_lifecycle_status("NE555", "Timer IC")
    assert status == "Active"

    

