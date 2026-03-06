from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():

    # load the cleaned csv file
    df = pd.read_csv('netflix_cleaned.csv')

    # get filter from URL parameter (default = 'All')
    filter_type = request.args.get('type', 'All')

    # apply filter if not All
    if filter_type != 'All':
        df = df[df['type'] == filter_type]

    # aggregation 1 — top 10 directors (exclude Unknown)
    top_directors = (df[df['director'] != 'Unknown']['director']
                    .value_counts()
                    .head(10)
                    .to_dict())

    # aggregation 2 — top 10 countries (exclude Unknown)
    top_countries = (df[df['country'] != 'Unknown']['country']
                    .value_counts()
                    .head(10)
                    .to_dict())

    # aggregation 3 — movie vs tv show count
    type_count = df['type'].value_counts().to_dict()

    # aggregation 4 — titles added per year
    top_years = (df['year_added']
                .value_counts()
                .sort_index()
                .to_dict())

    # pass all results + current filter to template
    return render_template('index.html',
                           top_directors=top_directors,
                           top_countries=top_countries,
                           type_count=type_count,
                           top_years=top_years,
                           filter_type=filter_type)

if __name__ == '__main__':
    app.run(debug=True)