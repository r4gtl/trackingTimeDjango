

def check_barcode(barcode, tipo_barcode):
    '''
    Controlla se il barcode è valido e se corrisponde al tipo di barcode necessario.
    Se è tutto a posto, ritorna la chiave primaria o il codice da passare al resto della view.
    '''
    delimiter='-'
    if delimiter not in barcode:
        return(False, 'Barcode non valido!')
    else:
        verifica, codice = barcode.split('-')    
        if verifica.lower()!=str(tipo_barcode):                
            return (False, 'Stai passando un barcode sbagliato. Il barcode che stai passando è relativo a ' + str(verifica))
    return (True, codice)
    

