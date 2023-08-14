def valid_cube_number_and_row(number, row):
    if number < 0 or number > 27:
        return False
    if row < 1 or row > 7:
        return False

    if number > 20 and row != 7:
        return False
    elif 21 > number > 14 and row != 6:
        return False
    elif 15 > number > 9 and row != 5:
        return False
    elif 10 > number > 5 and row != 4:
        return False
    elif 6 > number > 2 and row != 3:
        return False
    elif 3 > number > 0 and row != 2:
        return False
    elif number == 0 and row != 1:
        return False

    return True
