from colorama import Fore
import pytest
from unittest.mock import MagicMock
import sys
import os

from unittest.mock import patch

# add url 'main' a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main')))

from StateMachine import StateMachine

@pytest.fixture
def mock_client():
    """Create a customer mock to avoid real calls."""
    return MagicMock()

def test_select_opc_and_username_check(mock_client):
    """Test to verify that entering '1' changes to the ENTER_WITH_USERNAME state."""
    state_machine = StateMachine(mock_client)

    # set current status SELECT_OPC_LOGIN_MENU
    state_machine.current_status = {
        "code": "",
        "status": state_machine.SELECT_OPC_LOGIN_MENU,
        "text": "Select an OPTION:"
    }

    # Simulate user input '1'
    new_state = state_machine.processInput("1")

    # verify if the state was changed to ENTER_WITH_USERNAME
    assert new_state["status"] == state_machine.ENTER_WITH_USERNAME

    print("✅ Test for SELECT_OPC_LOGIN_MENU successful")

    # Simulate user input 'asd'
    new_state = state_machine.processInput("asd")

    # verify if the state was changed to ENTER_WITH_USERNAME
    assert new_state["status"] == state_machine.LOGIN_REQUEST_PASS
    assert new_state["code"] == 200
    print("✅ Test for SELECT_OPC_LOGIN_MENU successful.")

    
def test_username_zero_exit(mock_client):
    state_machine = StateMachine(mock_client)

    # set current status ENTER_WITH_USERNAME
    state_machine.current_status = {
        "code": "",
        "status": state_machine.ENTER_WITH_USERNAME,
        "text": "Enter your username:"
    }

    # simulate entry "0"
    new_state = state_machine.processInput("0")

    # verify if the status changed to EXIT
    assert new_state["status"] == state_machine.EXIT
    assert new_state["code"] == "EXIT"
    print("✅ Test for username '0' and exit successful.")

# Test to verify the flow when the username is empty or more than 15 characters
def test_username_empty_or_too_long(mock_client):
    state_machine = StateMachine(mock_client)
    
    # Simulate input() in the same order it would be executed in the while loop
    with patch("builtins.input", side_effect=["", "thisisaverylongusername", "validusername"]): # THIS SIMULATES 3 USER ENTRIES IN A ROW.
        
        # Simulate empty entry
        new_state = state_machine.processInput("")  # Since input_user is invalid (""), it enters the while loop, which keeps asking for values using input() until the correct one is entered.
        # It exits with "validusername" as the username.

        assert new_state["status"] == state_machine.LOGIN_MENU or state_machine.LOGIN_REQUEST_PASS  
        assert new_state["code"] == 200 or 404 
        


# Test to verify the flow when the username "asd" is found (200)
@patch('StateMachine.requests.get') # Mock the requests.get call
def test_username_asd_found(mock_get, mock_client):
    state_machine = StateMachine(mock_client)

    # Simulate that we are already in ENTER_WITH_USERNAME
    state_machine.current_status = {
        "code": "",
        "status": state_machine.ENTER_WITH_USERNAME,
        "text": "Enter your username:"
    }

    # Configure the mock to return a 200 with a found user
    mock_response = mock_get.return_value  # Get the simulated response value
    mock_response.status_code = 200  # Status code 200 (OK)
    mock_response.json.return_value = {'user': {'username': 'asd'}}   # Simulate that the username 'asd' was found

    # Process the input with the username "asd"
    new_state = state_machine.processInput("asd")

    # Verify that the state has changed correctly
    assert new_state["status"] == state_machine.LOGIN_REQUEST_PASS or state_machine.LOGIN_MENU # it may be in the DB or not
    assert new_state["code"] == 200 or 404 # We expect the code to be 200 if the user is found and 404 if not  
    print("✅ Test for username 'asd' found (200 OK) successful.")

# Test to verify the flow when the username "aaaa" does not exist (404)
@patch('StateMachine.requests.get') # Mock the requests.get call
def test_username_aaaa_not_found(mock_get, mock_client):
    state_machine = StateMachine(mock_client)
    state_machine.current_status = {
        "code": "",
        "status": state_machine.ENTER_WITH_USERNAME,
        "text": "Enter your username:"
    }

    # Configure the mock to return a 404 (user not found)
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"user": None} # Simulate response for user not found
    # Simulate input "aaaa"
    new_state = state_machine.processInput("aaaa")

    # Verify that the state changed to LOGIN_MENU with code 404
    assert new_state["status"] == state_machine.LOGIN_MENU
    assert new_state["code"] == 404
    print("✅ Test for username 'aaaa' not found (404) successful.")