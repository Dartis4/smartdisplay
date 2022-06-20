from os.path import exists

DEFAULT_FILENAME = 'ow-key.txt'


def check():
    return exists(DEFAULT_FILENAME)


def update():
    print('Please enter your api key: ')
    key = input().strip().lower()
    with open(DEFAULT_FILENAME, 'w') as f:
        f.write(key)
        return key


def update_key():
    if check():
        print('An Open-Weather api key already exists, would you like to set a new one? y/N')
        option = input()
        if option.lower() == 'y':
            return update()
        else:
            print('Key unchanged')
            return_key()
    else:
        return update()


def return_key():
    with open(DEFAULT_FILENAME, 'r') as f:
        return f.readline()


def main():
    update_key()


if __name__ == '__main__':
    main()
