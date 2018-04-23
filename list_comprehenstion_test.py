mylst = [k**2 for k in range(2, 9) if k > 4]
print(mylst)

mylst = [k.upper() for k in ['a', 'S', 'd', 'Fg'] if k.islower()]
print(mylst)

mylst = [k for k in range(2, 50) if k in range(2, 8) or k in [j for j in range(2, 8) if not k % j]]
print(mylst)

mylst = [k for k in range(2, 50) if k not in [j for j in range(2, 8) if k % j]]
print(mylst)

mylst = [j for j in range(2, 50) if j not in [k for k in range(2, 8) if not j % k]]
print(mylst)
