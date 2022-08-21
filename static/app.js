let guess = '';
let result = '';
let wordList = new Set();
let score = 0;

const $messages = $('#messages');
const $score = $('#score');
const $foundWords = $("ul");

class BoggleGame {

    constructor() {
        this.$foundWords = $("ul");
        this.word = "";
    }
    
    /** Calls API to check if word is valid and returns string of result */
    static async word_check(word) {
        const response = await axios.get(`/word-check?word=${word}`);
        return response.data['result'];
    }
}

function updateUI() {
    if (result === "ok") {
        if (wordList.has(guess)) {
            $messages.text("Already found that word!")
        } else {
            score += guess.length;
            $score.text(score);
            const newWord = `<li>${guess}</li>`;
            $foundWords.append(newWord);
            wordList.add(guess);
            console.log(`wordList: ${wordList}`);
        }
    } else if (result === 'not-on-board') {
        $messages.text("Word not on board!")
    } else if (result === 'not-a-word') {
        $messages.text("That's not a valid word!")
    }
}

$("form").on("submit", async function(evt) {
    evt.preventDefault();
    guess = $("#word_guess").val();
    result = await BoggleGame.word_check(guess);
    console.log(result);
    updateUI(result);
})