ROUNDS = {
    1: [1, 2, 3, 4, 5],    # 5 easy   — 20 min
    2: [6, 7, 8, 9],        # 4 medium — 25 min
    3: [10, 11, 12],        # 3 hard   — 15 min
}

# ── ROUND 1 — EASY ────────────────────────────────────────────────────────────

def double_consonants(x):
    # doubles every consonant in the word
    vowels = 'aeiou'
    return ''.join(c*2 if c.isalpha() and c.lower() not in vowels else c for c in str(x))

def sum_digits(x):
    # sums all digits in a number
    return sum(int(d) for d in str(x) if d.isdigit())

def reverse_string(x):
    # reverses the entire string character by character
    return str(x)[::-1]

def count_words(x):
    # counts number of words in a sentence
    return len(str(x).split())

def alternate_case(x):
    # alternates upper and lower case starting with upper
    result = ''
    i = 0
    for c in str(x):
        if c.isalpha():
            result += c.upper() if i % 2 == 0 else c.lower()
            i += 1
        else:
            result += c
    return result

# ── ROUND 2 — MEDIUM ──────────────────────────────────────────────────────────

def binary_to_decimal(x):
    # converts binary string to decimal
    try:
        return int(str(x).strip(), 2)
    except:
        return "invalid"

def ascii_sum(x):
    # sums ASCII values of all characters
    return sum(ord(c) for c in str(x))

def fizzbuzz(x):
    # fizzbuzz sequence from 1 to N
    try:
        n = int(str(x).strip())
        if n < 1:
            return "invalid"
        result = []
        for i in range(1, n + 1):
            if i % 15 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return " ".join(result)
    except:
        return "invalid"

def reverse_vowels(x):
    # reverses only the vowels in place
    s = list(str(x))
    vowels = "aeiouAEIOU"
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and s[i] not in vowels:
            i += 1
        while i < j and s[j] not in vowels:
            j -= 1
        if i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
    return "".join(s)

# ── ROUND 3 — HARD ────────────────────────────────────────────────────────────

def caesar(x):
    # caesar cipher with variable shift
    try:
        text, n = x.split(",")
        n = int(n.strip())
        result = ''
        for c in text.strip():
            if c.isalpha():
                base = ord('a') if c.islower() else ord('A')
                result += chr((ord(c) - base + n) % 26 + base)
            else:
                result += c
        return result
    except:
        return "invalid"

def pig_latin(x):
    # converts words to pig latin
    words = str(x).lower().split()
    result = []
    for w in words:
        if not w: continue
        vowels = 'aeiou'
        if w[0] in vowels:
            result.append(w + 'yay')
        else:
            i = 0
            while i < len(w) and w[i] not in vowels:
                i += 1
            result.append(w[i:] + w[:i] + 'ay')
    return ' '.join(result)

def anagram_sort(x):
    # sorts letters of each word alphabetically
    words = str(x).lower().split()
    if not words:
        return ''.join(sorted(str(x).lower().replace(" ","")))
    return ' '.join(''.join(sorted(w)) for w in words)

# ── REGISTRY ──────────────────────────────────────────────────────────────────

CHALLENGES = [
    double_consonants,   # C1  — easy
    sum_digits,          # C2  — easy
    reverse_string,      # C3  — easy
    count_words,         # C4  — easy
    alternate_case,      # C5  — easy
    binary_to_decimal,   # C6  — medium
    ascii_sum,           # C7  — medium
    fizzbuzz,            # C8  — medium
    reverse_vowels,      # C9  — medium
    caesar,              # C10 — hard
    pig_latin,           # C11 — hard
    anagram_sort,        # C12 — hard
]

# Canonical answer labels (used only as fallback display)
ANSWERS = {
    1:  "double consonants",
    2:  "sum of digits",
    3:  "reverse string",
    4:  "count words",
    5:  "alternate case",
    6:  "binary to decimal",
    7:  "sum of ascii values",
    8:  "fizzbuzz",
    9:  "reverse vowels",
    10: "caesar cipher",
    11: "pig latin",
    12: "anagram sort",
}

# Keyword sets — any submitted answer containing ALL keywords in ANY group is correct
ANSWER_KEYWORDS = {
    1:  [
            ["double", "consonant"],
            ["consonant", "twice"],
            ["repeat", "consonant"],
            ["consonant", "doubled"],
        ],
    2:  [
            ["sum", "digit"],
            ["add", "digit"],
            ["digit", "sum"],
            ["total", "digit"],
        ],
    3:  [
            ["reverse", "string"],
            ["reverse", "character"],
            ["string", "reversed"],
            ["flip", "string"],
            ["reverse"], ["reversing"],
                             # single keyword acceptable for very obvious answers
        ],
    4:  [
            ["count", "word"],
            ["word", "count"],
            ["number", "word"],
            ["no", "word"],
        ],
    5:  [
            ["alternate", "case"],
            ["alternating", "case"],
            ["alternate", "upper", "lower"],
            ["toggle", "case"],
            ["camel", "alternate"],
        ],
    6:  [
            ["binary", "decimal"],
            ["binary", "convert"],
            ["bin", "dec"],
            ["base", "2", "decimal"],
            ["binary", "number"],
        ],
    7:  [
            ["ascii", "sum"],
            ["sum", "ascii"],
            ["ascii", "value"],
            ["ascii", "total"],
            ["ascii", "add"],
        ],
    8:  [
            ["fizzbuzz"],
            ["fizz", "buzz"],
            ["fizz buzz"],
        ],
    9:  [
            ["reverse", "vowel"],
            ["vowel", "reverse"],
            ["flip", "vowel"],
            ["vowel", "swap"],
        ],
    10: [
            ["caesar"],
            ["caesar", "cipher"],
            ["caesar", "shift"],
            ["shift", "cipher"],
            ["letter", "shift"],
        ],
    11: [
            ["pig", "latin"],
            ["piglatin"],
            ["pig latin"],
        ],
    12: [
            ["anagram", "sort"],
            ["sort", "letter"],
            ["alphabetical", "sort"],
            ["sort", "anagram"],
            ["letter", "sort"],
            ["anagram"],
        ],
}

HINTS = {
    1:  "something happens to the consonants in your input",
    2:  "try inputting numbers with multiple digits",
    3:  "probe 'hello' and 'world' separately",
    4:  "try sentences with different number of words",
    5:  "probe 'hello' — notice the pattern in upper and lower",
    6:  "try '1010' and '1111' — think in powers of 2",
    7:  "every character contributes a number — computers know this",
    8:  "try numbers like 3, 5, 15 — look for patterns in the output",
    9:  "probe 'hello' — only certain letters seem to move",
    10: "input needs two parts — probe 'abc,1' and 'abc,2'",
    11: "words get rearranged — probe single words first",
    12: "probe 'cat' and 'act' — notice anything about the output",
}

def get_challenge(chal_id):
    try:
        return CHALLENGES[chal_id - 1]
    except IndexError:
        return None