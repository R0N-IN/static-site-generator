from create_page import *
from node_processing_functions import *
import sys


BASEPATH = sys.argv[1] if len(sys.argv) > 1 else "/"

ORIGIN_PATH = os.path.join(BASEPATH, "static")
DEST_PATH = os.path.join(BASEPATH, "docs")    

##Create the page from the markdown file 
##**Note: Add prompt to ask the user for the path of the markdown file and the template file.



GENERATE_FROM_PATH = os.path.join(BASEPATH, "content")
GENERATE_TEMPLATE_PATH = os.path.join(BASEPATH, "template.html")
GENERATE_DEST_PATH = os.path.join(BASEPATH, "public")

def main(): 
    
    copy_content(ORIGIN_PATH, DEST_PATH)
    # Generate the page from the markdown file
    generate_page_recursive(GENERATE_FROM_PATH, GENERATE_TEMPLATE_PATH, GENERATE_DEST_PATH, BASEPATH)
    

main()