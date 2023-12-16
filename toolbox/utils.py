import os


def tail(file_name, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    if not os.path.exists(file_name):
        return []

    with open(file_name, "r") as f:
        # loop until we find X lines
        while len(lines_found) < lines:
            try:
                f.seek(block_counter * _buffer, os.SEEK_END)
            except IOError:  # either file is too small, or too many lines requested
                f.seek(0)
                lines_found = f.readlines()
                break

            lines_found = f.readlines()

            # we found enough lines, get out
            # Removed this line because it was redundant the while will catch
            # it, I left it for history
            # if len(lines_found) > lines:
            #    break

            # decrement the block counter to get the
            # next X bytes
            block_counter -= 1

    return lines_found[-lines:]