from privacy_policy_evaluator import helpers, wordscoring, paragraphing, topic_grouper, correlation
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Settings
files = [
    "../privacy_policy_evaluator/data/policies/google.txt",
    "../privacy_policy_evaluator/data/policies/reddit.txt",
    "../privacy_policy_evaluator/data/policies/twitter.txt",
    "../privacy_policy_evaluator/data/policies/ing.txt",
    "../privacy_policy_evaluator/data/policies/icloud.txt",
]

topics = ['location', 'address', 'email', 'information']

texts = []  # Read File
for file in files:
    texts.append(helpers.read_file(file))

grouped = []
for text in texts:
    # Paragraph the given text
    paragraphed = paragraphing.paragraph(text)
    # Do the grouping
    grouped.append(topic_grouper.group(paragraphed, topics, 0.1))

a = [
    grouped[0].get('location'),
    grouped[0].get('address'),
    grouped[0].get('email'),
    grouped[0].get('information'),
    grouped[1].get('location'),
    grouped[1].get('address'),
    grouped[1].get('email'),
    grouped[1].get('information'),
]

corr_og = correlation.correlation_matrix(a)
df = corr_og.loc[0:3, np.arange(4, 8)]

fig = plt.figure(figsize=(7, 5), dpi=200)
ax = fig.add_subplot(111)

nThresholds = 10
col = [(1, 1, 1), (242 / 255, 40 / 255, 38 / 255)]
cmap = colors.LinearSegmentedColormap.from_list(name='custom', colors=col)
cax = ax.matshow(df, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)


cbar = fig.colorbar(cax)
cbar.ax.set_ylabel('Score', rotation=270)
ax.set_xticklabels([''] + topics)
ax.set_yticklabels([''] + topics)
ax.xaxis.tick_top()
ax.set_title('Google')
plt.ylabel('Reddit')
plt.show()
