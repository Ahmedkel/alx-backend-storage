-- SQL script that ranks country origins of bands, ordered by the number:
SELECT origin, nb_fans,
      RANK() OVER (ORDER BY nb_fans DESC) AS rank
FROM bands;