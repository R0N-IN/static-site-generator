from create_page import *
from node_processing_functions import *
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ORIGIN_PATH = os.path.join(project_root, "static")
DEST_PATH = os.path.join(project_root, "docs")
GENERATE_FROM_PATH = os.path.join(project_root, "content")
GENERATE_TEMPLATE_PATH = os.path.join(project_root, "template.html")
GENERATE_DEST_PATH = os.path.join(project_root, "docs")


def main(): 
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_content(ORIGIN_PATH, DEST_PATH)
    # Generate the page from the markdown file
    generate_page_recursive(GENERATE_FROM_PATH, GENERATE_TEMPLATE_PATH, GENERATE_DEST_PATH, basepath)
    print(basepath)

main()