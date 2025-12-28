import win32com.client

def get_outlook_app():
    """Returns the Outlook application COM object."""
    return win32com.client.Dispatch("Outlook.Application")

class JMPRunner:
    """Class to run JMP scripts via COM interface."""
    
    def __init__(self):
        self.jmp = win32com.client.Dispatch("JMP.Application")
    
    def run_script(self, script_path: str):
        """Runs a JMP script located at script_path."""
        self.jmp.RunJSLFile(script_path)