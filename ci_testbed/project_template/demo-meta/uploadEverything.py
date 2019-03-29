import subprocess
import os
import re
import sys

FIXEDVERSIONSFILE = "fixed_versions_conanfile.txt"
REF_REGEX = re.compile("(([a-zA-Z0-9_-]*)\/.*@(.*\/[a-zA-Z0-9-_]*))")

print("Uploading from " + FIXEDVERSIONSFILE + "...")

if not os.path.exists(FIXEDVERSIONSFILE):
    print("No " + FIXEDVERSIONSFILE + " exists")
    sys.exit()

with open(FIXEDVERSIONSFILE) as conanFile:
    content = conanFile.readlines()
    
    for line in content:
        refResult = REF_REGEX.search(line)
        if not refResult:
            continue
            
        #upload fixed reference version
        uploadCmd = "conan upload " + refResult.group(1) + " -r release-server --all"
        print(uploadCmd)
        subprocess.run(uploadCmd, stderr=sys.stderr, stdout=sys.stdout, shell=True)
        
        #upload HEAD alias
        aliasCmd = "conan alias " + refResult.group(2) + "/HEAD@" + refResult.group(3) + " " + refResult.group(1)
        uploadCmd = "conan upload " + refResult.group(2) + "/HEAD@" + refResult.group(3) + " -r release-server --all"
        print(uploadCmd)
        subprocess.run(uploadCmd, stderr=sys.stderr, stdout=sys.stdout, shell=True)