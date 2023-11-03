from simplempi.parfor import parfor, smpi


def test_parfor():
    """Test the parfor method."""

    # Make a list of things (20 numbers in this case)
    test_list = list(range(20))

    # run the loop in parallel
    for item in parfor(test_list):
        # Do some work on each item
        smpi.pprint(item**2)
