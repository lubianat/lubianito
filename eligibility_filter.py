# eligibility_filter.py
from datetime import datetime

class EligibilityFilter:
    def __init__(self, contests_df):
        self.contests_df = contests_df

    def filter_eligible(self):
        today = datetime.now()

        # Filter contests that are still open
        open_contests = self.contests_df[self.contests_df['deadline'] > today]

        # Additional filters: check for Brazilian eligibility
        open_contests['eligible'] = open_contests['title'].apply(lambda x: 'Brazil' in x or 'open to all' in x)
        eligible_contests = open_contests[open_contests['eligible'] == True]

        return eligible_contests
