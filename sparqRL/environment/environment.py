from dataclasses import dataclass
from typing import Union
import numpy as np


def _check_ranges(ranges) -> bool:
    """
    _check_ranges

    this checks that every element of a list has a length of 2

    :param ranges: ranges to test
    :return: bool
    """
    it = iter(ranges)
    the_len = 2
    if not all(len(l) == the_len for l in it):
        return False
    else:
        return True


@dataclass
class discrete_environment:
    """
    This class is used to store the information of the environment.

    :param state_space: [tuple] number of possible values in each state
    :param action_space: [tuple] number of possible values in each action
    :param state_range: state[min, max] min and max value of each state
    :param action_range: action[min, max] min and max value of each action

    """

    state_space: tuple = None
    action_space: tuple = None
    state_range: list[list] = None
    action_range: list[list] = None

    def __post_init__(self):
        """
        check inputs are correct format
        """
        if self.state_range is not None:
            # state_range outranks state_space
            # if a user defines the ranges of each state, we can define the spaces based on that
            assert _check_ranges(self.state_range), "ranges must have a length of 2"
            self.state_space = tuple(
                [self.state_range[i][1] - self.state_range[i][0] for i in range(len(self.state_range))])

        if self.action_range is not None:
            assert _check_ranges(self.action_range), "ranges must have a length of 2"
            self.action_space = tuple(
                [self.action_range[i][1] - self.action_range[i][0] for i in range(len(self.action_range))])

    def get_ranges(self):
        """
        get possible values of all states and actions

        :return: tuple(state ranges, action ranges)
        """
        # if no ranges are given, assume they can be 0 - max
        if self.state_range is None:
            self.state_values = [np.arange(0, self.state_space[i]) for i in range(len(self.state_space))]

        if self.action_range is None:
            self.action_values = [np.arange(0, self.action_space[i]) for i in range(len(self.action_space))]

        # user defines specific ranges for states/actions
        if self.state_range is not None:
            self.state_values = [np.arange(self.state_range[i][0], self.state_range[i][1]) for i in
                                 range(len(self.state_range))]

        if self.action_range is not None:
            self.action_values = [np.arange(self.action_range[i][0], self.action_range[i][1]) for i in
                                  range(len(self.action_range))]
        # return (state_ranges, action_ranges)
        return (self.state_values, self.action_values)

    def __getitem__(self, space: str = "action") -> tuple:
        """
        __getitem__

        get action, state, or state-action space

        :param space: [str] space should be any of the following ["action", "state", "state-action"]
        :return: tuple containing the space chosen by the user
        """

        _spaces = ["action", "state", "state-action"]

        assert space in _spaces, f"Please choose any one of {_spaces}"

        if space == "action":
            return self.action_space

        elif space == "state":
            return self.state_space

        elif space == "state-action":
            return self.state_space + self.action_space

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
