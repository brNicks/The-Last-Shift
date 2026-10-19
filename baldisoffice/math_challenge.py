class MathChallenge:
    """Desafio matematico usado pela avaliacao do The Last Shift.

    Mantem o progresso enquanto a interface e fechada com ESC.
    """

    def __init__(self):
        self.questions = [
            {"question": "8 + 7 = ?", "answers": ["14", "15", "16", "17"], "correct": 1},
            {"question": "12 - 5 = ?", "answers": ["5", "6", "7", "8"], "correct": 2},
            {"question": "6 x 4 = ?", "answers": ["20", "24", "26", "28"], "correct": 1},
            {"question": "36 / 6 = ?", "answers": ["5", "6", "7", "8"], "correct": 1},
            {"question": "9 + 6 x 2 = ?", "answers": ["21", "30", "24", "27"], "correct": 0},
        ]
        self.current_index = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.active = False
        self.finished = False

    def start(self):
        self.active = True
        self.finished = False

    def get_current_question(self):
        if self.finished or self.current_index >= len(self.questions):
            return None
        return self.questions[self.current_index]

    def get_progress(self):
        return self.current_index, len(self.questions)

    def answer(self, answer_index):
        if not self.active or self.finished:
            return False

        question = self.get_current_question()
        if question is None:
            return False

        correct = answer_index == question["correct"]

        if correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

        self.current_index += 1

        if self.current_index >= len(self.questions):
            self.finished = True
            self.active = False

        return correct
