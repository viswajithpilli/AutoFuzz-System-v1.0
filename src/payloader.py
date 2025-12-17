
class Payloader:
    def __init__(self):
        pass

    def de_bruijn(self, charset, n, k):
        k = len(charset)
        a = [0] * k * n
        sequence = []

        def db(t, p):
            if t > n:
                if n % p == 0:
                    sequence.extend(a[1 : p + 1])
            else:
                a[t] = a[t - p]
                db(t + 1, p)
                for j in range(a[t - p] + 1, k):
                    a[t] = j
                    db(t + 1, t)

        db(1, 1)
        return "".join(charset[i] for i in sequence)

    def generate_cyclic_pattern(self, length):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        full_seq = self.de_bruijn(charset, 4, len(charset))
        return full_seq[:length]

    def find_offset(self, val, pattern):
        if isinstance(val, int):
             try:
                 packed = val.to_bytes(4, byteorder='little')
                 s_val = packed.decode('latin-1')
             except:
                 return -1
        else:
            s_val = val
            
        return pattern.find(s_val)

if __name__ == "__main__":
    p = Payloader()
    pat = p.generate_cyclic_pattern(100)
    print(f"Pattern (100): {pat}")
