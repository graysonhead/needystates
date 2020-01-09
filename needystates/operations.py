from enum import Enum


class Operations(Enum):
    pass


class StateOperations(Operations):
    """
    Determine what operation should be performed to satisfy the need
    """
    SET = 1
    """
    Boolean: set sets the boolean to either True or False
    List: set replaces the entire list with a new list
    String: replaces the string with the new string
    Integer: replaces the integer with the new integer
    """

    DELETE = 2
    """
    Removes the attribute
    """

    CLEAR = 3
    """
    List: deletes the whole list
    """

    GET = 4
    """
    Only used by ad-hoc commands, returns the value of the attribute
    """

    ADD = 5
    """
    List: adds a new value (or values) to the listfrom runcible.core.need import NeedOperation as Op
    """