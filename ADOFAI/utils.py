from functools import reduce

class Util:
    class Singleton:
        Instance = None
        
        @classmethod
        def init(cls, *args, **kwargs):
            if cls.Instance is None:
                cls.Instance = cls(*args, **kwargs)
            return cls.Instance

    def Factory(*names):
        def __init__(self, *args):
            nL, aL = map(len, (names, args))
            attrs = []
            for i, (name, arg) in enumerate(zip(names, args)):
                if isinstance(name, tuple):
                    if i >= aL: name, arg = name
                    else: name = name[0]
                setattr(self, name, arg)
                attrs.append((name, arg))
            setattr(self, 'attrs', tuple(attrs))
            
        def __eq__(self, other):
            return id(self) == id(other)

        def __hash__(self):
            xor = int.__xor__
            return reduce(xor, map(hash, self.attrs), 0)

        def __str__(self):
            arg = ', '.join(f'{name}={val}' for name, val in self.attrs)
            return f'{type(self).__name__}({arg})'
        
        return type('a', (Util._Factory,), {
            '__init__': __init__, '__eq__': __eq__, '__hash__': __hash__,
            '__str__': __str__, '__repr__': __str__
        })
        
    class _Factory:
        Memoiz = {}

        @classmethod
        def get(cls, *args):
                if m := cls.Memoiz.get(args): return m
                cls.Memoiz[args] = res = cls(*args)
                return res

    def TODO(): raise NotImplementedError()
                
