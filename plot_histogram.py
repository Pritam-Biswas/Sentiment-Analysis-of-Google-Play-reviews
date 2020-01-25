import gzip
import json
import timeit as t
import matplotlib.pyplot as plt
import pylab
import matplotlib
import numpy as np

def showdata(data,n):
    print [data[str(i)] for i in xrange(1,4)]

def set_figproperty(ax,xlabelstr,ylabelstr,figfont):

    ax.set_xlabel(xlabelstr,fontweight='bold')#
    ax.set_ylabel(ylabelstr,fontweight='bold')
    
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(figfont) 
    return ax

def main():

    font = {'weight' : 'bold'}                                                  
    matplotlib.rc('font', **font)

    filename = 'reviews_facebook_with_score.json'

    with open(filename,'r') as fin:
        data = json.load(fin)

    n = len(data)

#    showdata(data,n)

    rating = [ int(data[str(i)]["rating"])  for i in xrange(1,n+1)]
    textscore = [ round(float(data[str(i)]["text_score"]),2)  for i in range(1,n+1)]
    #print rating
    maxrating = max(rating)
    minrating = min(rating)

    fig = pylab.figure()
    ax = fig.add_subplot(111)
    fig.suptitle('Rating vs Count || FACEBOOK ', fontsize=20)

    bins = range(minrating,maxrating+1,1)
    
    print rating
    plt.hist(rating,bins)
    
    xlabelstr = 'rating'
    ylabelstr = 'count'
    figfont = 24

    ax = set_figproperty(ax,xlabelstr,ylabelstr,figfont)

    #pylab.tight_layout() 
    pylab.savefig('hist_rating.eps',)
    plt.show()

    minsenti = min(textscore)
    maxsenti = max(textscore)

    newmin = 1.0
    newmax = 5.0
    
    textscore = [(newmax-newmin)/(maxsenti-minsenti)*(v-minsenti)+newmin for v in textscore]


    fig = pylab.figure()
    ax = fig.add_subplot(111)
    fig.suptitle('Sentiment score vs Count || FACEBOOK ', fontsize=20)
    step = 1
    bins = list(np.arange(newmin,newmax+step,step))
    plt.hist(textscore,bins)
    
    xlabelstr = 'sentiment'
    ylabelstr = 'count'
    figfont = 24

    ax = set_figproperty(ax,xlabelstr,ylabelstr,figfont)

    pylab.tight_layout() 
    pylab.savefig('hist_sentiment_scaled.eps',)
    plt.show()
#    print rating

#    print "done"

if __name__=='__main__':
    main()
