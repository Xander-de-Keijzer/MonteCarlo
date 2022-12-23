import numpy as np

class MersenneTwister:
    """
    A Mersenne Twister pseudo-random number generator.
    """

    def __init__(self, seed=0, **kwargs):
        """
        Initialize a Mersenne Twister instance with the given seed and any optional parameters specified in kwargs.
        
        Parameters
        ----------
        seed : int, optional
            The seed for the generator. Default is 0.
        w : int, optional
            The word size, in bits. Default is 32.
        r : int, optional
            The degree of recurrence. Default is 31.
        n : int, optional
            The degree of the polynomial. Default is 624.
        m : int, optional
            The middle word. Default is 397.
        a : int, optional
            The coefficient of the rational normal form twist matrix. Default is 0x9908b0df.
        b : int, optional
            The tempering bitmask. Default is 0x9d2c5680.
        c : int, optional
            The tempering bitmask. Default is 0xefc60000.
        d : int, optional
            The tempering bitmask. Default is calculated from w.
        f : int, optional
            The tempering bitmask. Default is 0x6c078965.
        u : int, optional
            The tempering shift. Default is 11.
        l : int, optional
            The tempering shift. Default is 18.
        s : int, optional
            The tempering shift. Default is 7.
        t : int, optional
            The tempering shift. Default is 15.
        """
        self.seed = seed
        self.write_defaults()
        for key in kwargs:
            if key in ["w","r","n","m","a","b","c","d","f","u","l","s","t"]:
                try:
                    setattr(self, key, int(kwargs[key]))
                except ValueError:
                    raise ValueError(f"Illegal value for '{key}', should be 'int' was {type(kwargs[key])}.")
            else:
                raise ValueError(f"Illegal variable '{key}' not defined in class.")
        self.initialize()

    def write_defaults(self):
        """
        Set the default values for the parameters of the Mersenne Twister.
        """
        self.w = 32
        self.r = 31
        self.n = 624
        self.m = 397
        self.a = 0x9908b0df
        self.b = 0x9d2c5680
        self.c = 0xefc60000
        self.f = 0x6c078965
        self.u = 11
        self.l = 18
        self.s = 7
        self.t = 15

    def initialize(self):
        """
        Initialize the state of the Mersenne Twister.
        """
        self.d = (2**self.w - 1)
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = ~self.lower_mask & self.d
        self.seed_x()
        
    def seed_x(self):
        """
        Seed the state of the Mersenne Twister and fill the polynomial x.
        """
        self.index = self.n
        self.x = np.zeros(self.n, dtype = np.uint32)
        self.x[0] = self.seed

        for i in range(1, self.n):
            xi = self.f * (self.x[i-1] ^ (self.x[i-1] >> (self.w - 2))) + i
            self.x[i] = xi & self.d

    def twist(self):
        """
        Perform a twist operation on the state of the Mersenne Twister.

        It updates each element in 'x' with a value derived from another
        element in 'x' using bitwise operations. This code depends on the
        paramaters 'a', 'm' and 'r'.
        """
        for i in range(self.n):
            xi = (self.x[i] & self.upper_mask) | (self.x[(i+1) % self.n] & self.lower_mask)
            xA = xi >> 1
            if (xi % 2) == 1:
                xA ^= self.a
            self.x[i] = self.x[(i + self.m) % self.n] ^ xA
        self.index = 0

    def next_number(self) -> int:
        """
        Generate and return the next unsigned 32-bit integer in the sequence.
        
        Returns
        -------
        int
            The next unsigned 32-bit integer in the sequence.
        """
        if self.index == self.n:
            self.twist()

        y = self.x[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ ((y >> self.l) & self.d)

        self.index = (self.index + 1) % self.n
        return y

    def next_float(self, a: float, b: float=None) -> float:
        """
        Generate and return the next floating point number in the sequence, uniformly distributed in the range [a, b).
        
        Parameters
        ----------
        a : float
            The lower bound of the range.
        b : float, optional
            The upper bound of the range. If not specified, the range is [0, a). Default is None.
        
        Returns
        -------
        float
            The next floating point number in the sequence, uniformly distributed in the specified range.
        """
        if b is None:
            return self.next_number() / self.d * a
        else:
            d = b - a
            return self.next_number() / self.d * d + a

    def next_int(self, a: int, b: int=None) -> int:
        """
        Generate and return the next integer in the sequence, uniformly distributed in the range [a, b).
        
        Parameters
        ----------
        a : int
            The lower bound of the range.
        b : int, optional
            The upper bound of the range. If not specified, the range is [0, a). Default is None.
        
        Returns
        -------
        int
            The next integer in the sequence, uniformly distributed in the specified range.
        """
        return int(np.round(self.next_float(a, b)))