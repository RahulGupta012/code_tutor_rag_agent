import pandas as pd


def load_data(
    questions_path: str,
    answers_path: str
):
    questions = pd.read_csv(questions_path)
    answers = pd.read_csv(answers_path)

    return questions, answers


def select_best_answers(
    answers: pd.DataFrame
) -> pd.DataFrame:

    best_answers = (
        answers
        .sort_values("Score", ascending=False)
        .groupby("ParentId")
        .first()
        .reset_index()
    )

    return best_answers


def merge_questions_answers(
    questions: pd.DataFrame,
    best_answers: pd.DataFrame
) -> pd.DataFrame:

    merged = questions.merge(
        best_answers,
        left_on="Id",
        right_on="ParentId",
        suffixes=("_question", "_answer")
    )

    return merged