import json
import os
import subprocess

class Article:
  def __init__(self,id, author, title):
    self.id = id
    self.author = author
    self.title = title

  def dump(self):
     print(self.id)
     print(self.title)
     print(self.author)


class Comment:
    def __init__(self, id, parent, text, by):
        self.id = id
        self.parent = parent
        self.text = text
        self.by = by

    def dump(self):
        print(id)
        print(parent)
        print(text)
        print(by)



ARTICLE_LINK="https://hacker-news.firebaseio.com/v0/item/"
ARTICLES_FILE="articles.txt"
COMMENTS_FILE="comments.txt"


articles = []
comments = []


# obtained by manually copying from https://hn.algolia.com/?dateRange=all&page=0&prefix=false&query=podman%20desktop&sort=byPopularity&type=story
HNEWS_PARENT_LINKS = [
"https://news.ycombinator.com/item?id=33536978",
"https://news.ycombinator.com/item?id=31055475",
"https://news.ycombinator.com/item?id=37216800",
"https://news.ycombinator.com/item?id=36046222",
"https://news.ycombinator.com/item?id=38133963",
"https://news.ycombinator.com/item?id=36723445",
"https://news.ycombinator.com/item?id=38709121",
"https://news.ycombinator.com/item?id=35296165",
"https://news.ycombinator.com/item?id=40800548",
"https://news.ycombinator.com/item?id=40284839",
"https://news.ycombinator.com/item?id=39728878",
"https://news.ycombinator.com/item?id=39973403",
"https://news.ycombinator.com/item?id=39718969",
"https://news.ycombinator.com/item?id=40297592",
"https://news.ycombinator.com/item?id=31665610",
"https://news.ycombinator.com/item?id=39724100",
"https://news.ycombinator.com/item?id=35290223",
"https://news.ycombinator.com/item?id=34536580",
"https://news.ycombinator.com/item?id=28390200",
"https://news.ycombinator.com/item?id=31383644",
"https://news.ycombinator.com/item?id=36048248",
"https://news.ycombinator.com/item?id=35613448",
"https://news.ycombinator.com/item?id=35571408",
"https://news.ycombinator.com/item?id=36070584",
"https://news.ycombinator.com/item?id=29474967",
"https://news.ycombinator.com/item?id=36134298",
"https://news.ycombinator.com/item?id=34979975",
"https://news.ycombinator.com/item?id=34804347",
"https://news.ycombinator.com/item?id=33019448",
"https://news.ycombinator.com/item?id=32885748",
"https://news.ycombinator.com/item?id=38878869",
"https://news.ycombinator.com/item?id=37713378",
"https://news.ycombinator.com/item?id=37179307",
"https://news.ycombinator.com/item?id=34845859",
"https://news.ycombinator.com/item?id=32737567",
"https://news.ycombinator.com/item?id=40289120",
"https://news.ycombinator.com/item?id=40351971",
"https://news.ycombinator.com/item?id=30763832",
"https://news.ycombinator.com/item?id=29815122"]

def get_hackernews_articles():
   #ret = []
   #ret.append("https://news.ycombinator.com/item?id=33536978")
   #ret.append("https://news.ycombinator.com/item?id=31055475")
   #return ret
   return HNEWS_PARENT_LINKS


def make_link(url):
   tokens = url.split("=")
   id = tokens[1]
   return ARTICLE_LINK + id + ".json"



def fetch_hackernews(link):
    print(link)
    try:
        output = subprocess.check_output(
            [
                "curl", link,
            ],
            text=True,
        )
        parsed_json = json.loads(output)
        return parsed_json

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")


def process_kid(kid):
    print("processing:" + str(kid))
    url = ARTICLE_LINK + str(kid) + ".json"
    cmnt = fetch_hackernews(url)
    if ("deleted" not in cmnt) and ("dead" not in cmnt):
        by = cmnt["by"]
        id = cmnt["id"]
        article = cmnt["parent"]
        txt = cmnt["text"]
        cmnt = Comment(id, article, txt, by)
        comments.append(cmnt)
        print("done processing:" + str(kid))
    



print("starting")
hn_articles = get_hackernews_articles()
for hna in hn_articles:
    retjson = fetch_hackernews(make_link(hna))
    if (("title" in retjson) and ("by" in retjson) and ("id" in retjson)): 
        title = retjson["title"]
        by = retjson["by"]
        id = retjson["id"]
        art = Article(id, by, title)
        articles.append(art)
    
    if ("kids" in retjson):
        kids = retjson["kids"]
        for kid in kids:
            process_kid(kid)

print ("There are " + str(len(articles)) + " articles")
print ("There are " + str(len(comments)) + " comments")

f_articles = open(ARTICLES_FILE, "w")
for article in articles:
    f_articles.write(str(article.id) + ":" + article.author + ":" + article.title + "\n")

f_articles.close()


f_comments = open(COMMENTS_FILE, "w")
for comment in comments:
    f_comments.write(str(comment.id) + ":" + str(comment.parent) + ":" + comment.by + ":" + comment.text + "\n")

f_comments.close()

# clean up html escape stuff
try:
    output = subprocess.check_output(
    [
        "sed", 's/&#x2F;/\//g', COMMENTS_FILE, "-i[bp]"
    ],
         text=True,
    )

    output = subprocess.check_output(
    [
        "sed", 's/&#x27;/\'/g', COMMENTS_FILE, "-i[bp2]"
    ],
         text=True,
    )

except:
    print("File cleanup failed")

print ("done")