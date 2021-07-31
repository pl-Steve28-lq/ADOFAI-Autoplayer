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
      atval = []
      atname = []
      for i in range(nL):
        name = names[i]
        istuple = False
        if isinstance(name, tuple):
          name, value = name
          istuple = True
        if i >= aL and not istuple:
          raise Exception('Not enough arguments!')
        v = value if i >= aL else args[i]
        setattr(self, name, v)
        atname.append(name)
        atval.append(v)
      setattr(self, 'attrs', atval)
      setattr(self, 'attrnames', atname)
      
    def __eq__(self, other):
      return id(self) == id(other)

    def __hash__(self):
      hash_ = 0
      for p in self.attrs:
        hash_ ^= hash(p)
      return hash_

    def __str__(self):
      arg = ', '.join(f'{self.attrnames[i]}={self.attrs[i]}' for i in range(len(self.attrs)))
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
        
