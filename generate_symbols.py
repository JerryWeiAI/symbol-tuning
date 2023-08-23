"""Generates a random semantically-unrelated label."""
import os
import pickle
import random
import urllib.request


WORDS_URL_SHORT = 'https://www.mit.edu/~ecprice/wordlist.10000'
WORDS_URL_LONG = 'https://www.mit.edu/~ecprice/wordlist.100000'


def save_pickle(filename, data):
  if os.path.exists(filename):
    print(f'WARNING: PICKLE ALREADY EXISTS AT {filename}, CONTINUING')
    return

  with open(filename, 'wb') as file:
    pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
    print(f'Saved pickle at {filename}')


def load_pickle(filename):
  with open(filename, 'rb') as file:
    return pickle.load(file)


def random_words():
  """Returns list of words from source."""
  if os.path.exists('random_words_10000.pickle') and os.path.exists(
      'random_words_100000.pickle'
  ):
    return load_pickle(
        'random_words_10000.pickle'
    ), load_pickle('random_words_100000.pickle')
  else:
    short_response = urllib.request.urlopen(WORDS_URL_SHORT)
    long_response = urllib.request.urlopen(WORDS_URL_LONG)
    short_txt = short_response.read().decode()
    long_txt = long_response.read().decode()
    short_words = short_txt.splitlines()
    long_words = long_txt.splitlines()
    save_pickle('random_words_10000.pickle', short_words)
    save_pickle('random_words_100000.pickle', long_words)
    return short_words, long_words


def int_to_alphabets(n):
  """Takes in positive integer input, returns character representation."""
  if n <= 0:
    return ''
  elif n <= 26:
    return chr(n + 64)
  else:
    q, r = divmod(n - 1, 26)
    return int_to_alphabets(q) + chr(r + 65)


def generate(
    num_labels,
    is_eval=False,
    num_unique_labels=10000,
    loaded_short_words=None,
    loaded_long_words=None,
):
  """Generates num_labels different symbols to use as labels."""
  if not is_eval:
    assert num_unique_labels <= 10000
    assert num_unique_labels > num_labels

  labels = []

  range_min, range_max = 0, num_unique_labels - 1
  if is_eval:
    range_min = 10000
    range_max = 99999

  if loaded_short_words and loaded_long_words:
    short_words_list = loaded_short_words
    long_words_list = loaded_long_words
  else:
    short_words_list, long_words_list = random_words()

  train_words = set(short_words_list)

  while len(labels) < num_labels:
    while len(labels) < num_labels:
      category = random.randint(0, 2)

      if category == 0:
        labels.append(str(random.randint(range_min, range_max)))
      elif category == 1:
        labels.append(
            int_to_alphabets(random.randint(range_min, range_max) + 1)
        )
      elif category == 2:
        if is_eval:
          label = long_words_list[random.randint(0, len(long_words_list))]
          while label in train_words:
            label = long_words_list[random.randint(0, len(long_words_list))]
          labels.append(label)
        else:
          labels.append(random.choice(short_words_list))

    labels = list(set(labels))

  return labels
