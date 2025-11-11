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


# --- Multi-word Tester ---
def test_multiple_words(target_words):
    results = []
    for word in target_words:
        print(f"\n=== Solving for: {word.upper()} ===")
        attempts = play_wordle(word, verbose=False)
        results.append((word, attempts))

    print("\n\n=== RESULTS ===")
    for word, tries in results:
        print(f"{word.upper()}: {tries if tries else 'Failed'} guesses")
     # Compute averages and counts
    avg_all = sum(valid_results) / len(valid_results)
    above_five = [t for t in valid_results if t > 5]
    avg_under_five = (
        sum(t for t in valid_results if t <= 5) / len([t for t in valid_results if t <= 5])
        if any(t <= 5 for t in valid_results)
        else None
    )

    print(f"\n📊 Average guesses (all): {avg_all:.2f}")
    print(f"⏱️  Words failed (>5 guesses): {len(above_five)} / {len(valid_results)}")
    if avg_under_five is not None:
        print(f"✨ Average (≤5 guesses only): {avg_under_five:.2f}")
    else:
        print("✨ Average (≤5 guesses only): N/A — all took more than 5 guesses")

    # Filter valid (solved) results
    valid_results = [t for _, t in results if t]
    if not valid_results:
        print("\nNo words were solved — check your word list.")
        return

   


# --- Interactive Input ---
if __name__ == "__main__":
    print("Welcome to Wordle Solver!\n")
    mode = input("Type '1' to test multiple words, or '2' to manually input today's word: ").strip()

    if mode == "1":
        print("\nEnter up to 10 target words (press Enter on a blank line to finish):")
        targets = []
        while len(targets) < 10:
            word = input(f"Word #{len(targets)+1}: ").strip().lower()
            if not word:
                break
            if len(word) != 5 or not word.isalpha():
                print("❌ Must be a 5-letter alphabetic word.")
                continue
            targets.append(word)
        test_multiple_words(targets)

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
