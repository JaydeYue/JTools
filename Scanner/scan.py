__author__ = "Jayde Yue"
# Website: www.jaydeyue.com
logo = """
        |
        |
        |
        |
   _____/
"""
print(logo)


import sys
from Scanner import Scanner


def main():
    scanner = Scanner(sys.argv[1:])
    scanner.run()


if __name__ == '__main__': main()
