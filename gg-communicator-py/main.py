import sys
import src.greeter as greeter
import time


def main():
    args = sys.argv[1:]
    while True:
        print(greeter.get_greeting(" ".join(args)))
        time.sleep(5)


if __name__ == "__main__":
    main()
