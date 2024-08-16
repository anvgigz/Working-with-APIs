import requests
import plotly.express as px

# Make an API call and store the response.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
submission_ids = r.json()

# Process information about each submission.
submission_dicts = []
for submission_id in submission_ids[:30]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    response_dict = r.json()

    # Check if the 'descendants' key exists before accessing it.
    if 'descendants' in response_dict:
        comments = response_dict['descendants']
    else:
        comments = 0

    # Build a dictionary for each article.
    submission_dict = {
        'title': response_dict.get('title', 'N/A'),
        'hn_link': f"https://news.ycombinator.com/item?pid={submission_id}",
        'comments': comments,
    }
    submission_dicts.append(submission_dict)

# Filter out promotional posts (skip KeyError)
filtered_submission_dicts = [s for s in submission_dicts if s['title'] != 'N/A']

# Create the visualization
fig = px.bar(
    filtered_submission_dicts,
    x='hn_link',
    y='comments',
    text='title',
    title="Most Active Discussions on Hacker News",
    labels={'hn_link': 'Discussion Link', 'comments': 'Number of Comments'},
    hover_name='title',
)

fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    xaxis_tickangle=-45,
    xaxis_tickfont=dict(size=10),
)

fig.show()
