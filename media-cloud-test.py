import urllib2, json, numpy as np, matplotlib.pyplot as plt, random, matplotlib
from bs4 import BeautifulSoup
keywords = ['caitlyn_jenner','obama', 'andrew_solomon', 'john_mccain', 'hillary_clinton', 'william_gibson', 'boston', 'pinnipeds']
#keywords = ['caitlyn_jenner']
api_key = 'API KEY HERE'
for keyword in keywords:
    print keyword
    url='https://api.mediacloud.org/api/v2/wc/list?q=' + keyword + '&media_sets_id=1&key=' + api_key
    content = urllib2.urlopen(url)
    freq = json.loads(content.read())
    total = np.sum([float(i['count']) for i in freq])
    entropy = np.sum([-(float(i['count'])/total)*np.log2(float(i['count'])/total) for i in freq])
    print entropy
    print
    
    worddist = {i['term']: float(i['count']) for i in freq}
    wordcolors = {k: worddist[k] * 1.0/max(worddist.values()) for k in worddist.keys()}
    wordchoice = []
    for i in worddist.keys():
        stop = int(worddist[i])
        while stop > 0:
            wordchoice.append(i)
            stop -= 1
    colormap = []
    for i in range(100):
        col = []
        for j in range(10):
            term = random.choice(wordchoice)
            hsv = (1.0/10.0 * entropy, .75, wordcolors[term] )
            col.append(matplotlib.colors.hsv_to_rgb(hsv))
        colormap.append(col)
    #how dominated by most common words is the conversation? the darker the image, the more dominated by common words it is.
    plt.imshow(colormap)
    plt.title(keyword)
    plt.show()
    #grayscale s.t. weighted average of colors is middle-gray.  
    
    ##color saturation by word frequent-ness (see whether more frequent words dominate)