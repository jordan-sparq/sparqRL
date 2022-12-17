import random
import numpy as np
import pandas as pd
from sparqRL.environment.environment import discrete_environment
from pattern.gcp import bigquery
GCP_PROJECT = "gatwick-dev-285508"

class gatwick_customers:
    def __init__(self, data: pd.DataFrame = None, n_daily_customers=None, **kwargs):
        """
        Requires a pandas DataFrame as input that has the following columns:
        leadtime_calendardays_binned, lengthofstay_24hrperiods_binned, ss_ppd_difference_binned,
        terminal_short, price_long_stay, price_valet, segment_short, itemRevenue
        @param data: data with the above columns where each row is 1 customer
        @param n_daily_customers: number of rows in the data
        """

        self.data = data
        # Save important environment information
        self._lt_state = [
            min(self.data.leadtime_calendardays_binned.dropna()),
            max(self.data.leadtime_calendardays_binned.dropna())
        ]

        self._dur_state = [
            min(self.data.lengthofstay_24hrperiods_binned.dropna()),
            max(self.data.lengthofstay_24hrperiods_binned.dropna())
        ]

        self._ss_diff_state = [
            min(self.data.ss_ppd_difference_binned.dropna()),
            max(self.data.ss_ppd_difference_binned.dropna())
        ]

        self._terminal_state = [
            min(self.data.terminal_short.dropna()),
            max(self.data.terminal_short.dropna())
        ]

        self._segments_state = [
            min(self.data.segment_short.dropna()),
            max(self.data.segment_short.dropna())
        ]

        self._competitor_state = [
            min(self.data.valet_comp_diff_binned.dropna()),
            max(self.data.valet_comp_diff_binned.dropna())
        ]

        self._n_daily_customers = n_daily_customers
        # Create the action/obs space.
        env = discrete_environment(state_range=[self._segments_state,
                                                self._terminal_state,
                                                self._lt_state,
                                                self._dur_state,
                                                self._ss_diff_state,
                                                self._competitor_state,
                                                self._competitor_state  # twice as we have ls and valet
                                                ],
                                   action_range=[
                                       [1, 501],
                                       [1, 1500]
                                   ])

        self.state_space = env.state_space
        self.action_space = env.action_space

        print(f"state space is {self.state_space}\naction space is {self.action_space}")
        self._validate_inputs()

    def _validate_inputs(self):
        """
        helper function to make sure the number of daily customers input
        is not greater than the number of customers in the data
        """
        if self._n_daily_customers is None or self._n_daily_customers > len(self.data):
            print(
                f"Value for n_daily_customers can not be larger than the len(data)!."
                f"Setting n_daily_customers: {len(self.data)}"
            )
            self._n_daily_customers = len(self.data)

    def reset(self, seed=None, options=None):
        """
        reset function for data runs.
        @param seed: NOT IMPLEMENTED
        @param options: NOT IMPLEMENTED
        @return: the reset state is returned and the dataset
        """

        # sample n daily customers from the table
        if self._n_daily_customers == len(self.data):
            self._sample_data = self.data
        else:
            self._sample_data = self.data.sample(self._n_daily_customers).reset_index(drop=True)
        # read lead time and durations from table --> make sure integers
        lt = self._sample_data.leadtime_calendardays_binned.to_numpy() - 1
        # duration cannot be 0 days --> 1 day has to be index 0
        dur = self._sample_data.lengthofstay_24hrperiods_binned.astype(int).to_numpy() - 1
        # read a ss price difference
        ss_diff = self._sample_data.ss_ppd_difference_binned.astype(int)
        # read terminal. north --> 0, south --> 1
        terminal = np.array([0 if x == "north" else 1 for x in self._sample_data.terminal_short])
        # ls competitor difference
        ls_comp_diff = self._sample_data.long_stay_comp_diff_binned
        # valet competitor difference
        valet_comp_diff = self._sample_data.valet_comp_diff_binned
        # define a segmentation - for data --> 0 for business and 1 for short break
        seg = np.array(
            [0 if i == "Business" else 1 if i == "Short Break" else 2 for i in self._sample_data.segment_short]
        )
        # now each dimension of the state has n customer values
        self._state = np.array([seg, terminal, lt, dur, ss_diff, ls_comp_diff, valet_comp_diff])
        return self._state, self._sample_data

    def step(self, state, action, substep, data_sample=None):
        """
        step function for data runs.
        @param state: state of environment
        @param action: prices shown for each customer
        @param substep: NOT CURRENTLY USED
        @param data_sample: 1 customer at a time
        @return: reward, absorbing = True (stop)
        """
        # Another required function. What happens when we take an action?

        # reward is 0 if nan
        reward = 0
        # if data_sample is none --> haven't seen the state before
        if data_sample is not None:
            # if the price paid is nan, reward = 0
            data_sample_ = data_sample.itemRevenue.dropna()
            # if not nan, reward = revenue
            if len(data_sample_) != 0:
                reward = data_sample.itemrevenue_per_10p_per_day.values[0]

        # Set the absorbing flag if we've arrived at day zero. Episode ends
        absorbing = True

        # Return all the information + empty dictionary (used to pass additional information)
        return reward, absorbing, {}

def main():

    print("Generating Gatwick Environment")

    data = bigquery.query_to_dataframe(
            query_str="""
    SELECT *
    FROM `rl_model.unconstrained_look2book_comp`
    WHERE date BETWEEN '2022-10-01' AND  '2022-11-01'
    AND long_stay_comp_diff_binned IS NOT NULL
    AND valet_comp_diff_binned IS NOT NULL
    """,
            project=GCP_PROJECT,
        )
    print(data.head())

if __name__ == "__main__":
    main()