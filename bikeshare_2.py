import time
import pandas as pd
import numpy as np






CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def convert_month(arg):
    """converts months from number to name and viceversa"""
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if arg in months:
        return months.index(arg) + 1
    elif arg in [1, 2, 3, 4, 5, 6]:
        return months[arg - 1]
    else:
        return 'not a valid argument'
        

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to explore: Chicago (c), New York City (ny) or Washington (w)?\nCity: ')       
        if city.lower() in ('chicago', 'c', 'cicago'):
            city = 'chicago'
            break
        elif city.lower() in ('new york city', 'new york', 'n y', 'ny', 'nyc', 'n y c'):
            city = 'new york city'
            break
        elif city.lower() in ('washington', 'washington dc', 'w'):
            city = 'washington'
            break
        else:
            print('\nSorry, you didn\'t enter a valid option.\n')
            


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month are you interested in? January, February, March, April, May, June or "all"?\nMonth: ')
        if month.lower() in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            month = month.lower()
            break
        else:
            print('\nSorry, not a valid input.\nPlease, type in the month name, or "all" to choose all months.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or "all"?\nDay of the week: ')
        if day.lower() in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            break
        else:
            print('\nSorry, not a valid input.\nPlease, type in the name of the day you are interested in, or "all" for the whole week.')
            
    print('\nYou chose to see the data for {}, month: {}, day of the week: {}\n'.format(city.upper(), month.upper(), day.upper()))
    
    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))   
    
    # store number of rows of the unfiltered df
    tot_rows = df.shape[0]
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

     # filter by month if applicable
    if month != 'all':
        chosen_month = convert_month(month)
    
        # filter by month to create the new dataframe
        df = df[df['month']==chosen_month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    #number of rows after applying filters
    filtered_rows = df.shape[0]
    
    message1 = '\nThe {} database has records for {} trips, from January to the end of June 2017.'
    message2 = 'Applying your filter (month: {}, day of week: {}) you get {} records.\n'
    
    # gives info about the number of records used for the following statistics
    print(message1.format(city.upper(), tot_rows))
    if filtered_rows != tot_rows:
        print(message2.format(month.upper(), day.upper(), filtered_rows))
    
    print('-'*40)    

    return df


#!!! ATTENZIONE: sistemare messaggio output e info in caso di filtro mese/giorno. input utente?
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    m = df['month'].unique()
    if len(m) == 1:
        s_month = convert_month(m[0])
        print('No most popular month, we are considering data just for {}'.format(s_month.upper()))
    else:
        m_c_month = convert_month(df['month'].mode()[0])
        print('The most popular MONTH is: {}'.format(m_c_month.upper()))
    

    # display the most common day of week
    d = df['day_of_week'].unique()
    if len(d) == 1:
        print('No most popular day, we are considering data just for {}'.format(d[0].upper()))
    else:
        m_c_day = df['day_of_week'].mode()[0]
        print('The most popular DAY is: {}'.format(m_c_day.upper()))


    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['Hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    m_c_hour = df['Hour'].mode()[0]
    print('The most popular HOUR is: {}'.format(m_c_hour))
   
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    
    # finds the most commonly used start station
    m_c_start = df['Start Station'].mode()[0]


    # finds the most commonly used end station
    m_c_end = df['End Station'].mode()[0]


    # finds the most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    m_c_trip = df['Trip'].mode()[0]

    print('Most popular\n- START STATION is: {}\n- END STATION is: {}\n- TRIP is: {}\n'.format(m_c_start, m_c_end, m_c_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # find the travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    
    # display total travel time
    print('Our bicicles have been ridden a TOTAL of {} in the selected period.'.format(df['Travel Time'].sum()))

    # display mean travel time
    print('The AVERAGE trip takes {}.'.format(df['Travel Time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('The {} trips in the selected period have been taken by:\n'.format(df.shape[0]))
    # Display counts of user types in a new dataframe for nicer result (slightly slower tho)
    df2 = df['User Type'].value_counts()
    user_types = pd.DataFrame({'TYPE':df2.index, 'count':df2.values})
    print(user_types, '\n')

    # Display counts of gender, if the info is available in the DB
    if 'Gender' in df.columns:
        df3 = df['Gender'].value_counts()
        user_gender = pd.DataFrame({'GENDER':df3.index, 'count':df3.values})
        print(user_gender)
    else:
        print('No gender information available for the users of this city.')

    
    # Display earliest, most recent, and most common year of birth, if the info is available in the DB
    if 'Birth Year' in df.columns:
        earl = int(df['Birth Year'].min())
        most_rec = int(df['Birth Year'].max())
        most_comm = int(df['Birth Year'].mode()[0])
        print('\nAbout the YEAR OF BIRTH,\n- the earliest is: {}\n- the most recent is: {}\n- the most common is: {}'.format(earl, most_rec, most_comm))
    else:
        print('No age information available for the users of this city.')
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, city, month, day):
    """asks user if they want to see raw data. displays them 5 at a time and asks if they want more"""
    
    #takes away the columns added by the previous functions, but keeps the filtered DB
    #I use the df for friendlier display (lines of the .csv file should be formatted anyway) and to show the filtered records
    del df['Travel Time']
    del df['Trip']
    del df['month']
    del df['day_of_week']
    del df['Hour']
    
    # to have some context    
    df_shape = df.shape
    print('The database for the city of {}, month: {}, day of the week: {}, has {} rows.'.format(city.upper(), month.upper(), day.upper(), df_shape[0]))
    
    #ask the user if they want to see raw data
    raw_1 = input('Would you like to display the raw data? (Type "yes" to see the raw data, anything else to dismiss): ')
    
    if raw_1.lower() == 'yes':
       
        print(raw_1)
        print(df[:5])
        stop = df_shape[0]
        for i in range(5, stop, 5):
            more_raw = input('Would you like to see 5 more rows? (Type "no" to dismiss, anything else to continue)')
            if more_raw.lower() != 'no':
                print(df[i : i+5])
            else:
                break      
    else:
        print('No raw data requested')
            
    print('-'*40)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        user_stats(df)
        trip_duration_stats(df)
        
        raw_data(df, city, month, day)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Good bye!')
            break


if __name__ == "__main__":
	main()
