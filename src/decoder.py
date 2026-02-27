from hashlib import sha256
x = int(input("Digite um número: "))
y = int(input("Digite outro número: "))
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1
print(f'The solution is y = {y}')