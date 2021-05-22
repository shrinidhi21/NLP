from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentiment_score(sent):
    sent_obj = SentimentIntensityAnalyzer()
    sent_dict = sent_obj.polarity_scores(sent)

    print(sent_dict)
    sent_emotion = max(sent_dict, key=sent_dict.get)
    print("The sentence is rated ", sent_dict[sent_emotion] * 100, "%", sent_emotion)

    print("Sentence Overall Rated As", end=" ")

    if sent_dict['compound'] >= 0.05:
        print("Positive")

    elif sent_dict['compound'] <= - 0.05:
        print("Negative")

    else:
        print("Neutral")


if __name__ == '__main__':
    sentence = "I am excited"
    sentiment_score(sentence)
