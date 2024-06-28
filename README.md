A Python program that reads in a dataset of family members and determines how 
people are related.

Relationship Paths:
    - P: parent
    - S: spouse

    - All people have a connection to themselves (empty string: "")
    - The path to a person’s parent is "P"; the path to a grandparent is "PP";
        the path to a great-grandparent is "PPP"
    - The path to a person’s spouse is "S". The path to a spouse’s parent 
        is "SP".
    - The path to a step-parent is "PS"


Person Class
    The Person class represents a person in a family. 

    Attributes:
    - name: the person’s name (str)
    - gender: the person’s gender (str): 'f', 'm', 'n'
    - parents: the person’s parents, if known 
    - spouse: the person’s spouse, if applicable

Family Class
    The Family class keeps track of all the Person instances you create. 

    Attribute:
    - people: name and value of Person objecy (dict)