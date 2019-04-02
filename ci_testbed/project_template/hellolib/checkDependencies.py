import json
import os
import re
import sys

BLACKLIST = []
BLACKLIST.append("old/release")
BLACKLIST.append("old/thirdparty")

CONANFILETXT = "conanfile.txt"
CONANFILEPY = "conanfile.py"
REF_REGEX = re.compile("([a-zA-Z0-9_-]*)\/.*@(.*\/[a-zA-Z0-9-_]*)")

conanfile = ""
if os.path.exists(CONANFILETXT):
    conanfile = CONANFILETXT
elif os.path.exists(CONANFILEPY):
    conanfile = CONANFILEPY
else:
    print("No conanfile recipe exists")
    sys.exit(1)

with open(conanfile) as f:
    content = f.readlines()
    for line in content:
        if not REF_REGEX.search(line):
            continue

        currentChannel = REF_REGEX.search(line).group(2)
        for entry in BLACKLIST:
            if entry in currentChannel:
                print("ERROR: This component depends on a deprecated dependency: " + REF_REGEX.search(line).group(0))
                sys.exit(1)

print("No blacklisted dependencies found!")