from mysqlconnection import connecttoMysql

class Movie:
    def __init__(self, data):
        self.id = data['id']
        self.movietitle = data['movietitle']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # get all
    @classmethod
    def getall_movies(cls):
        query = """
        SELECT movies.*, IFNULL(ROUND(AVG(reviews.rating), 2), 0) AS avg_rating
        FROM movies
        LEFT JOIN reviews ON movies.id = reviews.movie_id
        GROUP BY movies.id;
        """
        results = connecttoMysql("market_db").query_db(query)
        movies = []
        for movie in results:
            movies.append({
                "id": movie['id'],
                "movietitle": movie['movietitle'],
                "avg_rating": movie['avg_rating'],
                "created_at": movie['created_at'],
                "updated_at": movie['updated_at']
            })
        return movies

    # new movie
    @classmethod
    def new_movie(cls, data):
        query = "INSERT INTO movies (movietitle) VALUES(%(movietitle)s)"
        return connecttoMysql("market_db").query_db(query, data)

    # get one
    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM movies WHERE id=%(id)s;"
        result = connecttoMysql("market_db").query_db(query, data)
        if len(result) < 1:
            return False
        else:
            return cls(result[0])

class Review:
    def __init__(self, data):
        self.id = data['id']
        self.movie_id = data['movie_id']
        self.reviewer = data['reviewer']
        self.rating = data['rating']
        self.review = data['review']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # new review
    @classmethod
    def new_review(cls, data):
        query = """
        INSERT INTO reviews (movie_id, reviewer, rating, review) 
        VALUES(%(movie_id)s, %(reviewer)s, %(rating)s, %(review)s)
        """
        return connecttoMysql("market_db").query_db(query, data)

    # get reviews for a movie
    @classmethod
    def get_reviews_for_movie(cls, data):
        query = "SELECT * FROM reviews WHERE movie_id = %(movie_id)s;"
        results = connecttoMysql("market_db").query_db(query, data)
        reviews = []
        for review in results:
            reviews.append(cls(review))
        return reviews
