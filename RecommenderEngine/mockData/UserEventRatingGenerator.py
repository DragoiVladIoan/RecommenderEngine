import random

import time
import pandas as pd


'''
Users will be split into 4 categories:
1.Active Users: 10% of all users - these users will have frequencies for 50-70% of all merchants
2.Moderately Active Users: 20% of all users - these users will have frequencies for 30-49% of all merchants
3.Average Users: 50% of all users - these users will have frequencies for 15-29% of all merchants
4.Inactive Users: 20% of all users = these users will have frequencies for 0-14% of all merchants
'''


start_time = time.time()


class MockInputDataEventNames:
    def __init__(self):
        self._event_names_df = self._read_event_names()

    @staticmethod
    def _read_event_names():
        fields = ['EVENT_ID', 'TITLE']
        df = pd.read_csv('data/Events.csv', sep=",", skipinitialspace=True, usecols=fields)
        return df

    def export_event_names_files(self):
        return self._event_names_df


class MockInputDataUserRatings:
    def __init__(self):
        self._columns = ['USER_ID', 'EVENT_ID', 'RATING']
        self._df = pd.DataFrame(columns=self._columns)
        mocker_event_names = MockInputDataEventNames()
        self._df_event_names = mocker_event_names.export_event_names_files()
        self._number_of_users = 10000
        self._types_of_users = []
        self._number_of_events_per_user = []
        self._number_of_event_names = len(self._df_event_names.index)
        print(self._number_of_event_names)
        self._number_of_active_users = 0
        self._number_of_mod_active_users = 0
        self._number_of_avg_users = 0
        self._number_of_inactive_users = 0

    def generate_users(self):
        for i in range(0, self._number_of_users):
            probability = random.random()
            self._types_of_users.append(probability)
        return self._types_of_users

    def generate_number_of_events_per_user(self):
        for i in range(0, len(self._types_of_users)):
            if self._types_of_users[i] < 0.1:
                activity = random.uniform(50, 70)
                number_of_events_visited = activity/100 * self._number_of_event_names
                self._number_of_events_per_user.append(int(number_of_events_visited))
            elif 0.1 <= self._types_of_users[i] < 0.3:
                activity = random.uniform(30, 50)
                number_of_events_visited = activity / 100 * self._number_of_event_names
                self._number_of_events_per_user.append(int(number_of_events_visited))
            elif 0.3 <= self._types_of_users[i] < 0.8:
                activity = random.uniform(15, 30)
                number_of_events_visited = activity / 100 * self._number_of_event_names
                self._number_of_events_per_user.append(int(number_of_events_visited))
            elif 0.8 <= self._types_of_users[i] < 1:
                activity = random.uniform(0, 15)
                number_of_events_visited = activity / 100 * self._number_of_event_names
                self._number_of_events_per_user.append(int(number_of_events_visited))
        return self._number_of_events_per_user

    def generate_final_dataframe(self):
        for i in range(0, self._number_of_users):
            print("Currently generating ratings for user id: ", i)
            event_frequencies = [0 for x in range(0, self._number_of_event_names)]
            target = self._number_of_events_per_user[i]
            target_events = random.sample(range(0, self._number_of_event_names-1), target)
            user_results = []
            for j in range(0, len(target_events)):
                event_frequencies[target_events[j]] = self.generate_rating()
                user_results.append([i, target_events[j], event_frequencies[target_events[j]]])
            temp = pd.DataFrame(user_results, columns=self._columns)
            self._df = self._df.append(temp)
        return self._df

    def generate_rating(self):
        return random.randint(1, 5)

    def generate_statistics(self):
        for i in range(0, len(self._types_of_users)):
            if self._types_of_users[i] < 0.1:
                self._number_of_active_users += 1
            elif 0.1 <= self._types_of_users[i] < 0.3:
                self._number_of_mod_active_users += 1
            elif 0.3 <= self._types_of_users[i] < 0.8:
                self._number_of_avg_users += 1
            elif 0.8 <= self._types_of_users[i] < 1:
                self._number_of_inactive_users += 1

    def export(self):
        print("Currently exporting frequencies")
        self._df.to_csv('data/EventRatings.csv', index=False)

    def visualize_statistics(self):
        print("Out of", self._number_of_users, "users:")
        print("Active Users:", self._number_of_active_users, ' - ', self._number_of_active_users/self._number_of_users *100, "%")
        print("Moderately Active Users:", self._number_of_mod_active_users, ' - ', self._number_of_mod_active_users/self._number_of_users * 100, "%")
        print("Average Users:", self._number_of_avg_users, ' - ', self._number_of_avg_users/self._number_of_users * 100, "%")
        print("Inactive Users:", self._number_of_inactive_users, ' - ', self._number_of_inactive_users/self._number_of_users * 100, "%")


mocker = MockInputDataUserRatings()
mocker.generate_users()
mocker.generate_number_of_events_per_user()
mocker.generate_final_dataframe()
mocker.export()


print("--- %s seconds ---" % (time.time() - start_time))
