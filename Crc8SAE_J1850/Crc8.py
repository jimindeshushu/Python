import os

def Crc8(u8_data, leng):
   u8_crc8 = (0xFF)
   u8_poly = (0x1D)

   for i in range(0,leng,1):
      u8_crc8^=(u8_data[i])
      for j in range(0,8,1):
         if(u8_crc8&0x80):
            u8_crc8 = ((u8_crc8 << 1) & 0xFF) ^ u8_poly
         else:
            u8_crc8 <<= 1

   #u8_crc8 ^= 0xFF
   return hex(u8_crc8)


if __name__ == '__main__':
   InputData = [(0x5^0xFF)]
   length = len(InputData)
   print(Crc8(InputData, length))
   #os.system("pause")
