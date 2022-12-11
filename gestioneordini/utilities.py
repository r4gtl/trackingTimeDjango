import datetime

'''
Le prossime due variabili indicano ora di inizio e l'ora di fine
del range valido per l'inserimento
'''
START_TIME=datetime.time(6, 00, 00)
END_TIME=datetime.time(19, 00, 00)




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




def check_start_time(start_time):
    '''
    Controlla se l'orario di inizio inserito è compreso tra le 06.00 e le 19.00
    come richiesto da Ivano in data 09/12/2022
    '''    
    if start_time<datetime.time(6, 00, 00) or start_time>datetime.time(19,00,00):
        codice='L\'orario di inizio deve essere compreso tra le 06.00 e le 19.00!'
        return (True, codice)
    
    return(False,)



def check_end_time(end_time):
    '''
    Controlla se l'orario di fine inserito è compreso tra le 06.00 e le 19.00
    come richiesto da Ivano in data 09/12/2022
    '''  
    print("end_time: " + str(type(end_time)))    
    print("START_TIME: " + str(START_TIME) + str(type(START_TIME)))
    print("END_TIME: " + str(END_TIME))
    if end_time<START_TIME or end_time>END_TIME:
        codice='L\'orario di fine lavorazione deve essere compreso tra le 06.00 e le 19.00!'
        return (True, codice)
    
    return(False,)
        


def check_time_range(start_time, end_time):
    if start_time<START_TIME or start_time>END_TIME:
        codice=f'L\'orario di inizio deve essere compreso tra le {START_TIME} e le {END_TIME}!'
        return (True, codice)
    if end_time:
        if end_time<START_TIME or end_time>END_TIME:
            codice=f'L\'orario di inizio deve essere compreso tra le {START_TIME} e le {END_TIME}!'
            return (True, codice)
    
    return(False,)
    

