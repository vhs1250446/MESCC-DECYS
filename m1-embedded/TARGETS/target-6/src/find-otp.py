#!/usr/bin/env python3

from pathlib import Path
import serial
import re
import time
import sys

ALAN_PASSWORD = "alanzvnswtxmjxjcikzpmemegrjqaugjmidnmxiynjghxmdnlffbmw"
CC_PASSWORD = "cncgijucsnrdyfwsatpqxiodhlnqrfxutzzygjtmnkmofphuhzzaj"
PORT = "/dev/cu.usbserial-10"
BAUD = 115200


def init(serialObj):
    # initial wait for arduino setup
    time.sleep(2)
    out = serialObj.readall()
    if out:
        sys.stdout.write(out.decode())

    serialObj.write(ALAN_PASSWORD.encode() + b"\n")
    print(ALAN_PASSWORD)
    time.sleep(1)

    out = serialObj.readall()
    if out:
        sys.stdout.write(out.decode())

    serialObj.write(CC_PASSWORD.encode() + b"\n")
    print(CC_PASSWORD)
    time.sleep(2)

    # skip all the text after logging as alan
    out = serialObj.readall()
    if out:
        sys.stdout.write(out.decode())
    time.sleep(2)


def main():
    with serial.Serial(PORT, BAUD, timeout=0.1) as port:

        init(port)

        # the idea is:

        # loop
        #  send guess to the device
        #  read response from the device

        #  if response is correct
        #  then print the secret output and stop program
        #  else extract the expected_number from the error response

        #  if we are seeing expected_number for the second time and haven't updated our guess yet
        #  then set guess to expected_number
        #  else save expected_number to seen_numbers

        filler = "42"
        count = 1
        matched = False
        seen = {}
        while True:
            port.write(filler.encode() + b"\n")
            print(filler)
            time.sleep(1)

            # read all output from the device
            out = port.readall()
            if out:
                sys.stdout.write(out.decode())
            text = out.decode().strip()

            if re.search("Incorrect", text) is None:
                time.sleep(2)
                out = port.readall()
                if out:
                    sys.stdout.write(out.decode())
                sys.exit()

            try:
                number = re.findall(r'\d+', text)[-1]
            except IndexError:
                continue

            if number in seen and not matched:
                filler = number
                matched = True
                count = 0
                print(f"---- Duplicate Found [{number}] ----")
                continue
            else:
                seen[number] = True

            count = count + 1


if __name__ == "__main__":
    raise SystemExit(main())
