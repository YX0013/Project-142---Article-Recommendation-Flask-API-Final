from flask import Flask, jsonify, request

from storage import all_articles, liked_articles, disliked_articles, unviewed_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    return jsonify({
        "data": all_articles[0],
        "message": "success"
    }), 200

@app.route("/liked-article", methods = ["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message": "success"
    }), 200

@app.route("/disliked-article", methods = ["POST"])
def disliked_article():
    article = all_articles[0]
    disliked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message": "success"
    }), 200

@app.route("/unviewed-article", methods = ["POST"])
def unviewed_article():
    article = all_articles[0]
    unviewed_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message": "success"
    }), 200

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "index": article[1],
            "timestamp": article[2],
            "eventType": article[3],
            "contentId": article[4],
            "authorPersonId": article[5],
            "authorSessionId": article[6],
            "authorUserAgent": article[7],
            "authorRegion": article[8],
            "authorCountry": article[9],
            "contentType": article[10],
            "url": article[11],
            "title": article[12],
            "lang": article[14],
            "total_events": article[15]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    print(all_recommended)
    article_data = []
    for recommended in all_recommended:
        _d = {
            "index": recommended[1],
            "timestamp": recommended[2],
            "eventType": recommended[3],
            "contentId": recommended[4],
            "authorPersonId": recommended[5],
            "authorSessionId": recommended[6],
            "authorUserAgent": recommended[7],
            "authorRegion": recommended[8],
            "authorCountry": recommended[9],
            "contentType": recommended[10],
            "url": recommended[11],
            "title": recommended[12],
            "lang": recommended[14],
            "total_events": recommended[15]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run(debug = True)