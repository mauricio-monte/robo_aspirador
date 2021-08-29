class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.ultima_busca = None
        
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get(self):
        return self.data

    def add(self, child, pai):
        if self.data == pai:
            node = TreeNode(child)
            self.add_child(node)
        else:
            for children in self.children:
                children.add(child, pai)
    
    def search(self, root, child):
        print('#CHILD:', child, '#Data:', self.data, self.data == child)
        if self.data == child:
            return child
        
        for children in self.children:
            if children.data == child:
                root.ultima_busca = children
                return children
            else:
                children.search(root, child)

    def caminho(self):
        lista = []
        p = self.parent
        while p:
            lista.append(p.data)
            p = p.parent
        print(lista)
        return lista