import subprocess
import time
import os

class Monitor:
    def __init__(self, binary_path):
        self.binary_path = binary_path

    def run(self, payload):
        try:
            process = subprocess.Popen(
                [self.binary_path, payload],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=2)
            ret_code = process.returncode
            
            crashed = ret_code != 0
            
            return {
                'crashed': crashed,
                'return_code': ret_code,
                'output': stdout,
                'error': stderr
            }

        except subprocess.TimeoutExpired:
            process.kill()
            return {'crashed': False, 'return_code': None, 'output': 'Timeout', 'error': 'Timeout'}
        except Exception as e:
            return {'crashed': False, 'return_code': None, 'output': '', 'error': str(e)}

    def is_crash(self, return_code):
        if return_code is None: return False
        known_crashes = [0xC0000005, -1073741819, 139, -11]
        return return_code != 0 and (return_code in known_crashes or return_code < -1 or return_code > 255)
