import praw
from praw.models import MoreComments

reddit = praw.Reddit(client_id='qeEY-gzqmsBETQ', client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY', user_agent='Telvin Zhong')

submission = reddit.submission(url="https://www.reddit.com/r/AskReddit/comments/httuy9/what_is_a_lot_unhealthier_than_most_people_think/")
submission.comments.replace_more(limit = 0)

dic = {}
banned = ["\n", ".", "'", ")", "(", "*", "?", "!", "’"]
common = ["and", "the", "that", "you", "but"]

def clean(word):

    res = []
    for i in word:
        if i in banned:
            continue
        elif i.isalnum:
            res.append(i.lower())
    return "".join(res)

# if isinstance(top_level_comment, MoreComments):      Alternative way to skip more comments
for comment in submission.comments.list():
    com = str(comment.body).split(" ")
    for word in com:
        word = clean(word)
        if len(word) >= 4 and word not in common:
            dic[word] = dic.get(word, 0) + 1

# print(dic)
trimming = []
for key, val in dic.items():
    trimming.append([key, val])
trimming.sort(key = lambda x: x[1], reverse=True)
print(trimming)
# for i in range(len(trimming) // 4)):
#     dic.delitem(trimming[i])
    