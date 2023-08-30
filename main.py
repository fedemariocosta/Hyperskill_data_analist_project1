import pandas as pd
import requests
import os
pd.set_option('display.max_columns', None)

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
data_A = pd.read_xml('../Data/A_office_data.xml')
data_B = pd.read_xml('../Data/B_office_data.xml')
data_rh = pd.read_xml('../Data/hr_data.xml')

new_A_index = "A" + data_A['employee_office_id'].astype(str)
data_A.set_index(new_A_index, inplace=True)
data_A.index.name = None

new_B_index = "B" + data_B['employee_office_id'].astype(str)
data_B.set_index(new_B_index, inplace=True)
data_A.index.name = None

data_rh.set_index('employee_id', inplace=True)
data_rh.index.name = None

A_index = data_A.index.to_list()
B_index = data_B.index.to_list()
rh_index = data_rh.index.to_list()

# print(A_index)
# print(B_index)
# print(rh_index)

combined_data = pd.concat([data_A, data_B], axis=0)
merged_data = combined_data.merge(data_rh, how='left', indicator=True, left_index=True, right_index=True)
merged_data = merged_data.dropna()
merged_data.drop(columns=['employee_office_id', '_merge'], inplace=True)
merged_data.sort_index(inplace=True)


# print(list(merged_data.index))
# print(list(merged_data.columns))

# top_ten = merged_data.sort_values(by='average_monthly_hours', ascending=False).head(10).Department

# print(top_ten.to_list())

# number_projects = merged_data.query("(Department == 'IT') & (salary == 'low')").number_project.sum()

# print(number_projects)

# print([merged_data.loc['A4', ['last_evaluation', 'satisfaction_level']].to_list(),
#       merged_data.loc['B7064', ['last_evaluation', 'satisfaction_level']].to_list(),
#       merged_data.loc['A3033', ['last_evaluation', 'satisfaction_level']].to_list()])

def count_bigger_5(x):
    return (x > 5).sum()


""""
print(merged_data.columns)

merged_data['left'] = merged_data['left'].astype(int)

group_left = merged_data.groupby('left')

agg_functions = {
    'number_project': ['median', count_bigger_5],
    'time_spend_company': ['mean', 'median'],
    'Work_accident': 'mean',
    'last_evaluation': ['mean', 'std']
}

print(group_left.agg(agg_functions).round(2).to_dict())
"""

# Use df.pivot_table() to generate the first pivot table: Department as index, left and salary as columns, average_monthly_hours as values.
# Output median values in the table.

first_pivot_table = merged_data.pivot_table(index='Department', columns=['left', 'salary'],
                                            values='average_monthly_hours', aggfunc='median').round(2)

first_pt_filtered = first_pivot_table.loc[(first_pivot_table[(0.0, 'high')] < first_pivot_table[(0.0, 'medium')]) |
                                          (first_pivot_table[(1.0, 'low')] < first_pivot_table[(1.0, 'high')])]

second_pivot_table = merged_data.pivot_table(index='time_spend_company', columns='promotion_last_5years',
                                             values=['satisfaction_level', 'last_evaluation'],
                                             aggfunc=['min', 'max', 'mean']).round(2)

second_pt_filtered = second_pivot_table.loc[
    (second_pivot_table[('mean', 'last_evaluation', 0)] > second_pivot_table[('mean', 'last_evaluation', 1)])]

print(first_pt_filtered.to_dict())
print(second_pt_filtered.to_dict())
