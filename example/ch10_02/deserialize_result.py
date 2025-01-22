import pickle
import binascii

if __name__ == "__main__":
    serialized_result = binascii.unhexlify("80054B032E")
    
    result = pickle.loads(serialized_result)
    
    print(result)