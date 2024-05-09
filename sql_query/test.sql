SELECT t.primary_title,
    t.premiered,
    r.rating,
    r.votes
FROM titles t
    JOIN ratings r ON t.title_id = r.title_id
WHERE r.rating >= { rating }
    AND t.genres LIKE "%{genre}%"
    AND r.votes >= 1000
    AND t.premiered >= 2000
    AND type = "movie";