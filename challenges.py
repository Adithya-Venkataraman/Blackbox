ROUNDS = {
    1: [1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15],  # 15 easy  — 20 min
    2: [16, 17, 18, 19, 20, 21, 22, 23],                                 # 8 medium — 25 min
    3: [24, 25, 26, 27],                                                  # 4 hard   — 15 min
}

# ══ ROUND 1 — EASY ════════════════════════════════════════════════════════════

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
    try:
        return "even" if int(str(x).strip()) % 2 == 0 else "odd"
    except:
        return "invalid"

def uppercase(x):
    return str(x).upper()

def remove_spaces(x):
    return str(x).replace(" ", "")

def first_last_char(x):
    s = str(x).replace(" ", "")
    return s[0] + s[-1] if len(s) >= 2 else s

def double_chars(x):
    return ''.join(c * 2 for c in str(x))

def lowercase(x):
    return str(x).lower()

def count_digits(x):
    return sum(1 for c in str(x) if c.isdigit())

# ══ ROUND 2 — MEDIUM ══════════════════════════════════════════════════════════

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
    result = ''
    for c in str(x).lower():
        if c.isalpha():
            result += '*' if c in 'aeiou' else '#'
        else:
            result += c
    return result

def count_unique_chars(x):
    return len(set(str(x).lower().replace(" ", "")))

def word_length_sum(x):
    # input: any sentence → sum of the length of each word
    return sum(len(w) for w in str(x).split())

# ══ ROUND 3 — HARD ════════════════════════════════════════════════════════════

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

def rot13_reverse(x):
    # ROT13 the string, then reverse the result
    rot = ''
    for c in str(x):
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            rot += chr((ord(c) - base + 13) % 26 + base)
        else:
            rot += c
    return rot[::-1]

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
    double_chars,        # C13 — easy
    lowercase,           # C14 — easy
    count_digits,        # C15 — easy
    binary_to_decimal,   # C16 — medium
    ascii_sum,           # C17 — medium
    fizzbuzz,            # C18 — medium
    reverse_vowels,      # C19 — medium
    is_palindrome,       # C20 — medium
    vowel_consonant_swap,# C21 — medium
    count_unique_chars,  # C22 — medium
    word_length_sum,     # C23 — medium
    caesar,              # C24 — hard
    pig_latin,           # C25 — hard
    anagram_sort,        # C26 — hard
    rot13_reverse,       # C27 — hard
]

ANSWERS = {
    1:  "count vowels",
    2:  "reverse string",
    3:  "count characters",
    4:  "count words",
    5:  "title case",
    6:  "sum of digits",
    7:  "count consonants",
    8:  "repeat string",
    9:  "even or odd",
    10: "uppercase",
    11: "remove spaces",
    12: "first and last character",
    13: "double characters",
    14: "lowercase",
    15: "count digits",
    16: "binary to decimal",
    17: "sum of ascii values",
    18: "fizzbuzz",
    19: "reverse vowels",
    20: "palindrome check",
    21: "vowel consonant swap",
    22: "count unique characters",
    23: "word length sum",
    24: "caesar cipher",
    25: "pig latin",
    26: "anagram sort",
    27: "rot13 reverse",
}

ANSWER_KEYWORDS = {
    # ── EASY (broad, forgiving) ───────────────────────────────────────────────
    1:  [["vowel","count"],["count","vowel"],["number","vowel"],["no","vowel"]],
    2:  [["reverse","string"],["reverse","character"],["flip","string"],["string","reverse"],
         ["reverse","word"],["word","reverse"],["reversed"],["backwards"],["reverse"]],
    3:  [["count","character"],["character","count"],["char","count"],["count","char"]],
    4:  [["count","word"],["word","count"],["number","word"],["no","word"]],
    5:  [["title","case"],["capitalize","word"],["word","capitalize"],
         ["first","letter","upper"],["first","letter","capital"],
         ["first","character","upper"],["first","character","capital"],
         ["each","word","capital"],["each","word","upper"],["word","upper"],["word","capital"]],
    6:  [["sum","digit"],["digit","sum"],["add","digit"],["total","digit"]],
    7:  [["count","consonant"],["consonant","count"],["number","consonant"],["no","consonant"]],
    8:  [["repeat","string"],["string","repeat"],["duplicate","string"],["repeat"]],
    9:  [["even","odd"],["odd","even"],["even or odd"],["parity"]],
    10: [["uppercase"],["upper","case"],["all","upper"],["caps"]],
    11: [["remove","space"],["strip","space"],["no","space"],["space","remove"]],
    12: [["first","last"],["first","last","char"],["boundary","char"]],
    13: [["double","char"],["double","character"],["each","char","twice"],["double","letter"]],
    14: [["lowercase"],["lower","case"],["all","lower"],["small","case"]],
    15: [["count","digit"],["digit","count"],["number","digit"],["no","digit"]],

    # ── MEDIUM (tighter — must be specific) ───────────────────────────────────
    16: [["binary","decimal"],["binary","convert"],["base","2","decimal"]],
    17: [["ascii","sum"],["sum","ascii"],["ascii","value","sum"]],
    18: [["fizzbuzz"],["fizz","buzz"]],
    19: [["reverse","vowel"],["vowel","reverse"]],
    20: [["palindrome"],["palindrome","check"]],
    21: [["vowel","consonant","swap"],["vowel","consonant","symbol"]],
    22: [["unique","char"],["count","unique","char"],["distinct","char"]],
    23: [["word","length","sum"],["sum","word","length"],["total","word","length"]],

    # ── HARD (very tight — must name the concept) ─────────────────────────────
    24: [["caesar"],["caesar","cipher"],["caesar","shift"]],
    25: [["pig","latin"],["pig latin"]],
    26: [["anagram","sort"],["sort","letter","alphabetical"],["anagram"]],
    27: [["rot13","reverse"],["rot","13","reverse"],["rot13","reversed"],
         ["reverse","rot13"],["rot 13","revers"]],
}

HINTS = {
    # Easy — no hints
    # Medium — only for genuinely tricky ones
    18: "try inputs 3, 5, and 15 — certain words appear at multiples",
    19: "probe 'hello' carefully — only certain letters change position",
    21: "probe 'hello' — only two symbols appear in the output",
    23: "try 'hello world' vs 'hi' — compare with char count, it's different",
    # Hard — one directional nudge each
    24: "input needs two parts separated by a comma — try 'abc,1' then 'abc,2'",
    25: "probe one word at a time — parts of the word move with 'ay' at the end",
    26: "probe 'cat' then 'act' — compare the two outputs carefully",
    27: "two things happen to your input — probe 'abc' then 'abcd' and look closely",
}

def get_challenge(chal_id):
    try:
        return CHALLENGES[chal_id - 1]
    except IndexError:
        return None