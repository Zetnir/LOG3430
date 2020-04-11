from collections import Counter
from functools import total_ordering
import heapq

def compress_binary_string(string):
    """Convert string of 0s and 1s to bits, and reinterpret bits as string"""
    # string composed of bytes, each 8 bits
    # so must make sure string of 0s and 1s
    # has length which is a multiplier of 8
    pad = (8 - len(string)) % 8
    padded_data = '0' * pad + string

    chars = [
        # convert string to binary and reinterpret as ascii char
        chr(int(eight, 2)) for eight in
        # split padded_data in segments of length 8
        [padded_data[i:i + 8] for i in range(0, len(padded_data), 8)]
    ]

    return ''.join(chars), pad


def expand_compressed_string(string, pad=0):
    padded_data = ''.join([
        # interpret ascii char as base 2 int, convert to binary string,
        # remove 0b cruft, and ensure has length 8
        bin(ord(char))[2:].zfill(8) for char in string
    ])

    return padded_data[pad:]


@total_ordering
class Huffman(object):
    def __init__(self, weight, data, left=None, right=None):
        self.weight = weight
        self.data = data
        self.left = left
        self.right = right
        self.codebook = {}
        self.build_codebook()

    def __eq__(self, other):
        return (self.data, self.weight) == (other.data, other.weight)

    def __lt__(self, other):
        if self.weight == other.weight:
            return self.data < other.data
        else:
            return self.weight < other.weight

    def __repr__(self):
        ldata = self.left and self.left.data
        rdata = self.right and self.right.data
        return (
            f'<Huffman(data: {self.data}, '
            f'left: {ldata}, right: {rdata})>'
        )

    def is_leaf(self):
        return not self.right and not self.left

    def build_codebook(self):
        """Create map of chars to binary string encodings"""
        self.codebook = {}

        nodes = {
            '0': self.left,
            '1': self.right,
        }

        for prefix, node in nodes.items():
            if not node:
                continue

            if node.is_leaf():
                self.codebook[node.data] = prefix

            for data, code in node.codebook.items():
                self.codebook[data] = prefix + code

        return self.codebook

    @classmethod
    def from_string(cls, string):
        # count frequencies of characters in string
        frequency = Counter(string)
        # build priority queue from frequency counter -
        # higher frequency characters have lower priority
        heap = [Huffman(weight, data) for data, weight
                in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            weight = left.weight + right.weight
            data = left.data + right.data

            parent = Huffman(weight, data, left, right)
            heapq.heappush(heap, parent)

        return heapq.heappop(heap)

    def __encode_tree(self, leaves):
        if self.is_leaf():
            leaves.append(self.data)
            return '1'

        header = '0'
        header += self.left.__encode_tree(leaves)
        header += self.right.__encode_tree(leaves)
        return header

    def encode_tree(self):
        leaves = []
        encoded_tree = self.__encode_tree(leaves)
        leaves = ''.join(leaves)
        return encoded_tree, leaves

    @classmethod
    def unzip_tree(cls, encoded_tree, leaves, idx=0):
        leaves = list(leaves)

        def unzip_tree_helper():
            nonlocal idx
            nonlocal leaves
            nonlocal encoded_tree

            if idx >= len(encoded_tree):
                return None
            char = encoded_tree[idx]
            # leaf
            if char == '1':
                idx += 1
                data = leaves.pop(0)
                return Huffman(0, data)

            idx += 1
            left = unzip_tree_helper()
            right = unzip_tree_helper()

            data = ''

            if left:
                data += left.data
            if right:
                data += right.data

            return Huffman(0, data, left, right)

        return unzip_tree_helper()

    @classmethod
    def zip(cls, string):
        huff_tree = Huffman.from_string(string)
        encoded_data = huff_tree.huffman_encode(string)
        compressed_data, data_pad = compress_binary_string(encoded_data)

        encoded_tree, leaves = huff_tree.encode_tree()
        compressed_tree, tree_pad = compress_binary_string(encoded_tree)

        segments = [len(compressed_tree), tree_pad, len(leaves), data_pad]
        segments = [str(e) for e in segments]

        segments.append(compressed_tree + leaves + compressed_data)
        return '|'.join(segments)

    @classmethod
    def unzip(cls, string):
        meta = string.split('|', 4)

        if len(meta) != 5:
            raise ValueError('Error when encoding the string')

        meta[:4] = [int(e) for e in meta[:4]]
        ctree_len, tree_pad, leave_len, data_pad, rest = meta

        compressed_tree = rest[:ctree_len]
        leaves = rest[ctree_len:ctree_len+leave_len]
        compressed_data = rest[ctree_len+leave_len:]

        encoded_data = expand_compressed_string(compressed_data, data_pad)
        encoded_tree = expand_compressed_string(compressed_tree, tree_pad)

        huff_tree = Huffman.unzip_tree(encoded_tree, leaves)
        return huff_tree.huffman_decode(encoded_data)

    def huffman_encode(self, string):
        return ''.join([self.codebook[char] for char in string])

    def huffman_decode(self, string):
        decoded_string = ''
        node = self

        for char in string:
            if char == '0':
                node = node.left
            elif char == '1':
                node = node.right
            else:
                raise ValueError('Error when encoding the string')

            if node.is_leaf():
                decoded_string += node.data
                node = self

        return decoded_string


def zip(string: str) -> str:
    return Huffman.zip(string)

def unzip(string: str) -> str:
    return Huffman.unzip(string)

encodage = zip("Polymtl is polymtl")
print(encodage)
decodage = unzip(encodage)
print(decodage)