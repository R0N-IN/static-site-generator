import re
import os
import shutil
from node_processing_functions import *


def copy_content(origin_path, dest_path):
    if os.path.exists(origin_path) and os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        shutil.copytree(origin_path, dest_path)
    else:
        print("The file does not exist")

def extract_title(markdown):
    title = ""
    markdown =markdown.lstrip()
 
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    if title == "":
        raise Exception("No title found in the markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")
    print(f"Using template {template_path}")
    
    try:
        with open(from_path, "r") as f:
            markdown = f.read()
            title = extract_title(markdown)
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        title = extract_title(markdown)
        
        page = template.replace("{{ Title }}", title)\
               .replace("{{ Content }}", html)\
               .replace('href="/', f'href="{basepath}')\
               .replace('src="/', f'src="{basepath}')
        
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(page)
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return
        
def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    items = os.listdir(dir_path_content)
    for item in items:
        from_path = os.path.join(dir_path_content, item)
        
        if os.path.isdir(from_path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            if not os.path.exists(new_dest_dir_path):
                os.makedirs(new_dest_dir_path)
            generate_page_recursive(from_path, template_path, new_dest_dir_path, basepath)
            
        elif item.endswith(".md"):
            dest_file_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(from_path, template_path, dest_file_path, basepath)
            print(f"Generated page {dest_file_path}")