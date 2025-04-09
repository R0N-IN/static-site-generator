from enum import Enum
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from markdown_block import BlockType
import re


def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode('a',text_node.text, {'href': text_node.url})
            case TextType.IMAGE:
                return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
            case _:
                raise Exception("Invalid text type")
            


def split_nodes_delimiter(old_nodes, delimeter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif node.text.count(delimeter) % 2 == 0:
            text_to_split = node.text
            while(delimeter in text_to_split):
                index = text_to_split.find(delimeter)
                if index > 0:
                    new_nodes.append(TextNode(text_to_split[:index], TextType.TEXT))
                    text_to_split = text_to_split[index + len(delimeter):]
                    index = text_to_split.find(delimeter)
                    new_nodes.append(TextNode(text_to_split[:index], text_type))
                    text_to_split = text_to_split[index + len(delimeter):]
                else:
                    text_to_split = text_to_split[index + len(delimeter):]
                    index = text_to_split.find(delimeter)
                    new_nodes.append(TextNode(text_to_split[:index], text_type))
                    text_to_split = text_to_split[index + len(delimeter):]
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else: 
            raise Exception("Invalid Markdown Syntax") 
    return new_nodes

def extract_markdown_images(text): 
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text): 
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
 
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_tuples = extract_markdown_images(node.text)
        if image_tuples != []:
            text_to_split = node.text
            for image_tuple in image_tuples:
                delimiter = f"![{image_tuple[0]}]({image_tuple[1]})"
                index = text_to_split.find(delimiter)
                if index > 0:
                    new_nodes.append(TextNode(text_to_split[:index], TextType.TEXT))
                    new_nodes.append(TextNode(image_tuple[0], TextType.IMAGE,image_tuple[1]))
                    text_to_split = text_to_split[index + len(delimiter):]
                else:
                    new_nodes.append(TextNode(image_tuple[0], TextType.IMAGE,image_tuple[1]))
                    text_to_split = text_to_split[index + len(delimiter):]
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else: 
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_tuples = extract_markdown_links(node.text)
        if link_tuples != []:
            text_to_split = node.text
            for link_tuple in link_tuples:
                delimiter = f"[{link_tuple[0]}]({link_tuple[1]})"
                index = text_to_split.find(delimiter)
                if index > 0:
                    new_nodes.append(TextNode(text_to_split[:index], TextType.TEXT))
                    new_nodes.append(TextNode(link_tuple[0], TextType.LINK,link_tuple[1]))
                    text_to_split = text_to_split[index + len(delimiter):]
                else:
                    new_nodes.append(TextNode(link_tuple[0], TextType.LINK,link_tuple[1]))
                    text_to_split = text_to_split[index + len(delimiter):]
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else: 
            new_nodes.append(node)
    return new_nodes
    

def text_to_text_nodes(text):
    text_nodes = []
    new_text = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    new_text = split_nodes_delimiter(new_text, "_", TextType.ITALIC)
    new_text = split_nodes_delimiter(new_text, "`", TextType.CODE)
    new_text = split_nodes_link(new_text)
    new_text = split_nodes_image(new_text)
    for node in new_text:
        text_nodes.append(node)
    return text_nodes



def markdown_to_blocks(text):
    blocks = []
    if text == "":
        return blocks
    else:
        for line in text.split("\n\n"):
            line = re.sub(r"^\s+|\s+$", "", line)
            blocks.append(line.replace('    ',''))
    return blocks

def is_ordered_list(text_block):
    last_number = 0
    for line in text_block.split("\n"):
        if not line.startswith(str(last_number + 1) + ". "):
            return False
        elif int(line[0]) != last_number + 1:
            return False
        else:
            last_number += 1 
    return True

def block_to_block_type (text_block):
    #text_block.strip()

    if (text_block.startswith(('#','##','###','####','#####','######')) and 
        len(text_block.split("\n"))) == 1:
        return BlockType.HEADING
    if text_block.startswith("```") and text_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in text_block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("-") for line in text_block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(text_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_html_nodes(text):
    text_nodes = text_to_text_nodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes    
 

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            block = block[3:-3].lstrip()
            div_node.children.append(ParentNode("pre", [LeafNode("code", block)]))
        elif block_type == BlockType.HEADING:
            header_size = block[:6].count("#")
            div_node.children.append(ParentNode(f"h{header_size}", text_to_html_nodes(block[header_size + 1:])))
        elif block_type == BlockType.QUOTE:
            block = "".join([line.lstrip('> ') for line in block.split("\n")])
            div_node.children.append(ParentNode("blockquote", text_to_html_nodes(block)))
        elif block_type == BlockType.UNORDERED_LIST:
            div_node.children.append(ParentNode("ul", [ParentNode("li", text_to_html_nodes(line[2:])) for line in block.split("\n")]))
        elif block_type == BlockType.ORDERED_LIST:
            div_node.children.append(ParentNode("ol", [ParentNode("li", text_to_html_nodes(line[3:])) for line in block.split("\n")]))
        elif block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            div_node.children.append(ParentNode("p", text_to_html_nodes(block)))
        else:
            raise Exception("Invalid Markdown Syntax")
    return div_node
