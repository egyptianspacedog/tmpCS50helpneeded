import sys
import csv


def main():
    argc = len(sys.argv)
    if (argc != 3):
        print("Usage: python dna.py [database] [sequence]")
        exit()

    # Sets variable name for each argv argument
    arg_database = sys.argv[1]
    arg_sequence = sys.argv[2]

    # Converts sequence csv file to string, and returns as thus
    sequence = get_sequence(arg_sequence)
    seq_len = len(sequence)

    # Returns STR patterns as list
    STR_array = return_STRs(arg_database)
    STR_array_len = len(STR_array)

    # Counts highest instance of consecutively reoccurring STRs
    STR_values = STR_count(sequence, seq_len, STR_array, STR_array_len)

    DNA_match(STR_values, arg_database, STR_array_len)


# Reads argv2 (sequence), and returns text within as a string
def get_sequence(arg_sequence):
    with open(arg_sequence, 'r') as csv_sequence:
        sequence = csv_sequence.read()

    return sequence


# Reads STR headers from arg1 (database) and returns as list
def return_STRs(arg_database):
    with open(arg_database, 'r') as csv_database:
        database = csv.reader(csv_database)

        STR_array = []

        for row in database:
            for column in row:
                STR_array.append(column)
            break

        # Removes first column header (name)
        del STR_array[0]
    return STR_array


def STR_count(sequence, seq_len, STR_array, STR_array_len):
    # Creates a list to store max recurrence values for each STR
    STR_count_values = [0] * STR_array_len
    # Temp value to store current count of STR recurrence
    temp_value = 0

    # Iterates over each STR in STR_array
    for i in range(STR_array_len):
        STR_len = len(STR_array[i])

        # Iterates over each sequence element
        for j in range(seq_len):
            # Ensures it's still physically possible for STR to be present in sequence
            while (seq_len - j >= STR_len):
                # Gets sequence substring of length STR_len, starting from jth element
                sub = sequence[j:(j + (STR_len))]

                # Compares current substring to current STR
                if (sub == STR_array[i]):
                    temp_value += 1
                    j += STR_len
                else:
                    # Ensures current STR_count_value is highest
                    if (temp_value > STR_count_values[i]):
                        STR_count_values[i] = temp_value
                    # Resets temp_value to break count, and pushes j forward by 1
                    temp_value = 0
                    j += 1
        i += 1

    return STR_count_values


# Searches database file for DNA matches
def DNA_match(STR_values, arg_database, STR_array_len):
    with open(arg_database, 'r') as csv_database:
        database = csv.reader(csv_database)

        name_array = [] * (STR_array_len + 1)
        next(database)

        # Iterates over one row of database at a time
        for row in database:
            name_array.clear()
            # Copies entire row into name_array list
            for column in row:
                name_array.append(column)

            # Converts name_array number strings to actual ints
            for i in range(STR_array_len):
                name_array[i + 1] = int(name_array[i + 1])

            # Checks if a row's STR values match the sequence's values, prints the row name if match is found
            match = 0
            for i in range(0, STR_array_len, + 1):
                if (name_array[i + 1] == STR_values[i]):
                    match += 1

                if (match == STR_array_len):
                    print(name_array[0])
                    exit()

        print("No match")
        exit()


main()