import sys
import os

def vulnerable_function(input_str):
    if len(input_str) > 50:
        print("MOCK_CRASH: Buffer Overflow detected!")
        sys.exit(-1073741819) 
    else:
        print(f"Input accepted: {input_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mock_target.py <input>")
        sys.exit(1)
    
    vulnerable_function(sys.argv[1])
