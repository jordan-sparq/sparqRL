import sparse
from dataclasses import dataclass
from typing import Union


@dataclass
class table:

    """
    tabular environment

    for q learning and SARSA algorithms

    inputs:
        shape - [tuple] shape of table
        initial_value - [float] initial value of every element
        _table - [sparse.DOK] user can initialise this table which ignores other params
    """

    shape: Union[tuple, list] = None
    initial_value: float = 0
    _table: sparse.DOK = None

    assert shape is not None, "user must define a shape for the table [tuple]"

    if _table is None:
        _table = sparse.DOK(shape, fill_value=initial_value)

    def __getitem__(self, key: tuple) -> Union[float, int, sparse.DOK]:
        """
        __getitem__

        get item of the table determined by element

        :param key: [tuple] element of table user would like to return
        :return: table[element], this could be a number of types
        """
        # if table has one element, return that element
        if self._table.shape == (1,):
            return self._table[0]
        else:
            # return element of the table
            return self._table[key]

    def __setitem__(self, key: tuple, value) -> sparse.DOK:
        """
        __setitem__

        set an item of the table to a user defined value

        :param key: element of table user would like to replace
        :param value: value to insert
        :return: table with replaced value
        """
        # if there is only one element, replace that one
        if self._table.shape == (1,):
            self._table[0] = value
        else:
            self._table[key] = value

def main():

    return None

if __name__ == "__main__":
    """
    just to show how to use this class
    """
    main()
