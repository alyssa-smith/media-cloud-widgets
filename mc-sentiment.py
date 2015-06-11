import urllib2, numpy as np, mediacloud, itertools, nltk, datetime, matplotlib.pyplot as plt, ast
api_key = 'your api key here'
mc = mediacloud.api.AdminMediaCloud(api_key)
def train():
    counts = {}
    counts[-1] = {}
    counts[1] = {}
    totalpos = 0
    totalneg = 0
    with open('datasetSentences.txt') as f, open('sentiment_labels.txt') as g:
        sent = f.readlines()
        rate = g.readlines()
        for (s, r) in itertools.izip(sent, rate[1:]):
            prob = float(r.split('|')[1])
            if prob >= .45 and prob <= .55:
                pass
            else:
                if prob < .45:
                    cat = -1
                    totalneg += 1
                elif prob > .55:
                    cat = 1 
                    totalpos += 1
                for i in nltk.word_tokenize(s[5:]):
                    if i in counts[cat]:
                        pass
                    else:
                        counts[cat][i] = 0
                    counts[cat][i] += 1
    print counts
    negcounts = {key: np.log2(float(counts[-1][key])/float(totalneg)) for key in counts[-1]}
    poscounts = {key: np.log2(float(counts[1][key])/float(totalpos)) for key in counts[1]}
    allcounts = {-1: negcounts, 1: poscounts }
    return allcounts
#allcounts = train()
# with open('priors.txt', 'w') as f:
#     f.write(str(allcounts))
#     f.close()
with open('priors.txt') as f:
    allcounts = ast.literal_eval(f.readlines()[0])
    f.close()
def categorize(query, solr):  
    pos = 0  
    neg = 0
    for i in mc.sentenceList(query, solr_filter = solr)['response']['docs']:
        sent = i['sentence']
        negprior = 0.0
        posprior = 0.0
        for i in nltk.word_tokenize(sent):
            if i in allcounts[-1]:
                negprior += allcounts[-1][i]
            if i in allcounts[1]:
                posprior += allcounts[1][i]
        if posprior > negprior:
            #print sent
            #print 'pos', 2.0 ** posprior
            #print 'neg', 2.0 ** negprior
            #print
            pos += 1
        else:
            neg += 1
    print query
    print 'pos', pos
    print 'neg', neg
    print
    return float(pos)/float(pos + neg)


def categorize_over_time(query, s, e, d):
    #input format: s and e are tuples in the following format: (year, month, day, hour, minute, second)
    #d is the length of sampling interval in number of days 
    #query is the thing you want to track people's opinions of (use solr query syntax)
    ys = []
    xs = []
    labels = []
    def make_solr_time(dt):
        def reformat(i):
            if i < 10:
                return '0' + str(i)
            else:
                return str(i)
        f = str(dt.year) + '-' + reformat(dt.month) + '-' + reformat(dt.day) + 'T' + reformat(dt.hour) + ':' + reformat(dt.minute) + ':' + reformat(dt.second) + 'Z'
        #print f
        return f
        
        
    begin = datetime.datetime(s[0], s[1], s[2], s[3], s[4], s[5])
    delta = datetime.timedelta(days = d)
    end = begin + delta
    #print begin
    #print end
    beginsolr = make_solr_time(begin)
    endsolr = make_solr_time(end)
    endtime = datetime.datetime(e[0], e[1], e[2], e[3], e[4], e[5])
    numdays = 0
    while end < endtime:
        xs.append(numdays)
        numdays += d
        solr = '+publish_date:[' + beginsolr + ' TO ' + endsolr + ']'
        print solr
        print 
        pos = categorize(query, solr)
        beginsolr = endsolr
        end = end + delta
        endsolr = make_solr_time(end)
        #print beginsolr
        #print endsolr
        ys.append(pos)
        labels.append(beginsolr[0:10])
    #fig = figure()
    #ax = fig.add_subplot(111)
    plt.plot(xs, ys)
    for label, x, y in itertools.izip(labels, xs, ys):
        plt.annotate(label,xy = (x,y) )
    ##dashed red line at 0.5 (neutral sentiment I guess?)
    mid = 0.5 * np.ones(len(xs))
    plt.plot(xs, mid, 'r--')
    
    plt.axis([0, int(xs[-1])+10, 0, 1])
    plt.title(query)
    plt.show()
    #times should take form (year, )
                    
#categorize_over_time('Obama', (2015, 1, 1, 0, 0, 0), (2015, 6, 11, 9, 0, 0), 10)
categorize_over_time('hipster', (2015, 1, 1, 0, 0, 0), (2015, 6, 11, 9, 0, 0), 10)

