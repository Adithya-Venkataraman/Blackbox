ROUNDS = {
    1: [1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12],  # 12 easy  — 20 min
    2: [13, 14, 15, 16, 17, 18, 19],                        # 7 medium — 20 min
    3: [20, 21, 22],                                         # 3 hard   — 20 min
}

# ══ ROUND 1 — EASY (12 questions, ~1 min each) ════════════════════════════════

def vowel_count(x):
    return sum(1 for c in str(x).lower() if c in 'aeiou')

def reverse_string(x):
    return str(x)[::-1]

def char_count(x):
    return len(str(x).replace(" ", ""))

def word_count(x):
    return len(str(x).split())

def title_case(x):
    return " ".join(w.capitalize() for w in str(x).split())

def sum_digits(x):
    return sum(int(d) for d in str(x) if d.isdigit())

def count_consonants(x):
    return sum(1 for c in str(x).lower() if c.isalpha() and c not in 'aeiou')

def repeat_string(x):
    # input: "hello,3" → "hellohellohello"
    try:
        text, n = str(x).rsplit(",", 1)
        return text.strip() * int(n.strip())
    except:
        return "invalid"

def is_even_odd(x):
    # input: any integer → "even" or "odd"
    try:
        return "even" if int(str(x).strip()) % 2 == 0 else "odd"
    except:
        return "invalid"

def uppercase(x):
    return str(x).upper()

def remove_spaces(x):
    return str(x).replace(" ", "")

def first_last_char(x):
    # input: any word → first and last character concatenated
    s = str(x).replace(" ", "")
    return s[0] + s[-1] if len(s) >= 2 else s

# ══ ROUND 2 — MEDIUM (7 questions, ~2-3 min each) ════════════════════════════

def binary_to_decimal(x):
    try:
        return int(str(x).strip(), 2)
    except:
        return "invalid"

def ascii_sum(x):
    return sum(ord(c) for c in str(x))

def fizzbuzz(x):
    try:
        n = int(str(x).strip())
        if n < 1: return "invalid"
        result = []
        for i in range(1, n + 1):
            if i % 15 == 0:   result.append("FizzBuzz")
            elif i % 3 == 0:  result.append("Fizz")
            elif i % 5 == 0:  result.append("Buzz")
            else:              result.append(str(i))
        return " ".join(result)
    except:
        return "invalid"

def reverse_vowels(x):
    s = list(str(x))
    vowels = "aeiouAEIOU"
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and s[i] not in vowels: i += 1
        while i < j and s[j] not in vowels: j -= 1
        if i < j:
            s[i], s[j] = s[j], s[i]
            i += 1; j -= 1
    return "".join(s)

def is_palindrome(x):
    s = str(x).lower().replace(" ", "")
    return "yes" if s == s[::-1] else "no"

def vowel_consonant_swap(x):
    # vowels → *, consonants → #
    result = ''
    for c in str(x).lower():
        if c.isalpha():
            result += '*' if c in 'aeiou' else '#'
        else:
            result += c
    return result

def count_unique_chars(x):
    return len(set(str(x).lower().replace(" ", "")))

# ══ ROUND 3 — HARD (3 questions, ~5-6 min each) ══════════════════════════════

def caesar(x):
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
    words = str(x).lower().split()
    result = []
    for w in words:
        if not w: continue
        vowels = 'aeiou'
        if w[0] in vowels:
            result.append(w + 'yay')
        else:
            i = 0
            while i < len(w) and w[i] not in vowels: i += 1
            result.append(w[i:] + w[:i] + 'ay')
    return ' '.join(result)

def anagram_sort(x):
    words = str(x).lower().split()
    if not words:
        return ''.join(sorted(str(x).lower().replace(" ","")))
    return ' '.join(''.join(sorted(w)) for w in words)

# ══ REGISTRY ══════════════════════════════════════════════════════════════════

CHALLENGES = [
    vowel_count,         # C1  — easy
    reverse_string,      # C2  — easy
    char_count,          # C3  — easy
    word_count,          # C4  — easy
    title_case,          # C5  — easy
    sum_digits,          # C6  — easy
    count_consonants,    # C7  — easy
    repeat_string,       # C8  — easy
    is_even_odd,         # C9  — easy
    uppercase,           # C10 — easy
    remove_spaces,       # C11 — easy
    first_last_char,     # C12 — easy
    binary_to_decimal,   # C13 — medium
    ascii_sum,           # C14 — medium
    fizzbuzz,            # C15 — medium
    reverse_vowels,      # C16 — medium
    is_palindrome,       # C17 — medium
    vowel_consonant_swap,# C18 — medium
    count_unique_chars,  # C19 — medium
    caesar,              # C20 — hard
    pig_latin,           # C21 — hard
    anagram_sort,        # C22 — hard
]

ANSWERS = {
    1:  "count vowels",
    2:  "reverse string",
    3:  "count characters",
    4:  "count words",
    5:  "upper case",
    6:  "sum of digits",
    7:  "count consonants",
    8:  "repeat string",
    9:  "even or odd",
    10: "uppercase",
    11: "remove spaces",
    12: "first and last character",
    13: "binary to decimal",
    14: "sum of ascii values",
    15: "fizzbuzz",
    16: "reverse vowels",
    17: "palindrome check",
    18: "vowel consonant swap",
    19: "count unique characters",
    20: "caesar cipher",
    21: "pig latin",
    22: "anagram sort",
}

ANSWER_KEYWORDS = {
    1:  [["vowel","count"],["count","vowel"],["number","vowel"],["no","vowel"]],
    2:  [["reverse","string"],["reverse","character"],["flip","string"],["string","reverse"]],
    3:  [["count","character"],["character","count"],["char","count"],["length","no space"],["count","char"]],
    4:  [["count","word"],["word","count"],["number","word"],["no","word"]],
    5:  [["title","case"],["capitalize","word"],["title case"],["word","capitalize"],["capital","uppercase"]],
    6:  [["sum","digit"],["digit","sum"],["add","digit"],["total","digit"]],
    7:  [["count","consonant"],["consonant","count"],["number","consonant"],["no","consonant"]],
    8:  [["repeat","string"],["string","repeat"],["duplicate","string"],["repeat"]],
    9:  [["even","odd"],["odd","even"],["even or odd"],["parity"]],
    10: [["uppercase"],["upper","case"],["all","upper"],["caps"],["capital"]],
    11: [["remove","space"],["strip","space"],["no","space"],["space","remove"]],
    12: [["first","last"],["first","last","char"],["first last"],["boundary","char"]],
    13: [["binary","decimal"],["bin","dec"],["binary","convert"],["base","2"]],
    14: [["ascii","sum"],["sum","ascii"],["ascii","value"],["ascii","total"]],
    15: [["fizzbuzz"],["fizz","buzz"],["fizz buzz"]],
    16: [["reverse","vowel"],["vowel","reverse"],["flip","vowel"],["vowel","swap"]],
    17: [["palindrome"],["reads","same"],["same","backwards"],["palindrome","check"]],
    18: [["vowel","consonant","swap"],["vowel","symbol"],["mask","vowel"],["replace","vowel"]],
    19: [["unique","char"],["count","unique"],["distinct","char"],["unique","letter"]],
    20: [
            ["caesar"],
            ["caesar","cipher"],
            ["shift","cipher"],
            ["letter","shift"],
            ["caesar","shift"],
            ["shift","letter"],
            ["rotate","letter"],
            ["rotate","alphabet"],
            ["shift","alphabet"],
            ["encrypt","shift"],
            ["shift","position"],
            ["alphabet","shift"],
            ["character","shift"],
            ["encode","shift"],
            ["shifting"],
            ["letter","rotation"],
            ["alphabet","rotation"],
            ["shift","by"],
            ["move","letter"],
            ["letter","moved"],
        ],
    21: [["pig","latin"],["piglatin"],["pig latin"]],
    22: [["anagram"],["anagram","sort"],["sort","letter"],["alphabetical","sort"],["letter","sort"]],
}

# Hints: minimal — only shown when explicitly requested. Easy=vague, Medium=slightly more, Hard=directional.
HINTS = {
    # Easy — very vague, just a nudge
    1:  "think about specific letters in the alphabet",
    2:  "what if you read it backwards",
    3:  "spaces don't count",
    4:  "try inputs with different numbers of words",
    5:  "look at the first letter of each word",
    6:  "try a number like 123",
    7:  "not vowels",
    8:  "try input with a comma",
    9:  "try 4 and then 7",
    10: "look at the case of each letter",
    11: "what's missing from the output",
    12: "look at the very start and end",
    # Medium — slightly more revealing
    13: "think in powers of 2",
    14: "every character has a code number",
    15: "try 3, 5, and 15 as inputs",
    16: "only certain letters move",
    17: "try 'racecar' vs 'hello'",
    18: "two different symbols appear — what do they represent",
    19: "probe the same letter multiple times",
    # Hard — directional only
    20: "you need two parts in your input — separated by a comma",
    21: "probe a single word — where do parts of it go",
    22: "probe 'cat' then 'act' — compare outputs",
}

def get_challenge(chal_id):
    try:
        return CHALLENGES[chal_id - 1]
    except IndexError:
        return None