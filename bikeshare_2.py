import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

months_list = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]
days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    print("Type 'exit' anytime to quit.\n")

    # City input
    while True:
        city = input("Enter city (chicago, new york city, washington): ").strip().lower()
        if city == 'exit':
            return None, None, None
        if city in CITY_DATA:
            break
        print("Invalid city. Try again.")

    # Filter type input
    while True:
        filter_type = input("Would you like to filter by 'month', 'day', 'both', or 'none'? ").strip().lower()
        if filter_type == 'exit':
            return None, None, None
        if filter_type in ['month', 'day', 'both', 'none']:
            break
        print("Invalid option. Please choose: month, day, both, or none.")

    month = 'all'
    day = 'all'

    if filter_type in ['month', 'both']:
        while True:
            month_input = input("Enter month (1–12 or name), or 'all': ").strip().lower()
            if month_input == 'exit':
                return None, None, None
            if month_input == 'all':
                month = 'all'
                break
            if month_input.isdigit() and 1 <= int(month_input) <= 12:
                month = months_list[int(month_input) - 1]
                break
            if month_input in months_list:
                month = month_input
                break
            print("Invalid month.")

    if filter_type in ['day', 'both']:
        while True:
            day_input = input("Enter day (1–7 or name), or 'all': ").strip().lower()
            if day_input == 'exit':
                return None, None, None
            if day_input == 'all':
                day = 'all'
                break
            if day_input.isdigit() and 1 <= int(day_input) <= 7:
                day = days_list[int(day_input) - 1]
                break
            if day_input in days_list:
                day = day_input
                break
            print("Invalid day.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """ 
    Load data based on input
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_num = months_list.index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """ 
    Time Statistics for input data
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'month' in df:
        print('Most Common Month:', df['month'].mode()[0])
    if 'day_of_week' in df:
        print('Most Common Day of Week:', df['day_of_week'].mode()[0])
    print('Most Common Start Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """ 
    Stations statistics for input data
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Common Start Station:', df['Start Station'].mode()[0])
    print('Most Common End Station:', df['End Station'].mode()[0])

    df['Start-End Combo'] = df['Start Station'] + " to " + df['End Station']
    print('Most Common Trip:', df['Start-End Combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """ 
    Trip duration statistics for input data
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel Time:', df['Trip Duration'].sum())
    print('Average Travel Time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """ 
    Displays statistics on bikeshare users, including additional insights.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Count of user types
    print('User Types:\n', df['User Type'].value_counts())

    # Gender breakdown
    if 'Gender' in df.columns:
        print('\nGender Breakdown:\n', df['Gender'].value_counts())
        print('Missing Gender Data:', df['Gender'].isnull().sum())
    else:
        print('\nNo Gender data available.')

    # Birth year statistics
    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:', int(df['Birth Year'].min()))
        print('Most Recent Birth Year:', int(df['Birth Year'].max()))
        print('Most Common Birth Year:', int(df['Birth Year'].mode()[0]))

        # Additional birth year stats
        print('Average Birth Year:', round(df['Birth Year'].mean(), 1))
        print('Number of Users with Birth Year data:', df['Birth Year'].count())
    else:
        print('\nNo Birth Year data available.')

    # Count of missing values in key columns
    print('\nMissing Values Summary:')
    for col in ['User Type', 'Gender', 'Birth Year']:
        if col in df.columns:
            print(f'  {col}: {df[col].isnull().sum()} missing')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print("🚲 Welcome to the Bikeshare Data Explorer!")

    while True:
        city, month, day = get_filters()

        if city is None:
            print("👋 User exited. Goodbye!")
            break

        df = load_data(city, month, day)

        if df.empty:
            print("\n⚠️ No data available for the selected filters.")
            restart = input("🔁 Would you like to try again? (yes/no): ").strip().lower()
            if restart != 'yes':
                print("👋 Goodbye!")
                break
            continue

        # Display 5 rows at a time if user wants
        row_index = 0
        print("\n📊 Preview of raw data:")
        while True:
            show = input("🔍 Would you like to see 5 rows of data? (yes/no): ").strip().lower()
            if show == 'yes':
                print(df.iloc[row_index:row_index + 5])
                row_index += 5
                if row_index >= len(df):
                    print("✅ No more data to display.")
                    break
            elif show == 'no':
                break
            else:
                print("❌ Invalid input. Please type 'yes' or 'no'.")

        print("\n📈 Generating statistics...\n")
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\n🔁 Would you like to restart the analysis? (yes/no): ").strip().lower()
        if restart != 'yes':
            print("👋 Thanks for using the Bikeshare Data Explorer. Goodbye!")
            break


if __name__ == "__main__":
    main()
