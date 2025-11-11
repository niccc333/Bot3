import collections

# --- Setup ---
with open("wordlist.txt") as f:
    all_words = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]


# --- Feedback Logic (Official Wordle Rules) ---
def get_feedback(guess: str, target: str) -> str:
    guess = guess.lower()
    target = target.lower()
    feedback = [''] * 5

    target_chars = list(target)
    # Greens first
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = 'g'
            target_chars[i] = None

    # Yellows and grays
    for i in range(5):
        if feedback[i] == '':
            if guess[i] in target_chars:
                feedback[i] = 'y'
                target_chars[target_chars.index(guess[i])] = None
            else:
                feedback[i] = '-'
    return ''.join(feedback)


# --- Word Filtering ---
def filter_words(possible_words, guess, feedback):
    return [w for w in possible_words if get_feedback(guess, w) == feedback]


# --- Guess Selection ---
def choose_next_guess(possible_words):
    return max(sorted(possible_words), key=lambda w: len(set(w)))


# --- Core Wordle Solver ---
def play_wordle(target_word, initial_guesses=None, verbose=True):
    if initial_guesses is None:
        initial_guesses = ["aurei", "shock"]

    possible_words = all_words.copy()
    attempt = 1

    def print_victory(cat_word, cat_attempts):
        # Multi-line ASCII cat message (properly escaped and formatted)
        print(f"""
            
　　　　　🌸＞---フ       _____________________________________
　　　　　| 　_　 _ l     |  YAY, you solved it in {cat_attempts} guesses! |
　 　　　／` ミ_w_ノ      |  {cat_word.upper()} was the correct word!      |
　　 　 /　　　  　|     <_____________________________________|
　　　 /　 ヽ　　 ﾉ
　 　 │　　|　| |
　／￣|　　 |　| |
　| (￣ヽ＿_ヽ_)__)
　＼二つ
""")
    # --- Initial guesses ---
    for guess in initial_guesses:
        feedback = get_feedback(guess, target_word)
        if verbose:
            print(f"Guess {attempt}: {guess.upper()}  →  Feedback: {feedback}")
        if feedback == "ggggg":
            print_victory(guess, attempt)
            return attempt
        possible_words = filter_words(possible_words, guess, feedback)
        if verbose:
            print(f"  → {len(possible_words)} possible words remain.")
        attempt += 1

    # --- Continue guessing automatically ---
    while possible_words:
        next_guess = choose_next_guess(possible_words)
        feedback = get_feedback(next_guess, target_word)
        if verbose:
            print(f"Guess {attempt}: {next_guess.upper()}  →  Feedback: {feedback}")
        if feedback == "ggggg":
            print_victory(next_guess, attempt)
            return attempt
        possible_words = filter_words(possible_words, next_guess, feedback)
        if verbose:
            print(f"  → {len(possible_words)} possible words remain.")
            if len(possible_words) <= 10:
                print("  Remaining:", ', '.join(w.upper() for w in possible_words))
        attempt += 1

    print("\n❌ No possible words remain — failed to solve today's Wordle.")
    return None


def test_multiple_words(target_words):
    results = []
    for word in target_words:
        print(f"\n=== Solving for: {word.upper()} ===")
        attempts = play_wordle(word, verbose=False)
        results.append((word, attempts))

    print("\n\n=== RESULTS ===")
    for word, tries in results:
        print(f"{word.upper()}: {tries if tries else 'Failed'} guesses")

    # --- Fix: define valid_results BEFORE doing any math ---
    valid_results = [t for _, t in results if t is not None]
    if not valid_results:
        print("\nNo words were solved — check your word list.")
        return

    # --- Compute averages and stats ---
    avg_all = sum(valid_results) / len(valid_results)
    above_five = [t for t in valid_results if t > 5]
    below_or_equal_five = [t for t in valid_results if t <= 5]
    avg_under_five = (
        sum(below_or_equal_five) / len(below_or_equal_five)
        if below_or_equal_five else None
    )
    Winrate = (len(below_or_equal_five) / len(valid_results)) * 100

    print("\n=== STATISTICS ===")
    print(f"Total words tested: {len(valid_results)}")
    print(f"\nTotal average guesses: {avg_all:.2f}")
    print(f"Games lost: {len(above_five)} / {len(valid_results)}")
    print(f"Winrate (≤5 guesses): {Winrate:.2f}%")
    if avg_under_five is not None:
        print(f"Average in won games(≤5 guesses): {avg_under_five:.2f}")
    else:
        print("✨ Average (under 5 guesses only): N/A — you suck")

   


# --- Interactive Input ---
if __name__ == "__main__":
    print("\n\n              ˖°❀⋆.ೃ࿔*:･===============·༻𐫱༺·==================･:*ೃ.⋆❀°˖\n                            Welcome to Wordle Solver!\n                 ˖°❀⋆.ೃ࿔*:･=================================･:*ೃ.⋆❀°˖")
    mode = input("Type '1' to test multiple words at once, or '2' to manually input today's word: ").strip()

    if mode == "1":
        try:
            with open("AnswerWords.txt") as f:
                targets = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]
            if not targets:
                print("❌ No valid 5-letter words found in AnswerWords.txt.")
            else:
                print(f"\n📘 Loaded {len(targets)} target words from AnswerWords.txt:")
                print(", ".join(targets))
                test_multiple_words(targets)
        except FileNotFoundError:
            print("❌ File 'AnswerWords.txt' not found! Please create it in the same folder as this script.")

    elif mode == "2":
        while True:
            word = input("\nEnter today's Wordle word (or 'q' to quit): ").strip().lower()
            if word == "q":
                break
            if len(word) != 5 or not word.isalpha():
                print("❌ Must be a 5-letter alphabetic word.")
                continue
            play_wordle(word)

    else:
        print("Invalid choice — exiting.")
