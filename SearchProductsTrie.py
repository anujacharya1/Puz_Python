'''
Created on Sep 23, 2013

@author: anujacharya
'''
from functools                      import wraps

def nestedDictIteration(d,endDelimeter):
    '''
    This function iterate over the nested dictonary
    '''
    #d = {'a': {'d': {'_end': '_end'}}, 'h': {'o': {'n': {'e': {'_end': '_end'}}}}}
    #d = {'a': {'a': {'_end': '_end'}, '_end': '_end'}, '_end': '_end'}

    stack = list() # A list behaving as stack
    s =''
    result = list()

    for k in d.keys():
        s+=k

        if k is endDelimeter:
            # If we found some exact match
            result.append('')
            d.pop(endDelimeter)
              
        else:
            # Get the inside dict and put in stack
            stack.append(d[k])
            if endDelimeter in d[k] and (type(d[k]) is type({})):
                # This here will get you 'a' if there is list containing [a,aa,aaa]
                result.append(k)
            while stack:
                # remove the dict from the stack
                insideDict = stack.pop()
                if (type(insideDict) == type({})):
                    # if there is dict inside dict and not string
                    for key in insideDict.keys():
                        # Iterate over all the keys inside the dict
                        if key is not endDelimeter:
                            # I can make use list comprehension but for readbility purpose
                            # i am not doing it
                            
                            s+=key
                            stack.append(insideDict[key])
            result.append(s)
            if len(result) is 10:
                # break when we get 10 result
                break
            s=''
    return result

def preprocess(fun):
    '''
    Wrapper to pre-process the trie
    '''
    @wraps(fun)
    def wrapper(words, search, *args, **kwargs):
        root = dict()
        _end = '_end' # Delimeter
        for word in words:
            current_dict = root
            for letter in word:
                current_dict = current_dict.setdefault(letter, {})
            current_dict = current_dict.setdefault(_end, _end)
        
        # Search and return
        for letter in search:
            if letter in root:
                root = root[letter]
        
        kwargs['root']  =  root
        kwargs['end']   = _end # delimeter
        
        return fun(input, search, *args, **kwargs)
    
    return wrapper
    
@preprocess
def parseThefile(input, search, *args, **kwargs):
    root    = kwargs['root']
    end     = kwargs['end']

    # Join all the keys till end
    result = nestedDictIteration(root,end)
    if result is None:
        # Found the exact match
        result = [search]
    else:
        result = [search+i for i in result]
         
    print result

if __name__ == '__main__':
    input = ['iphone', 'ipad', 'gmail']
    search = 'ip'
    parseThefile(input, search)
      
    inputWithD  = ['da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'di', 'dj', 'dk']
    searchD = 'd'
    parseThefile(inputWithD, searchD)
     
    inputWithG  = ['a', 'aa', 'aaa']
    searchG = 'a'
     
    parseThefile(inputWithG, searchG)
     
    inputWithH  = ['apple']
    searchH = 'apple'
     
    parseThefile(inputWithH, searchH)
     
    inputWithI  = ['apple', 'apple']
    searchI = 'apple'
     
    parseThefile(inputWithI, searchI)
    
    
    