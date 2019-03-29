import json
import os
import re
import sys

CONANFILE = "conanfile.txt"
DEPFILE = "dependencies.json"
FIXEDVERSIONSFILE = "fixed_versions_conanfile.txt"
REF_REGEX = re.compile("([a-zA-Z0-9_-]*)\/.*@(.*\/[a-zA-Z0-9-_]*)")

print("Generating " + FIXEDVERSIONSFILE + "...")

if not os.path.exists(CONANFILE):
    print("No " + CONANFILE + " exists")
    sys.exit()

if not os.path.exists(DEPFILE):
    print("No " + DEPFILE + " exists")
    sys.exit()

newContent = []
with open(CONANFILE) as conanFile:
    content = conanFile.readlines()
    with open(DEPFILE) as depFile:
        deps = json.load(depFile)
        for line in content:
            if not REF_REGEX.search(line):
                newContent.append(line)
                continue
        
            hasReplaced = False
            for dep in deps:
                if not REF_REGEX.search(dep['reference']):
                    continue
                currentDepName = REF_REGEX.search(dep['reference']).group(1)
                currentDepChannel = REF_REGEX.search(dep['reference']).group(2)
                currentLineName = REF_REGEX.search(line).group(1)
                currentLineChannel = REF_REGEX.search(line).group(2)
                if  currentDepName == currentLineName and currentDepChannel == currentLineChannel:
                    print("Replacing " + line.strip('\n') + " with " + dep['reference'])
                    newContent.append(line.replace(line.strip('\n'), dep['reference']))
                    hasReplaced = True
                    break
            if not hasReplaced:
                newContent.append(line)

with open("fixed_versions_conanfile.txt", "w") as resultFile:
    resultFile.writelines(newContent)

print("...generated " + FIXEDVERSIONSFILE)