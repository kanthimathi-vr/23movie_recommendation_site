from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

movies = [
    {
        'id': 1,
        'title': 'Inception',
        'genre': 'Sci-Fi',
        'poster': 'posters/inception.jpg',
        'description': 'A mind-bending thriller by Christopher Nolan.'
    },
    {
        'id': 2,
        'title': 'Interstellar',
        'genre': 'Sci-Fi',
        'poster': 'posters/interstellar.jpg',
        'description': 'Exploring space and time with heart.'
    },
    {
        'id': 3,
        'title': 'The Matrix',
        'genre': 'Action',
        'poster': 'posters/matrix.jpg',
        'description': 'What is real? Enter the Matrix.'
    }
]

recommendations = {
    1: [],
    2: [],
    3: []
}

@app.route('/')
def home():
    genre_filter = request.args.get('genre')
    filtered_movies = [m for m in movies if m['genre'] == genre_filter] if genre_filter else movies
    genres = sorted(set(m['genre'] for m in movies))
    return render_template('home.html', movies=filtered_movies, genres=genres, selected_genre=genre_filter)

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        rec = request.form.get('recommendation')
        if rec:
            recommendations[movie_id].append(rec)
        return redirect(url_for('movie_detail', movie_id=movie_id))

    recs = recommendations.get(movie_id, [])
    return render_template('movie_detail.html', movie=movie, recs=recs)


if __name__ == '__main__':
    app.run(debug=True)