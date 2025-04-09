from create_page import *
from node_processing_functions import *
import sys

ORIGIN_PATH = "/Users/mchavezguzman/Documents/workspace/github/personal/ssg/static" 
DEST_PATH = "/Users/mchavezguzman/Documents/workspace/github/personal/ssg/docs"    

##Create the page from the markdown file 
##**Note: Add prompt to ask the user for the path of the markdown file and the template file.

GENERATE_FROM_PATH = "/Users/mchavezguzman/Documents/workspace/github/personal/ssg/content"
GENERATE_TEMPLATE_PATH = "/Users/mchavezguzman/Documents/workspace/github/personal/ssg/template.html"
GENERATE_DEST_PATH = "/Users/mchavezguzman/Documents/workspace/github/personal/ssg/docs"

def main(): 
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_content(ORIGIN_PATH, DEST_PATH)
    # Generate the page from the markdown file
    generate_page_recursive(GENERATE_FROM_PATH, GENERATE_TEMPLATE_PATH, GENERATE_DEST_PATH, basepath)
    print(basepath)

main()