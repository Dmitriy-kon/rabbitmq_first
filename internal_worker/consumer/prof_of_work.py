import hashlib
import time

from color_formatter import color_f




class Pow:
    MAX_NONCE = 2 ** 32

    def __init__(self, message, *args, **kwargs):
        self.message = message
    
    async def proof_of_word(self, header, difficulty_bits):
        targer = 2 ** (256-difficulty_bits)
        
        for nonce in range(self.MAX_NONCE):
            encode_to_bytes = f"{header}{nonce}".encode()
            hash_result = hashlib.sha256(encode_to_bytes).hexdigest()
            
            if int(hash_result, 16) < targer:
                print(f"{color_f.green}Success with nonce: {nonce}{color_f.default}")
                print(f"{color_f.green}Hash is: {hash_result}{color_f.default}")
                return hash_result, nonce
        
        print(f"{color_f.red}Failed after trying {self.MAX_NONCE} times{color_f.default}")
        return nonce
    
    
    async def calculate(self):
        nonce = 0
        hash_result = ''
        
        original_max_range=24
        test_range=24
        calculate_sart_time = time.time()
        
        for difficulty_bits in range(test_range):
            difficulty = 2 ** difficulty_bits
            
            print(f"Difficulty: {difficulty} ({difficulty_bits} bits)")
            print("Starting search")
            
            start_time = time.time()
            
            new_block = self.message + hash_result
            
            hash_result, nonce = await self.proof_of_word(new_block, difficulty_bits)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"Elapsed time: {elapsed_time:.4f} seconds")
            
            if elapsed_time > 0:
                hash_power = float(int(nonce) / elapsed_time)
                print(f"Hash power: {hash_power:2f} hashes per second")
        calculate_elapsed_time = time.time() - calculate_sart_time
        
        return hash_result, calculate_elapsed_time


if __name__ == "__main__":
    pow = Pow("hello world")
    _hash= pow.calculate()
    print(f"Hash: {_hash[0]} and time: {_hash[1]:.2f}")