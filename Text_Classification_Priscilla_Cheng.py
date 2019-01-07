import math
def clean_text(txt):
        """returns a list containing the words in txt after it has been
        “cleaned”;used when you need to process each word in a text individually, without having to worry about
        punctuation or special characters.
        """
        return txt.replace('.','').replace('.','').replace('?','').lower()

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   
    f = open(filename, 'w')      
    f.write(str(d))              
    f.close()                   

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    
    d_str = f.read()           
    f.close()

    d = dict(eval(d_str))      

    print("Inside the newly-read dictionary, d, we have:")
    print(d)
    
def stem(s):
        """accepts string; return stem/root of s exclude prefixes and suffixes"""
        special=['s']
        one_singular=['y','e','a']
        singular=['on','er','us','en','st']
        plural=['ie','ey','es']
        three_end=['ier','ing','dom','er','ism','ist','ion','ous','iou']
        four_end=['ible','able','ment','ness','ship','sion','tion','ance','ence','ious']
        two_prefix=['re','un','co','de']
        three_prefix=['pre','dis']
        if len(s)>=3 and s[-1] in special:
                if s[-3:-1] in plural:
                        return s[:-3]
                if s[-4:-1] in three_end:
                        return s[:-4]
                if len(s)>=5:
                        if s[-5:-1]in four_end:
                                return s[:-5]
                if s[:2] in two_prefix:
                        return s[2:]
                if s[:3] in three_prefix:
                        return s[3:]
                if s[-2:-1] in one_singular:
                        return s[:-2]

                else:
                        return s[:-1]
        if len(s)>=3:
                if s[:2] in two_prefix:
                        return s[2:]
                if s[:3] in three_prefix:
                        return s[3:]
                if s[-1] in one_singular:
                        return s[:-1]
                if s[-2:] in plural:
                        return s[:-2]
                if s[-3:] in three_end:
                        return s[:-3]
                if len(s)>=5:
                        if s[-4]in four_end:
                                return s[:-4] 
                else:
                        return s
        if s[-1]in one_singular:
                return s[:-1]
        if s[-2:] in singular:
                return s
        if s[-2:]in plural:
                return s
        else:
                return s


def compare_dictionaries(d1, d2):
        """ compute and return their log similarity score."""
        score=0
        count=0
        total=len(d1)
        for w in d2:
                count+=1
                if w in d1:
                        score+=math.log(d1[w]/total)
                        score*=count
                else:
                        score+=(0.5/total)
                        score*=count
        return score


class TextModel:
    def __init__(self, model_name):
        """model_name :string
            Attributes: name-string label for text model
                        words-dictionary that records # times each word appears in text
                        word_lengths-dictionary records # of times each word length appears

        """
        self.name=model_name
        self.words={}
        self.word_lengths={}
        self.stems={}
        self.sentence_lengths={}
        self.three_adjacent={}

    def max_adjacent(self):
        """helper to find the most frequent adjacent words in self.three_adjacent"""
        frequency=0
        sequence=''
        for a in self.three_adjacent:
                if self.three_adjacent[a]>frequency:
                        frequency=self.three_adjacent[a]
                        sequence=a
        if frequency==1:
                return 'There is no 3-word sequence used more than 1 time'
        else:
                return "'"+sequence+"'"+ ' used '+str(frequency)+' time(s)'
        
    def __repr__(self):
        """returns a string that includes the name of the model as well
        as the sizes of the dictionaries for each feature of the text
        """
        s = 'text model name: ' + str(self.name) + '\n'
        s += ' number of words: ' + str(len(self.words)) + '\n'
        s += ' number of word lengths: '+str(len(self.word_lengths))+'\n'
        s += ' number of stems: '+str(len(self.stems))+'\n'
        s += ' number of sentence lengths: '+str(len(self.sentence_lengths))+'\n'
        s += ' most Frequently used 3-word sequence: '+str(self.max_adjacent())
        return s


    def add_string(self,s):
        """adds a string of text s to the model by augmenting the
        feature dictionaries defined in the constructor. It should not
        explicitly return a value.
        """

        sentence=s.split('.?!')
        for sent in sentence:
           if len(sent) not in self.sentence_lengths:
                self.sentence_lengths[len(sent)]=1
           else:
                self.sentence_lengths[len(sent)]+=1
                
        word_list = clean_text(s).split()
        for w in word_list:
            if w not in self.words:
                self.words[w]=1
            else:
                self.words[w]+=1
            if len(w)not in self.word_lengths:
                self.word_lengths[len(w)]=1
            else:
                self.word_lengths[len(w)]+=1               
            if stem(w) not in self.stems:
                self.stems[stem(w)]=1
            else:
                self.stems[stem(w)]+=1
                
        for n in range(0,len(word_list)-2): 
           sequence=str(word_list[n])+' '+str(word_list[n+1])+' '+str(word_list[n+2])
           if sequence not in self.three_adjacent:
                self.three_adjacent[sequence]=1
           else:
                self.three_adjacent[sequence]+=1


                
                
    def add_file(self,filename):
        """adds all of the text in the file identified by filename to
        the model. It should not explicitly return a value.
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file=clean_text(f.read())
        self.add_string(file)



    def save_model(self):
        """saves the TextModel object self by writing its various feature
        dictionaries to files. There will be one file written for each
        feature dictionary. For now, you just need to handle the words and
        word_lengths dictionaries
        """
        dic1=self.name+'_'+'words'
        dic2=self.name+'_'+'word_lengths'
        dic3=self.name+'_'+'stems'
        dic4=self.name+'_'+'sentence_lengths'
        dic5=self.name+'_'+'three_adjacent'
        f = open(dic1, 'w')     
        f.write(str(self.words))
        f.close()
        f= open(dic2,'w')
        f.write(str(self.word_lengths)) 
        f.close()
        f = open(dic3, 'w')     
        f.write(str(self.stems))
        f.close()
        f = open(dic4, 'w')     
        f.write(str(self.sentence_lengths))
        f.close()
        f=open(dic5,'w')
        f.write(str(self.three_adjacent))
        f.close()

        
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object
        from their files and assigns them to the attributes of the called
        TextModel.
        """
        dic1=self.name+'_'+'words'
        dic2=self.name+'_'+'word_lengths'
        dic3=self.name+'_'+'stems'
        dic4=self.name+'_'+'sentence_lengths'
        dic5=self.name+'_'+'three_adjacent'
        f = open(dic1, 'r')    
        words = f.read()
        self.words=dict(eval(words))
        f.close()
        
        f=open(dic2,'r')
        word_lengths=f.read()
        self.word_lengths=dict(eval(word_lengths))
        f.close()

        f=open(dic3,'r')
        stems=f.read()
        self.stems=dict(eval(stems))
        f.close()
        
        f=open(dic4,'r')
        sentence_lengths=f.read()
        self.sentence_lengths=dict(eval(sentence_lengths))
        f.close()

        f=open(dic5,'r')
        three_adjacent=f.read()
        self.three_adjacent=dict(eval(three_adjacent))
        f.close()


    def similarity_scores(self,other):
        """returns a list of log similarity scores measuring the
        similarity of self and other – one score for each type of
        feature (words, word lengths, stems, sentence lengths, and your
        additional feature). You should make repeated calls to
        compare_dictionaries, and put the resulting scores in a list
        that the method returns.
        """
        scores=[]
        word_score_a = compare_dictionaries(other.words, self.words)
        word_score_b = compare_dictionaries(other.word_lengths, self.word_lengths)
        word_score_c = compare_dictionaries(other.stems, self.stems)
        word_score_d = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        word_score_e = compare_dictionaries(other.three_adjacent, self.three_adjacent)
        return scores+[word_score_a]+[word_score_b]+[word_score_c]+[word_score_d]+[word_score_e]

    def classify(self,source1,source2):
        """compares the called TextModel object (self) to two other
        “source” TextModel objects (source1 and source2) and determines
        which of these other TextModels is the more likely source of the
        called TextModel.
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print ('scores for '+source1.name+': '+ str(scores1))
        print ('scores for '+source2.name+': '+ str(scores2))
        count1=0
        count2=0
        for s in range(len(scores1)):
                if scores1[s]>scores2[s]:
                        count1+=1
                if scores1[s]<scores2[s]:
                        count2+=1
        if count1>count2:
                print(self.name+' is more likely to have come from '+source1.name)
        if count1<count2:
                print(self.name+' is more likely to have come from '+source2.name)
        if count1==count2:
                print (self.name+' is equally likely to have come from either')


###Testing###
def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ see if missing text from friends matches """
    source1 = TextModel('Two and 1/2 Men Pilot - Chuck Lorre Script')
    source1.add_file('friends.txt')

    source2 = TextModel('BBT Pilot- Chuck Lorre and Bill Prady Script')
    source2.add_file('BBT_pilot.txt')

    new1 = TextModel('Random BBT Script')
    new1.add_file('BBT.txt')
    new1.classify(source1, source2)
