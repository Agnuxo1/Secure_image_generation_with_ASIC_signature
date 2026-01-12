import struct
import binascii

def find_silicon_meta(path):
    print(f"Direct binary audit: {path}")
    with open(path, 'rb') as f:
        header = f.read(8)
        if header != b'\x89PNG\r\n\x1a\n':
            print("Not a valid PNG")
            return
            
        while True:
            chunk_len_data = f.read(4)
            if not chunk_len_data: break
            length = struct.unpack('>I', chunk_len_data)[0]
            chunk_type = f.read(4)
            
            if chunk_type == b'tEXt':
                data = f.read(length)
                parts = data.split(b'\x00')
                if len(parts) >= 2:
                    key = parts[0].decode('latin-1', errors='ignore')
                    value = parts[1].decode('latin-1', errors='ignore')
                    if 'Silicon' in key:
                        print(f"[FOUND] {key}: {value}")
            elif chunk_type == b'zTXt':
                # Skip compressed chunks for now as we just need to see if they exist
                f.read(length)
            else:
                f.read(length)
            
            f.read(4) # CRC

if __name__ == "__main__":
    import sys
    path = 'D:/ASIC-ANTMINER_S9/ASIC_DIFFUSION_Art_Research_Memo/Secure_image_generation_with_ASIC_signature/Imagen_test2.png'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    find_silicon_meta(path)
