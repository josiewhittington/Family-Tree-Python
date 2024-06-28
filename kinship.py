'''Finds relationship between two people.'''
from argparse import ArgumentParser
from json import load
from relationships import relationships
from sys import argv

class Person:
    '''Represents a person in a family.
    Attributes:
        name(string): person's name
        gender(string): person's gender
        parents(list): person's parents
        spouse(instance): person's spouse'''
    def __init__(self, name, gender):
        '''Initializes the name and gender. Creates a list of parents and
        creates an instance of spouse.
        
        Args:
            name(string): person's name
            gender(string): person's gender
        
        Side effects:
            Initializes attributes name and gender.
            Set attributes parents and spouse. '''
        self.name = name
        self.gender = gender
        self.parents = []
        self.spouse = None
    def add_parent(self,parent):
        '''Create an instance of parent.
        
        Args:
            parent(string): parent's name'''
        if isinstance(parent, Person):
            self.parents.append(parent)
    def set_spouse(self, spouse):
        '''Create an instance of spouse.
        
        Args:
            spouse(string): spouse name'''
        if isinstance(spouse, Person):
            self.spouse = spouse
    def connections(self):
        '''Identifies connections lowest common relatives.
        Returns:
            dict: a dictionary of person's connections and relatives'''
        cdict = {self:""}
        queue = [self]
        while queue:
            person = queue.pop(0)
            personpath = cdict[person]
            for parent in person.parents:
                if parent not in cdict:
                    parentpath = personpath + "P"
                    cdict[parent] = parentpath
                    queue.append(parent)
            if "S" not in personpath and person.spouse is not None and person.spouse not in cdict:
                spousepath = personpath + "S"
                cdict[person.spouse]=spousepath
                queue.append(person.spouse)
        return cdict
    def relation_to(self, other):
        '''Finds kinship term of relative and self.
        Args:
            other(string): the other person's name
            
        Returns:
            string: kinship term'''
        self_connect = self.connections()
        other_connect = other.connections()
        shared = set(self_connect.keys()) & set(other_connect.keys())
        if not shared:
            return None
        min_path = min(shared, key=lambda path:
            len(f"{self_connect[path]}:{other_connect[path]}"))
        path = f"{self_connect[min_path]}:{other_connect[min_path]}"
        if path in relationships:
            term = relationships[path][self.gender]
            return term
        else:
            return "distant relative"

class Family:
    '''Keeps track of instances and defines relationshis.
    
    Attributes:
        information(dict): dictionary of individuals, parents, and couples
        name1(string): name of first person
        name2(string): name of second person'''
    def __init__(self, information):
        '''Initializes a dictionary of individuals, parents, and couples. Calls
        Person class and add_parent and set_spouse method.
        
        Args:
            information(dict): dictionary of individuals, parents, and couples
        
        Side effects:
            Initializes dictionary'''
        self.people = {}
        for name, gender in information["individuals"].items():
            p = Person(name, gender)
            self.people[name] = p
        for child,parents in information["parents"].items():
            children = self.people[child]
            for parent in parents:
                parent_name = self.people[parent]
                children.add_parent(parent_name)
        for couple in information["couples"]:
            spouse1, spouse2 = [self.people[name] for name in couple]
            spouse1.set_spouse(spouse2)
            spouse2.set_spouse(spouse1)
            
    def relation(self, name1, name2):
        '''Takes two names and returns their relationship. Calls relation_to 
        method.
        
        Args:
            name1(string): name of first person
            name2(string): name of second person
            
        Returns: 
            str: relationship between two people'''
        person1 = self.people[name1]
        person2 = self.people[name2]
        return person1.relation_to(person2)
    
def main(filepath, name1, name2):
    '''Takes file and two names and prints their relationship. Calls Family
    class and relation method.
    
    Args:
        name1(string): name of first person
        name2(string): name of second person
    
    Side effects:
        Prints to terminal'''
    with open(filepath, "r", encoding="utf-8") as f:
        familydata = load(f)
    fam = Family(familydata)
    relate = fam.relation(name1, name2)
    if relate is None:
        print(f"{name1} is not related to {name2}")
    else:
        print(f"{name1} is {name2}'s {relate}")

def parse_args(args):
    '''Allows for user to use terminal to test code and determines what the
    inputs mean.
    
    Args:
        args(list): command-line arguments
        
    Returns:
        namespace: the parse arguments as a namespace'''
    argument = ArgumentParser()
    argument.add_argument("filepath", help="file of names")
    argument.add_argument("name1", help="first name to look for")
    argument.add_argument("name2", help="second name to find path to first name")
    return argument.parse_args(args)

if __name__ == "__main__":
    args = parse_args(argv[1:])
    main(args.filepath, args.name1, args.name2)