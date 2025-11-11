import collections

# --- Setup ---
# Load possible Wordle words (replace wordlist.txt with your list)
with open("wordlist.txt") as f:
    all_words = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]

def get_feedback(guess: str, target: str) -> str:
    """
    Return Wordle-style feedback comparing guess -> target.
    'g' = green (correct position)
    'y' = yellow (in word, wrong position)
    '-' = gray (not in word / no remaining occurrences)
    Implements the official Wordle logic: greens first, then yellows with counts.
    """
    guess = guess.lower()
    target = target.lower()
    feedback = [''] * 5

    # First pass: greens
    target_chars = list(target)
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = 'g'
            target_chars[i] = None  # consume that char

    # Second pass: yellows or grays
    for i in range(5):
        if feedback[i] == '':
            if guess[i] in target_chars:
                feedback[i] = 'y'
                # remove first occurrence from target_chars
                idx = target_chars.index(guess[i])
                target_chars[idx] = None
            else:
                feedback[i] = '-'

    return ''.join(feedback)

def filter_words(possible_words, guess, feedback):
    """
    Keep only candidate words that WOULD produce the same feedback when guessed.
    This is the most reliable way to filter (handles duplicates correctly).
    """
    return [w for w in possible_words if get_feedback(guess, w) == feedback]

def choose_next_guess(possible_words):
    """
    Choose the next guess from possible_words.
    Current heuristic: maximize number of distinct letters; tie-break alphabetically.
    You can swap in other heuristics if you like.
    """
    return max(sorted(possible_words), key=lambda w: len(set(w)))

def play_wordle(target_word, initial_guesses=None, verbose=True):
    """
    Play automatically until solved or no possibilities remain.
    target_word: the true target (simulator mode).
    initial_guesses: list of fixed guesses to play first (defaults to ["aurei","monks"]).
    """
    if initial_guesses is None:
        initial_guesses = ["aurei", "shock"]

    possible_words = all_words.copy()
    attempt = 1

    # Play initial fixed guesses
    for guess in initial_guesses:
        if guess not in all_words:
            if verbose:
                print(f"Warning: initial guess '{guess}' not in wordlist; still using it.")
        feedback = get_feedback(guess, target_word)
        if verbose:
            print(f"Guess {attempt}: {guess.upper()}  →  Feedback: {feedback}")
        if feedback == "ggggg":
            if verbose:
                print(f"\n----------------------------------------------------\n ;p Solved in {attempt} guesses! ({next_guess.upper()})\n----------------------------------------------------\n")
            return attempt
        possible_words = filter_words(possible_words, guess, feedback)
        if verbose:
            print(f"  → {len(possible_words)} possible words remain.")
        attempt += 1

    # Continue guessing automatically
    while possible_words:
        next_guess = choose_next_guess(possible_words)
        feedback = get_feedback(next_guess, target_word)
        if verbose:
            print(f"Guess {attempt}: {next_guess.upper()}  →  Feedback: {feedback}")
        if feedback == "ggggg":
            if verbose:
                print(f"\n----------------------------------------------------\n ;p Solved in {attempt} guesses! ({next_guess.upper()})\n----------------------------------------------------\n")
            return attempt
        possible_words = filter_words(possible_words, next_guess, feedback)
        if verbose:
            print(f"  → {len(possible_words)} possible words remain.")
            if len(possible_words) <= 10:
                print("  Remaining:", ', '.join(w.upper() for w in possible_words))
        attempt += 1

    if verbose:
        print("\n ;( No possible words remain — failed to solve today's wordle.")
    return None

# --- Example runs ---
if __name__ == "__main__":
    # Replace with whichever target you want to simulate
    play_wordle("wryly")
  
