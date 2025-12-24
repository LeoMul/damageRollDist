import numpy as np 
import scipy as sci
import matplotlib.pyplot as plt 

'''
Python module to look at / compare damage rolls for dnd spells, by 
    ----------------------------------------------------------
                    Leo Patrick Mulholland
                   leomulholland@hotmail.com
                    lmulholland25@qub.ac.uk 
          Scholar account: https://shorturl.at/L0kU9
    ----------------------------------------------------------
'''


class damageRollDist:
    def __init__(self,numrolls,dicesize):
        
        self.__n = numrolls 
        self.__k = dicesize
        
        self.numrolls = numrolls 
        self.dicesize = dicesize 

        self.__norm = self.__k ** -self.__n 
        
        self.outcomes = np.arange(self.__n,self.__n*self.__k+1,1,dtype=int)
        self.prob = np.zeros_like(self.outcomes,dtype=float)
        
        self.__n_possible_outcomes = len(self.outcomes)
        
        self.__middle = int(np.floor ( (self.__n_possible_outcomes + 1)/2 ) ) 

        
        self.__generateFormula()
        self.__generateStatistics()
        self.__getInterp()
        return None
    
    def __generateFormula(self):
        '''
        Adapted from: https://mathworld.wolfram.com/Dice.html 
        From J. V. Uspensky's textbook from 1937 also.
        '''
        
        for ii in range(0, self.__middle): 
            s = self.outcomes[ii]
        #for (ii,s) in enumerate(srange):
#        print(s,n,k,(s - n)/k)

            upperlim = int(np.floor( (s - self.__n)/self.__k ))
            sum = 0.0
            for j in range(0, upperlim + 1):
                c1 = sci.special.binom(self.__n,j)
                c2 = sci.special.binom(s-j*self.__k-1,self.__n-1) 
                sum += c1 * c2 * (-1) ** j 
            self.prob[ii] = sum
        self.prob *= self.__norm
        jj = 0
        for ii in range(self.__n_possible_outcomes-1,self.__middle-1,-1):
            self.prob[ii] = self.prob[jj]
            jj+=1 
        
        return None
    
    def __getInterp(self):
        self.interp = sci.interpolate.interp1d(self.outcomes,self.prob)
        return None
    
    def __generateStatistics(self):
        
        self.mean = np.sum ( self.outcomes * self.prob )
        self.var  = np.sum ( np.power(self.outcomes - self.mean ,2) * self.prob )
        self.std  = np.sqrt(self.var)
        return None
    
    def plotDist(self,dpi=150):
        
        fig,ax = plt.subplots(1,1,dpi = dpi)
        
        ax.plot(self.outcomes,self.prob,color = 'k')
        ax.set_xlabel('Damage')
        ax.set_ylabel('Probability of Damage')
        ax.set_title('Probability distribution of {}d{}'.format(self.__n,self.__k))
        
        yy = ax.get_ylim()[1]
        
        ax.plot( [self.mean,self.mean], [0,max(self.prob)] ,'k--')#,label = 'Mean'
                
        mu = self.mean 
        sigma = self.std

        color_3sigma = '#BDD7EE' # Lightest shade
        color_2sigma = '#92C5DE' # Medium shade
        color_1sigma = '#4B9CD3' # Darker shade
        plt.fill_between(self.outcomes, 0, self.prob, color=color_3sigma, alpha=0.5)
        plt.fill_between(self.outcomes, 0, self.prob, where=abs(self.outcomes - mu) <= 3*sigma, color=color_3sigma, alpha=0.5)
        plt.fill_between(self.outcomes, 0, self.prob, where=abs(self.outcomes - mu) <= 2*sigma, color=color_2sigma, alpha=0.7)
        plt.fill_between(self.outcomes, 0, self.prob, where=abs(self.outcomes - mu) <= 1*sigma, color=color_1sigma, alpha=0.9)

        ax.set_ylim([0,yy])
        ax.legend(loc = 'upper right')
        return ax,fig  