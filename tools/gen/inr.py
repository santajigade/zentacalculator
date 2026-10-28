def inr(x, dec=0):
    neg = x < 0; x = abs(round(x, dec))
    s = f"{x:.{dec}f}"; ip, _, fp = s.partition('.')
    if len(ip) > 3:
        head, tail = ip[:-3], ip[-3:]
        parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        ip = ','.join(parts + [tail])
    return ('-' if neg else '') + '₹' + ip + ('.' + fp if fp else '')
def lakh(x):
    if x >= 1e7: return f"₹{x/1e7:.2f} crore"
    return f"₹{x/1e5:.2f} lakh"
