from dataclasses import dataclass
from typing import Union
import numpy as np


def _check_ranges_len(ranges) -> bool:
    """
    _check_ranges

    this checks that every element of a list has a length of 2

    :param ranges: ranges to test
    :return: bool
    """
    it = iter(ranges)
    the_len = 2
    #  assert len = 2
    if not all(len(l) == the_len for l in it):
        return False
    # assert min <= max
    if not all(l[1] - l[0] >= 0 for l in ranges):
        return False
    else:
        return True


@dataclass
class discrete_environment:
    """
    This class is used to store the information of the environment.

    :param state_range: state[min, max] min and max value of each state
    :param action_range: action[min, max] min and max value of each action

    """

    state_range: list[list] = None
    action_range: list[list] = None

    def __post_init__(self):
        """
        post init
        """

        assert (self.state_range is not None) & (self.action_range is not None), \
            "User must define both the state and action range, e.g state_range = [[1, 5], [5, 10], [2, 5]], " \
            "where the first element is the minimum value a state/action can take, and the second element is the " \
            "maximum (inclusive)."

        assert _check_ranges_len(self.state_range) & _check_ranges_len(self.action_range), \
            "Range of both the state and action spaces must have a length of 2: [min, max] (inclusive). " \
            "The max must be >= min."

        self.state_space = self._get_dimensions(self.state_range)
        self.action_space = self._get_dimensions(self.action_range)

        self.state_values = self._get_values(self.state_range)
        self.action_values = self._get_values(self.action_range)

    def _get_dimensions(self, state_or_action_range: list[list]):
        """
        _get_dimensions

        get dimensions of state or action space

        :param state_or_action_range: state or action ranges list[list]
        :return: [tuple] tuple of number of possible values for each state or action
        """
        _dimensions = []
        for i in state_or_action_range:
            if i[0] == i[1]:
                _dimensions.append(1)
            else:
                _dimensions.append((i[1] - i[0]) + 1)  # + 1 as it includes the min and max

        return tuple(_dimensions)

    def _get_values(self, state_or_action_range: list[list]):
        """
        get_values

        get possible values of each state or action

        :param state_or_action_range: state or action ranges list[list]
        :return: [list[list]] all possible values of each state or action
        """

        _possible_values = []

        for i in state_or_action_range:
            if i[0] == i[1]:
                _possible_values.append([i[0]])
            else:
                _possible_values.append(list(np.arange(i[0], i[1] + 1)))

        return _possible_values

    def __getitem__(self, space: str = "action") -> tuple:
        """
        __getitem__

        get action or state information

        :param space: [str] space should be any of the following ["action", "state"]
        :return: tuple containing the space chosen by the user
        """

        _spaces = ["action", "state"]

        assert space in _spaces, f"Please choose any one of {_spaces}"

        if space == "action":
            return (self.action_space, self.action_range)

        elif space == "state":
            return (self.state_space, self.state_range)

    def __setitem__(self, space, value: tuple) -> None:
        """
        __setitem__

        set action or state space

        :param space:
        :param value:
        :return:
        """

        _spaces = ["action", "state"]

        assert space in _spaces, f"Please choose any one of {_spaces}"
        assert type(value) == tuple, "value must be a tuple"

        if space == "action":
            self.action_space = value

        elif space == "state":
            self.state_space = value

        return None
