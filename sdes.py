
'''
19cp014
SDES PYTHON PROGRAM
date:6/9/21


'''

'''
THIS ALL ARE THE STATIC VALUES WE NEEDED TO PERFORM SDES ALGORITHM. 
THIS INCLUDE P10(PERMUTATION 10),P8,P4 AND INITIAL PERMUTION AND ITS INVERSE AND RANDOK KEY VALUE,S BOXES(S0,S1),EXPANSION BOX
YOU MAY CHANGE THIS VALUE FOR DIFFERENT CASES 
'''
p10 = [3,5,2,7,4,10,1,9,8,6]
p8 = [6,3,7,4,8,5,10,9]
p4 = [2,4,3,1]
IP = [2,6,3,1,4,8,5,7]
IP_inv = [4,1,3,5,7,2,8,6]
expas = [4,1,2,3,2,3,4,1]
s0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
s1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
key = [1,0,1,0,0,0,0,0,1,0]


def shift(l,r,n):   #TO PERFORM LEFT SHIFT IN STRING BY n
  return l[n:]+l[0:n],r[n:]+r[0:n]

def permutation(bitstirng,arr):  #TO APPLY GIVEN (arr) PERMUTATION ON GIVEN BLOCK
  return "".join(bitstirng[index-1] for index in arr)

def expansion(bitstring,expans):  #TO APPLY EXPANSION ON GIVEN BLOCK
    return "".join([bitstring[expans[i]-1] for i in range(len(expans))])

def xor(bitstring,key):  #SIMPLE XOR OPERATION
  ans=""
  for i in range(len(bitstring)):
    if(bitstring[i]==key[i]):
      ans+="0";
    else:
      ans+="1";
  return ans
def genrate_key(k):  #THIS WILL RETURN TWO KEYS FOR SDES
  tmpkey=permutation(k,p10);
  l,r=tmpkey[0:5],tmpkey[5:];
  l,r=shift(l,r,1)
  k1=permutation(l+r,p8);
  l,r=shift(l,r,2)
  k2=permutation(l+r,p8);
  return k1[0:8],k2[0:8]

def bitTodec(str):  # 2 bit binary to decimal number converson
  dec={
    "00":0,
    "01":1,
    "10":2,
    "11":3
  }
  return dec.get(str);
def decTobin(str):  # decimal number <4 to 2 bit binary conversion
  dec={
    0:"00",
    1:"01",
    2:"10",
    3:"11"
  }
  return dec.get(str);
def givesboxoutput(bitstring,s):  # perform sbox operation
  row=bitTodec(bitstring[0]+bitstring[3]) #first and liast bit as a row
  col=bitTodec(bitstring[1]+bitstring[2]) # middle two bits(secind and third) as column
  return decTobin(s[row][col])

def fk(r1,k1):  #f(k) function
  mid=expansion(r1,expas)
  exor_out=xor(mid,k1);
  sbox_out1,sbox_out2=givesboxoutput(exor_out[0:4],s0),givesboxoutput(exor_out[4:],s1)
  return permutation(sbox_out1+sbox_out2,p4)


def process(plain,k1,k2):  #encryption and decryption starting
  mid=permutation(plain,IP)
  l1,r1=mid[0:4],mid[4:]
  fkoutput=fk(r1,k1)
  l2,r2=r1,xor(fkoutput,l1)
  fkoutput=fk(r2,k2)
  l2,r2=xor(l2,fkoutput),r2
  return permutation(l2+r2,IP_inv)

if __name__=='__main__':
  k1,k2=genrate_key(''.join(map(str,key)));
  ciphertext=process("01110010",k1,k2); #call process for given plain tect to cipher text transformation(ENCRYTION)
  print("Cipher Text: ",ciphertext)  
  plaintext=process(ciphertext,k2,k1)  #call process for given cipher tect to plain text transformation(DECRYTION)(DON'T MISS THAT FOR DECRYPTION WE USE KEY IN REVERSE ORDER)
  print("Plain Text: ",plaintext)
