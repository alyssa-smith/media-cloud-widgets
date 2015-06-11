import urllib2, json, numpy as np, matplotlib.pyplot as plt, random, matplotlib, mediacloud
from bs4 import BeautifulSoup
keywords = ['caitlyn_jenner','obama', 'andrew_solomon', 'john_mccain', 'hillary_clinton', 'william_gibson', 'boston', 'pinnipeds']
#keywords = ['obama']
api_key = 'your api key here'
mc = mediacloud.api.MediaCloud(api_key)
for keyword in keywords:
    try:
        url='https://api.mediacloud.org/api/v2/wc/list?q=' + keyword + '&media_sets_id=1&key=' + api_key
        print url
        
        content = urllib2.urlopen(url)
        freq2 = json.loads(content.read())
        print keyword
        freq = mc.wordCount('('+keyword+')')
        total = np.sum([float(i['count']) for i in freq])
        entropy = np.sum([-(float(i['count'])/total)*np.log2(float(i['count'])/total) for i in freq])
        print freq == freq2
        print 
        print 'from API'
        print freq2[0:10]
        print
        print
        print 'from client'
        print freq[0:10]
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
    except:
        print freq