# Script for transfering notes from notable to obsidian

import argparse
from ast import parse
import os
import re
import sys

# Regex patterns to find tags, linked notes, and attachments
tagPattern = r'tags:\s*\[(.*?)\]'
linkPattern = r'\[\]\(@note/([^)]+)\)'
attachmentPattern = r'!\[\]\(@attachment/([^\)]+)\)'

def replaceTags(match):

                    tags = match.group(1).split(',')
                    reFormTags = "\n".join([f"  - {tag.strip()}" for tag in tags])
                    return "tags:\n" + reFormTags + "\n"
  
def notable_to_obsidian (srcDir, tarDir):
    try:
        if not os.path.exists(srcDir):
            print (f"Source directory '{srcDir}' for your Notable notes does not exist.")
            return

        if not os.path.exists(tarDir):
            print (f"Target directory/Obisidan vault '{tarDir}' does not exist.")

            if (input ("Allow script to make target directory/vault? [y/n]") == 'y'):
                "...\n...vault made..."
                os.makedirs(tarDir)
            else:
                print ("Exiting script...")
                return

        for file in os.listdir(srcDir):
            srcPath = os.path.join(srcDir, file)
            tarPath = os.path.join(tarDir, file)

            with open(srcPath,'r', encoding="utf8") as srcFile:
                with open(tarPath, 'w', encoding="utf8") as targFile:
                    for line in srcFile:
                        # if line contains tags, links, attachments... process
                        line = re.sub(linkPattern, lambda match: r'[[{}]]'.format(match.group(1).replace('%20', ' ')), line)
                        line = re.sub(attachmentPattern, r'![](\1)', line)
                        line = re.sub(tagPattern, replaceTags, line)
                        #match = re.search(tagPattern, line)
                        targFile.write(line)
 
        print("Your Notable repo has been converted to Obsidian..")              

    except Exception as e:
        print(f"An error occurred:\n {str(e)}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert Notable md notes to Obsidian.")
    parser.add_argument("src_dir", type=str, help="Source directory containing Notable notes. (.Notable/notes)")
    parser.add_argument("tar_dir", type=str, help="Target directory directory for Obsidian vault")

    args = parser.parse_args()
    notable_to_obsidian(args.src_dir, args.tar_dir)
