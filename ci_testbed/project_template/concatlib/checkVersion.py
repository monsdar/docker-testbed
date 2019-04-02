
import re
import subprocess
import sys

INSPECTCMD = "conan inspect conanfile.py -a version" #TODO: Use --raw (or whatever #3913 comes up with)
SEMVER_SHORT_REGEX = re.compile("[0-9]*\.[0-9]*\.[0-9]*")
SEMVER_LONG_REGEX = re.compile("[0-9]*\.[0-9]*\.[0-9]*-[a-zA-Z0-9]*")

output = subprocess.check_output(INSPECTCMD, shell=True).decode("utf-8")

if not (SEMVER_SHORT_REGEX.search(output) or SEMVER_LONG_REGEX.search(output)):
    print("ERROR: No valid SemVer found")
    sys.exit(1)
print("Valid SemVer found: " + output)

