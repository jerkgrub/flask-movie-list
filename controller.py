from flask import Flask, render_template, session, request, redirect, url_for
app = Flask("__name__")
# session
app.secret_key = "flaskProject"
from movies import Movie, Review

# home
@app.route("/")
def index():
    movies = Movie.getall_movies()
    return render_template("index.html", allmovies=movies)

# new movie 
@app.route("/movie/new")
def newmovie():
    return render_template("newmovie.html")

# process new movie
@app.route("/process/new/movie", methods=['POST'])
def create_new_movie():
    movietitle = request.form['movietitle']
    if len(movietitle) < 3:
        return redirect("/")
    data = {
        "movietitle": movietitle
    }
    Movie.new_movie(data)
    return redirect("/")

# review movie
@app.route("/review/<id>")
def review(id):
    data = {
        "id": int(id)
    }
    movie = Movie.getOne(data)
    if not movie:
        return redirect("/")
    return render_template("review.html", moviex=movie)

# process new review
@app.route("/process/new/review", methods=['POST'])
def create_new_review():
    movie_id = request.form['movie_id']
    reviewer = request.form['reviewer']
    rating = request.form['rating']
    review = request.form['review']
    data = {
        "movie_id": movie_id,
        "reviewer": reviewer,
        "rating": rating,
        "review": review
    }
    Review.new_review(data)
    return redirect("/")

# read reviews
@app.route("/movie/<id>/reviews")
def read_reviews(id):
    data = {
        "movie_id": int(id)
    }
    movie = Movie.getOne({"id": id})
    reviews = Review.get_reviews_for_movie(data)
    return render_template("readreviews.html", movie=movie, reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True)
