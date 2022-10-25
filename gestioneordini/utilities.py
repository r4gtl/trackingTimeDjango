

def check_barcode_type(barcode, tipo_barcode):
    
    verifica, codice = barcode.split('-')    
    if verifica.lower()!=str(tipo_barcode):                
        return (False, 'Stai passando un barcode sbagliato. Il barcode che stai passando è relativo a ' + str(verifica))
    return (True, codice)
    

def check_barcode(barcode):
    delimiter='-'
    if delimiter not in barcode:
        return(True, 'Barcode non valido!')