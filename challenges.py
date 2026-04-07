ROUNDS = {
    1: [1, 2, 3],
    2: [4, 5, 6],
    3: [7, 8, 9],
}

def vowel_count(x):
    # input: any word → output: number of vowels
    return sum(1 for c in str(x).lower() if c in 'aeiou')

def word_reverse(x):
    # input: any sentence → output: words in reverse order
    return " ".join(str(x).split()[::-1])

def char_count(x):
    # input: any word → output: number of characters
    return len(str(x).replace(" ", ""))

def binary_to_decimal(x):
    # input: binary string like "1010" → output: decimal
    try:
        return int(str(x).strip(), 2)
    except:
        return "invalid input"

def is_palindrome(x):
    # input: any word → output: yes or no
    s = str(x).lower().replace(" ", "")
    return "yes" if s == s[::-1] else "no"

def ascii_sum(x):
    # input: any word → output: sum of ASCII values
    return sum(ord(c) for c in str(x))

def anagram_sort(x):
    # input: any word → output: letters sorted alphabetically
    return "".join(sorted(str(x).lower().replace(" ", "")))

def caesar(x):
    # input: "hello,3" → output: shifted string
    try:
        text, n = x.split(",")
        n = int(n.strip())
        result = ""
        for c in text.strip():
            if c.isalpha():
                base = ord('a') if c.islower() else ord('A')
                result += chr((ord(c) - base + n) % 26 + base)
            else:
                result += c
        return result
    except:
        return "invalid input"

def pig_latin(x):
    # input: any word → output: pig latin version
    words = str(x).lower().split()
    result = []
    for w in words:
        vowels = "aeiou"
        if w[0] in vowels:
            result.append(w + "yay")
        else:
            i = 0
            while i < len(w) and w[i] not in vowels:
                i += 1
            result.append(w[i:] + w[:i] + "ay")
    return " ".join(result)

CHALLENGES = [
    vowel_count,       # C1 — easy
    word_reverse,      # C2 — easy
    char_count,        # C3 — easy
    binary_to_decimal, # C4 — medium
    is_palindrome,     # C5 — medium
    ascii_sum,         # C6 — medium
    anagram_sort,      # C7 — hard
    caesar,            # C8 — hard
    pig_latin,         # C9 — hard
]

ANSWERS = {
    1: "count vowels",
    2: "reverse words",
    3: "count characters",
    4: "binary to decimal",
    5: "palindrome check",
    6: "sum of ascii values",
    7: "anagram sort",
    8: "caesar cipher",
    9: "pig latin",
}

HINTS = {
    1: 'Input: any word → outputs number of vowels (a,e,i,o,u)',
    2: 'Input: "hello world" → outputs "world hello"',
    3: 'Input: any word → outputs total number of characters',
    4: 'Input: binary string like "1010" → outputs decimal number',
    5: 'Input: any word → outputs "yes" or "no"',
    6: 'Input: any word → outputs sum of ASCII value of each letter',
    7: 'Input: any word → outputs letters sorted A to Z',
    8: 'Input: "hello,3" → shifts each letter by 3 positions',
    9: 'Input: any word → outputs pig latin version',
}

def get_challenge(chal_id):
    try:
        return CHALLENGES[chal_id - 1]
    except IndexError:
        return None