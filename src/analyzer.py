import subprocess
import re
import os

class Analyzer:
    def __init__(self, binary_path):
        self.binary_path = binary_path

    def analyze_crash(self, payload):
        gdb_commands = [
            f"file {self.binary_path}",
            f"run {payload}",
            "info registers",
            "quit"
        ]
        
        try:
            cmd = ["gdb", "--batch"]
            for c in gdb_commands:
                cmd.extend(["-ex", c])
            
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                timeout=5
            )
            
            output = result.stdout
            
            eip_match = re.search(r"eip\s+(0x[0-9a-f]+)", output, re.IGNORECASE)
            rip_match = re.search(r"rip\s+(0x[0-9a-f]+)", output, re.IGNORECASE)
            
            reg_val = None
            if eip_match:
                reg_val = eip_match.group(1)
            elif rip_match:
                reg_val = rip_match.group(1)
                
            if reg_val:
                return {
                    'error': None,
                    'register_value': reg_val,
                    'gdb_output': output
                }
            else:
                 return {
                    'error': "Could not find EIP/RIP in GDB output",
                    'register_value': None, 
                    'gdb_output': output
                }

        except FileNotFoundError:
            return {'error': "GDB not found in PATH", 'register_value': None, 'gdb_output': ""}
        except Exception as e:
            return {'error': str(e), 'register_value': None, 'gdb_output': ""}
