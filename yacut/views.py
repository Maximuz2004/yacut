import string
import random

from yacut import ID_MAX_LENGTH, MIN_LENGTH


AVAILABLE_CHARS = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
)

def get_unique_short_id():
    id_length = random.randrange(MIN_LENGTH, ID_MAX_LENGTH+1)
    return ''.join(
        [random.choice(AVAILABLE_CHARS) for _ in range(
            random.randrange(MIN_LENGTH, ID_MAX_LENGTH+1)
        )]
    )


if __name__ == '__main__':
    print(get_unique_short_id())