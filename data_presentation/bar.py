from typing import Iterator

from tqdm import tqdm


def bar(iter: Iterator, name):
    return tqdm(iter,
                colour="green",
                bar_format=f'{name}'+': {l_bar}{bar}|||',
                ncols=150)