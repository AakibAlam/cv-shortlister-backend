from sklearn.metrics.pairwise import cosine_similarity


def similarity_score(embedding1, embedding2):
    try:        
        score = cosine_similarity(embedding1, embedding2)[0][0]
        score = round(5 * score, 2)
        return score
    except Exception as e:
        return e