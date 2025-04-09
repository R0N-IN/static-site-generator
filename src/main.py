from create_page import *
from node_processing_functions import *

ORIGIN_PATH = "/home/ronin/workspace/github.com/R0N-IN/static-site/static" 
DEST_PATH = "/home/ronin/workspace/github.com/R0N-IN/static-site/public"    

##Create the page from the markdown file 
##**Note: Add prompt to ask the user for the path of the markdown file and the template file.

GENERATE_FROM_PATH = "/home/ronin/workspace/github.com/R0N-IN/static-site/content"
GENERATE_TEMPLATE_PATH = "/home/ronin/workspace/github.com/R0N-IN/static-site/template.html"
GENERATE_DEST_PATH = "/home/ronin/workspace/github.com/R0N-IN/static-site/public"

def main(): 
    copy_content(ORIGIN_PATH, DEST_PATH)
    # Generate the page from the markdown file
    generate_page_recursive(GENERATE_FROM_PATH, GENERATE_TEMPLATE_PATH, GENERATE_DEST_PATH)
    

main()

'''
 with open(GENERATE_FROM_PATH, "r") as f:
        markdown = f.read()


        node = markdown_to_html_node(markdown)
        html = node.to_html()
        print('HTML content generated successfully')
        print(f"HTML content: {html}")
      
    text = "![JRR Tolkien sitting](/images/tolkien.png)"  
    text_node = text_to_text_nodes(text)
    html_node = markdown_to_html_node(tex)
    #html_node = text_node_to_html_node(text_node[0])

    print(f"Text nodes: {text_node}")
    print(f"HTML node: {html_node}")


    text = "![JRR Tolkien sitting](/images/tolkien.png)"  
    node = markdown_to_html_node(text)
    print(f"Node: {node}")
    print("==========================")
    text_node = node.to_html()
    print(f"Text nodes: {text_node}")
'''