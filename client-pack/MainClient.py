from StateMachine import StateMachine
from Client import Client
from DisplayManager import DisplayManager

class MainClient:
    def __init__(self):
        self.client = Client()
        self.state_machine = StateMachine(self.client)

    def run(self):
        self.state_machine.run()

if __name__ == "__main__":
    display_manager = DisplayManager()
    display_manager.show_welcome()
    main_client = MainClient()
    main_client.run()