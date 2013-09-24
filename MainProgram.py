'''
Created on Sep 23, 2013

@author: anujacharya
'''
from functools                      import wraps

def joinMultidict(d, end):
    
    if end in d :
        # found the exact match
        return None
    else:
        s = ''
        result = list()
        stack = d.items()
        while stack:
            k, v = stack.pop()
            
            if k is not end:
                s+=k
            else:
                result.append(s)
                s=''
                if len(result) is 10:
                    # break when we get 10 result
                    break
                
            if isinstance(v, dict):
                stack.extend(v.iteritems())
    
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
    result  = list()
    
    # Join all the keys till end
    result = joinMultidict(root,end)
    if result is None:
        # Found the exact match
        result = [search]
    else:
        result = [search+i for i in result]
        
    print result

if __name__ == '__main__':
    input = ['iphone', 'ipad ', 'gmail']
    search = 'iphon'
    parseThefile(input, search)
    
    inputWithD  = ['da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'di', 'dj', 'dk']
    searchD = 'd'
    parseThefile(inputWithD, searchD)
    
    