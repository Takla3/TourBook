import numpy as np
import requests
from django.conf import settings


def get_sentiment_scores(comments):
    """
    Calculates sentiment scores for a list of comments using the Hugging Face Inference API.

    Args:
        comments (list): A list of strings representing comments.

    Returns:
        str: A percentage representation of the average sentiment score.
    """
    try:
        headers = {
            'Authorization': f'Bearer {settings.HUGGING_FACE_API_TOKEN}',
            'Content-Type': 'application/json',
        }

        if not comments:
            return "0.00%"

        # Prepare the payload
        payload = {'inputs': comments}

        # Send the request to the API
        response = requests.post(
            settings.MODEL_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        # Get the results
        sentiments = response.json()
        scores = []

        for sentiment in sentiments:
            label = sentiment[0]['label']
            score = sentiment[0]['score']
            # Convert 'LABEL_1' (positive) and 'LABEL_0' (negative) into a compound score similar to [-1, 1]
            compound_score = 0
            if label == 'positive':
                compound_score = score
            elif label == 'negative':
                compound_score = -score
            scores.append(compound_score)

        # Calculate the average and convert to percentage
        average_score = np.mean(scores)
        result = convert_to_percentage_value(average_score)
        return f"{round(result, 2)}%"

    except requests.exceptions.RequestException as e:
        return f"API request error: {e}"
    except ImportError:
        return "Numpy is not available in the environment. Please install Numpy to use this function."


def convert_to_percentage_value(score):
    """
    Converts the average sentiment score to a percentage value.

    Args:
        score (float): The average sentiment score.

    Returns:
        float: The percentage representation of the average sentiment score.
    """
    # Example conversion, modify according to your needs
    return (score + 1) * 50


def get_organizer_tours_rating(tours):
    """
        Get sentiment scores for organizer tours.

        Args:
            tours (QuerySet): A queryset of tours.

        Returns:
            str: The sentiment score percentage.
        """
    comments = [
        comment.comment for tour in tours for comment in tour.tour_comments.all()]
    # print(comments)
    return get_sentiment_scores(comments)
