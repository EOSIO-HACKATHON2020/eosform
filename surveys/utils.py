import random


def gen_eos_username() -> str:
    alphabet = "12345abcdefghijklmnoprstuvwxyz"
    return ''.join(random.choices(alphabet, weights=None, k=12))
