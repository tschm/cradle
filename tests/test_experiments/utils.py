import random
import string


def randomword(length, prefix=""):
    letters = string.ascii_lowercase
    return prefix + "_" + "".join(random.choice(letters) for i in range(length))
