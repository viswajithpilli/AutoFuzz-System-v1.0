import sys
import os
from src.payloader import Payloader
from src.monitor import Monitor
from src.analyzer import Analyzer


class Fuzzer:
    def __init__(self, binary_path):
        self.binary_path = binary_path
        self.payloader = Payloader()
        self.monitor = Monitor(binary_path)
        self.analyzer = Analyzer(binary_path)

    def fuzz(self):
        pattern_len = 200
        payload = self.payloader.generate_cyclic_pattern(pattern_len)
        
        result = self.monitor.run(payload)
        
        output_data = {
            "crashed": result['crashed'],
            "return_code": result['return_code'],
            "output": result['output'],
            "error": result['error'],
            "eip": None,
            "offset": None,
            "status": "Safe"
        }

        if result['crashed']:
            output_data["status"] = "Vulnerable"
            
            analysis = self.analyzer.analyze_crash(payload)
            
            if not analysis.get('error'):
                eip = analysis['register_value']
                output_data["eip"] = eip
                
                try:
                    val = int(eip, 16)
                    offset = self.payloader.find_offset(val, payload)
                    output_data["offset"] = offset
                except:
                    pass
            else:
                 output_data["analysis_error"] = analysis['error']
        
        return output_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fuzzer.py <path_to_binary>")
        sys.exit(1)

    binary_path = sys.argv[1]
    fuzzer = Fuzzer(binary_path)
    print(f"[*] Starting Fuzzer against: {binary_path}")
    res = fuzzer.fuzz()
    print(res)
