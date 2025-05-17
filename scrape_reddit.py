import praw
import pandas as pd

# Wynn's Credentials
client_id = 'DF9UIkqhDDBSlJGL18LxyA'
client_secret = 'EhPWd1nmJQNZZX0iQPLyDoiNnGCWSA'
user_agent = 'eco-anxiety-scraper by /u/WYNN_Z'

# Authenticate
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def scrape_by_keword(keyword, max_results):
    # Search across all subreddits and locate the posts and comments with the keyword
    posts = []
    for submission in reddit.subreddit("all").search(keyword, limit=max_results):
        posts.append({
            "date": submission.created_utc,
            "username": str(submission.author),
            "title": submission.title,
            "selftext": submission.selftext,
            "subreddit": submission.subreddit.display_name,
            "url": submission.url
        })
    # Convert to DataFrame and save
    df = pd.DataFrame(posts)
    df.to_csv(f"reddit_{keyword.replace(' ', '_')}_posts.csv", index=False)
    # Show success
    print(f"Scraped {len(df)} Reddit posts with keyword '{keyword}'")

def scrape_by_username(username, limit):
    # Get posts from a specified user
    posts = []
    for post in reddit.redditor(username).submissions.new(limit=limit):
        posts.append({
            "type": "submission",
            "date": post.created_utc,
            "subreddit": post.subreddit.display_name,
            "title": post.title,
            "content": post.selftext,
            "url": post.url
        })
    # Get comments
    for comment in reddit.redditor(username).comments.new(limit=limit):
        posts.append({
            "type": "comment",
            "date": comment.created_utc,
            "subreddit": comment.subreddit.display_name,
            "title": "",  # Comments don't have titles
            "content": comment.body,
            "url": f"https://www.reddit.com{comment.permalink}"
        })
    # Save to CSV
    df = pd.DataFrame(posts)
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df.to_csv(f"{username}_activity.csv", index=False)
    # Show success
    print(f"Saved {len(df)} items from user '{username}'")

def scrape_by_subreddit(subreddit_name, max_results):
    # Collect posts from a specific subreddit
    posts = []
    for submission in reddit.subreddit(subreddit_name).new(limit=max_results):
        posts.append({
            "date": submission.created_utc,
            "username": str(submission.author),
            "title": submission.title,
            "selftext": submission.selftext,
            "subreddit": subreddit_name,
            "url": submission.url
        })
    # Convert to DataFrame and save
    df = pd.DataFrame(posts)
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df.to_csv(f"subreddit_{subreddit_name}_posts.csv", index=False)
    print(f"Scraped {len(df)} posts from r/{subreddit_name}")

def scrape_by_keword_within_subreddit(subreddit_name, keyword, max_results):
    # Search across all subreddits and locate the posts and comments with the keyword
    posts = []
    for submission in reddit.subreddit(subreddit_name).search(keyword, limit=max_results):
        posts.append({
            "date": submission.created_utc,
            "username": str(submission.author),
            "title": submission.title,
            "selftext": submission.selftext,
            "subreddit": submission.subreddit.display_name,
            "url": submission.url
        })
    # Convert to DataFrame and save
    df = pd.DataFrame(posts)
    df.to_csv(f"reddit_{keyword.replace(' ', '_')}_posts.csv", index=False)
    # Show success
    print(f"Scraped {len(df)} Reddit posts with keyword '{keyword}' from subreddit r/{subreddit_name}")

scrape_by_keword_within_subreddit("TwoXChromosomes", "climate", 100)

# scrape_by_subreddit("climatechange", 5000)
# scrape_by_username("Molire", 50)
# scrape_by_keword("eco-anxiety", 50)