def c_to_f(celsius):
    converted_list=[]
    for (i) in celsius:
        if not isinstance(i, (float,int)):
            print(f"Skipping non-integer: {i}")
            continue
        else:    
            fahrenheit = i * 9/5 +32
            converted_list.append(fahrenheit)
            print (i, 'degrees celsius is equal to',fahrenheit,'degrees fahrenheit')
    return converted_list
    
cel=[2,5,45,90]    
c_to_f(cel)