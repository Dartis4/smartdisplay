import os
from os.path import exists

PATH = os.path.dirname(__file__)
DEFAULT_FILENAME = os.path.join(PATH, 'location.txt')


def check():
    return exists(DEFAULT_FILENAME)


def update():
    print('Please enter your country (Format = "COUNTRY", i.e. "GB" = Great Britain): ')
    country = input()
    print('Please enter your state if applicable (Format = "STATE", i.e. "NY" = New York): ')
    state = input()
    print('Please enter your city (Format = "City", i.e. "London"): ')
    city = input()

    location = city + ', ' + state + ', ' + country

    with open(DEFAULT_FILENAME, 'w') as f:
        f.write(location)
        return location


def update_loc():
    if check():
        print('Would you like to update your location? y/N')
        option = input()
        if option.lower() == 'y':
            return update()
        else:
            print('Location unchanged')
            return_loc()
    else:
        return update()


def return_loc():
    with open(DEFAULT_FILENAME, 'r') as f:
        return f.readline()


def main():
    update_loc()


if __name__ == '__main__':
    main()
