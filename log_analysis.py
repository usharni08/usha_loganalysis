#!/usr/bin/env python3

import psycopg2

DBNAME = "news"

request_1 = "What are the most popular three articles of all time?"

query_1 = ("SELECT title, COUNT(1) AS popular_articles\n"
           "FROM articles a \n"
           "  JOIN log l\n"
           "    ON a.slug = SUBSTRING(l.path, 10)\n"
           "    GROUP BY title \n"
           "    ORDER BY popular_articles DESC \n"
           "    LIMIT 3;")

request_2 = "Who are the most popular article authors of all time?"

query_2 = ("SELECT au.name, count(1) AS popular_art_auth \n"
           "    FROM articles a \n"
           "    JOIN authors au\n"
           "      ON a.author = au.id \n"
           "      JOIN log l \n"
           "      ON a.slug = SUBSTRING(l.path, 10)\n"
           "      WHERE l.status LIKE '200 OK'\n"
           "      GROUP BY au.name \n"
           "      ORDER BY popular_art_auth DESC;")

request_3 = "On which days more than 1% of the requests led to error?"

query_3 = ("SELECT ROUND((cnt*100.0)/visitors, 3) AS\n"
           "        result, TO_CHAR(errortime, 'Mon DD, YYYY')\n"
           "        FROM errorcount_view ORDER BY result DESC LIMIT 1;")

# Connect to the database and feed query to extract results


def get_queryResults(sql_query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_query)
    results = c.fetchall()
    db.close()
    return results

result1 = get_queryResults(query_1)
result2 = get_queryResults(query_2)
result3 = get_queryResults(query_3)


# Create a function to print query results


def print_results(q_list):
    for i in range(len(q_list)):
        title = q_list[i][0]
        res = q_list[i][1]
        print("\t" + "%s - %d" % (title, res) + " views")
    print("\n")

print(request_1)
print_results(result1)
print(request_2)
print_results(result2)
print(request_3)
print("\t" + result3[0][1] + " - " + str(result3[0][0]) + "%")
