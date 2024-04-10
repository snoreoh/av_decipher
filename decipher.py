import math
import string

engLetter_freq = {
	'A': 0.08167,'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 
    'G': 0.02015,'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 
    'M': 0.02406,'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 
    'S': 0.06327,'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
	'Y': 0.01974, 'Z':0.00074
}

engCoinIndex = 0.0667
theABC = string.ascii_uppercase

relPrime = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25] # взаимно простые с 26

# Нахождение обратного 
def findReverseChar(a, b = 26):
	r, s, t = [min(a, b), max(a, b)], [1, 0], [0,1]
	
	while r[-1] != 1:
		q = r[-2] // r[-1]
		r.append(r[-2] - q*r[-1])
		s.append(s[-2] - q*s[-1])
		t.append(t[-2] - q*t[-1])
	
	return (s[-1] % r[1])

# D(x) = a^(-1)(x - b) mod 26 - функция дешифрования Афинного шифра
def AfineDecrypt(msg, key_pair):
	return ''.join(theABC[findReverseChar(key_pair[0])*(theABC.index(letter) - key_pair[1])%26] for letter in msg)


def sumCharsFreqInMessage(msg):
	if len(msg) != 0:
		return sum([msg.count(letter)*engLetter_freq[letter]/len(msg) for letter in theABC])


## Дешифрование текста, зашифрованного Афинным шифром
with open('Affine.txt', 'r') as file:
	msg = file.read()
	result = []
	for a in relPrime:
		for b in range(26):
			result.append((sumCharsFreqInMessage(AfineDecrypt(msg, [a, b])), a, b))
	final_key_pair = max(result, key=lambda x: x[0])
	
	print('_____________Афинный шрифт___________________')
	print(final_key_pair)
	print('Дешифрованный текст: ', AfineDecrypt(msg, [final_key_pair[1], final_key_pair[2]]))

#------------------------------------------------------------------------------------------------------------------------------------------------
def countLetters(msg):
	return {letter: msg.count(letter) for letter in theABC}

def indexCoin(msg):
	return sum([dict.get(countLetters(msg), letter, 0)* (dict.get(countLetters(msg), letter, 0) - 1) / (len(msg)*(len(msg) - 1)) for letter in theABC])

def shiftCoin(msg):
	shiftedCoinDict = {}
	for i in range(1, 26):
		text = ''.join([msg[k] for k in range(0, len(msg), i)])
		shiftedCoinDict[i] = indexCoin(text)
	return shiftedCoinDict

def findKeyLenght(msg):
	return min([(index, coin) for index, coin in shiftCoin(msg).items() if abs(coin - engCoinIndex) < engCoinIndex * 0.1], key=lambda k: k[0])[0]

def shiftABC(letter, offset):
	return theABC[(theABC.index(letter)+offset)%26]

def probableKey(msg):
	keys=[]
	for i in range(26):
		text = ''.join(map(shiftABC, list(msg), [26-i,]*len(msg)))
		keys.append((i, sumCharsFreqInMessage(text)))
	return max(keys, key=lambda x: x[1])

def findKey(msg, keylen):
	key = []
	for i in range(keylen):
		text = ''.join([msg[k] for k in range(i, len(msg), keylen)])
		keyPart = probableKey(text)
		key.append(theABC[keyPart[0]])
	return ''.join(key)

with open('Vigenere.txt', 'r') as file:
	msg = file.read()
	keyLen = findKeyLenght(msg)
	key = findKey(msg, keyLen)
	print('_____________Шрифт Вижинера___________________')
	print('Длина ключа = ', keyLen)
	print('Ключ = ', key)

	VigenereDecrypt = ''.join(map(shiftABC, msg, list(map(lambda x: 26-theABC.index(x), key))*(len(msg)//len(key)+1)))
	print('Дешифрованный текст: ', VigenereDecrypt)