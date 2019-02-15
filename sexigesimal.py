def sex(x):
	import numpy as np
	if x == int(x): integer = True
	else: integer = False
	
	if 18446744073709551615 > x > 0:
		max_order = int(np.log(x)/np.log(60.))
		negative = False
	elif 0 > x > -18446744073709551615:
		x = np.abs(x)
		max_order = int(np.log(x)/np.log(60.))
		negative = True
	elif x == 0: 
		return str(x) #due to problems with logs this is the easiest way
		raise Exception("Seriously?")
	else:
		raise Exception("Currently cannot calculate numbers greater than 2^64 - 1 but props for trying")
	
	digits = list()
	
	if x >= 1:
		orders_to_check = np.arange(max_order+1)[::-1]
		if integer == True: pass
		else: orders_to_check = np.append(orders_to_check, (-1)*np.arange(8)[1:] )
		
		for n in orders_to_check:
			digits.append(int(float(x)/(60**n)))
			x = round(((float(x)/(60**n))-int(float(x)/(60**n)))*(60**n),8) #the 'round' deals with floating point errors
		
		if negative == False:
			if integer == True: sex = str(digits[:max_order+1])[1:-1]
			else: sex = str(digits[:max_order+1])[1:-1]+"; "+str(digits[max_order+1:])[1:-1]
		else:
			if integer == True: sex = "-"+str(digits[:max_order+1])[1:-1]
			else: sex = "-"+str(digits[:max_order+1])[1:-1]+"; "+str(digits[max_order+1:])[1:-1]
	
	else:
		orders_to_check = (-1)*np.arange(8)[1:]
		for n in orders_to_check:
			digits.append(int(float(x)/(60**n)))
			x = ((float(x)/(60**n))-int(float(x)/(60**n)))*(60**n)
		
		if negative == False: sex = "0; "+str(digits)[1:-1]
		else: sex = "-0; "+str(digits)[1:-1]
	
	lasttest = sex.split(' ')
	
	while True:
		checkfailure = False
		isnegative = False
		for digit in np.arange(len(lasttest)):
			delimiter = lasttest[digit][-1]
			if lasttest[0][0]=='-':
				isnegative = True
				lasttest[0] = lasttest[0][1:]
			else: pass
			try:	
				if int(lasttest[digit][:-1]) == 60:
					checkfailure = True
					lasttest[digit] = str(0)+delimiter
					lasttest[digit-1] = str(int(lasttest[digit-1][:-1])+1)+lasttest[digit-1][-1]
				else: pass
			except ValueError:
				pass

		if isnegative == True: lasttest[0] = '-'+lasttest[0]
		else: pass

		if checkfailure == True: continue
		else: break

	sex = str()
	for digit in lasttest:
		sex += digit + ' '
	sex = sex[:-1]
	return sex

def desex(sex):
	import numpy as np
	if sex[0] == '-':
		sex = sex[1:]
		negative = True
	else: negative = False

	if ";" in sex:
		sex = sex.split(";")
		decimal = True
	else: decimal = False

	if decimal == True:
		if len(sex) > 2: raise Exception("There should be at most one semicolon in a sexigessimal number.")
		else:
			integer_sex = sex[0].split(",")
			decimal_sex = sex[1].split(",")
	else:
		integer_sex = sex.split(",")

	for digit in np.arange(len(integer_sex)): 
		if integer_sex[digit] != '': integer_sex[digit] = int(integer_sex[digit])
		else: integer_sex[digit] = int(0)

	if decimal == True: 
		for digit in np.arange(len(decimal_sex)): 
			if decimal_sex[digit] != '': decimal_sex[digit] = int(decimal_sex[digit])
			else: decimal_sex[digit] = int(0)
	else: pass

	n, answer = 0, 0
	for element in integer_sex[::-1]:
		answer += element*(60**n)
		n += 1

	n = 1
	if decimal == True:
		for element in decimal_sex:
			answer += element*(60**(-n))
			n += 1
	else: pass

	if negative == True: answer *= (-1)
	else: pass

	return answer

def sexadd(num1, num2=0):
	if isinstance(num1, str):
		return sex(desex(num1) + desex(num2))
	elif isinstance(num1, list):
		for sexnum in num1:
			num2 += desex(sexnum)
		return sex(num2)
	else: print "This is not a valid set of arguments." 

def sexsub(num1, num2=0):
	if isinstance(num1, str):
		return sex(desex(num1) - desex(num2))
	elif isinstance(num1, list):
		num2 = num1.pop(0)
		for sexnum in num1:
			num2 += -desex(sexnum)
		return sex(num2)
	else: print "This is not a valid set of arguments." 

def sexmul(num1, num2=1):
	if isinstance(num1, str):
		return sex(desex(num1) * desex(num2))
	elif isinstance(num1, list):
		for sexnum in num1:
			num2 *= desex(sexnum)
		return sex(num2)
	else: print "This is not a valid set of arguments." 

def sexdiv(num1, num2=1):
	if isinstance(num1, str):
		return sex(desex(num1) / desex(num2))
	elif isinstance(num1, list):
		num2 = num1.pop(0)
		for sexnum in num1:
			num2 *= 1/desex(sexnum)
		return sex(num2)
	else: print "This is not a valid set of arguments." 






















