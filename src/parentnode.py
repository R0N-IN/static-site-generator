from htmlnode import HTMLNode
from leafnode import LeafNode   

class ParentNode(HTMLNode): 
    def __init__(self,tag,children,props = None):
        super().__init__(tag,None,children, props)
    
    def to_html(self):
        node_html = ""
        if self.tag == None: 
            raise ValueError("All parent nodes must have a tag")
        
        else:
            if isinstance(self,ParentNode):
                if self.children == None:
                    raise ValueError("All parent nodes must have children")
                
                node_html += f"<{self.tag}{self.props_to_html()}>"
                for node in self.children:
                    node_html += f"{node.to_html()}"
                node_html += f"</{self.tag}>"
        return node_html 
    
    def __eq__(self, other):
        return (self.tag == other.tag and
                self.children == other.children and
                self.props == other.props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    