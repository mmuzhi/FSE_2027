class NumericEntityUnescaper:
    def replace(self, input_str):
        if not input_str:
            return ""
        
        out = []
        n = len(input_str)
        pos = 0
        
        while pos < n - 2:
            if input_str[pos] == '&' and input_str[pos+1] == '#':
                start = pos + 2
                is_hex = False
                
                if start < n and (input_str[start] == 'x' or input_str[start] == 'X'):
                    start += 1
                    is_hex = True
                
                if start >= n:
                    break
                    
                end = start
                while end < n and self.is_hex_char(input_str[end]):
                    end += 1
                    
                if end < n and input_str[end] == ';':
                    try:
                        num_str = input_str[start:end]
                        base = 16 if is_hex else 10
                        entity_value = int(num_str, base)
                        out.append(chr(entity_value & 0xFF))
                        pos = end + 1
                        continue
                    except ValueError:
                        pass
                else:
                    out.append(input_str[pos])
            else:
                out.append(input_str[pos])
            pos += 1
            
        return ''.join(out)
    
    @staticmethod
    def is_hex_char(c):
        return c.isdigit() or ('a' <= c.lower() <= 'f')