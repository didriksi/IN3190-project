import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Hyperparameters sent by the client are passed as command-line arguments to the script.
    parser.add_argument("-p", "--parse-data", action="store_true",
                        help="Load the data, and make derivative files from it"\
                             " that is easier to read and use.")
    
    args = parser.parse()

    return args


def main():
    args = parse_arguments()


if __name__ == "__main__":
    main()