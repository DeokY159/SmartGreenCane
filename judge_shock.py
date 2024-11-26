import sys
import time

def judge_shock(impact, timestamp):
    shock_threshold=70
    shock_flag="not"
    if impact>=shock_threshold:
        shock_flag="is"
    return (impact, shock_flag, timestamp)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Invalid number of arguments")
        sys.exit(1)

    impact = int(sys.argv[1])
    timestamp = sys.argv[2]

    result = judge_shock(impact, timestamp)

    print(result)  