
import subprocess
import os
import re
import sys

FIXEDVERSIONSFILE = "fixed_versions_conanfile.txt"
REF_REGEX = re.compile("([a-zA-Z0-9_-]*\/.*@.*\/[a-zA-Z0-9-_]*)")

print("Uploading from " + FIXEDVERSIONSFILE + "...")

if not os.path.exists(FIXEDVERSIONSFILE):
    print("No " + FIXEDVERSIONSFILE + " exists")
    sys.exit()

with open(CONANFILE) as conanFile:
    content = conanFile.readlines()
    
    for line in content:
        refResult = REF_REGEX.search(line)
        if not refResult
            continue
        uploadCmd = "conan upload " + refResult.group[1] + " -r release-server"
        subprocess.run(uploadCmd, stderr=sys.stderr, stdout=sys.stdout)