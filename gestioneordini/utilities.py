import datetime
from datetime import time, timedelta

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



def check_end_time(end_time, start_time):
    '''
    Controlla se l'orario di fine inserito è compreso tra le 06.00 e le 19.00
    come richiesto da Ivano in data 09/12/2022.
    Inoltre controllo che l'orario di fine sia maggiore dell'orario di inizio.
    '''  
    
    if end_time<START_TIME or end_time>END_TIME:
        codice='L\'orario di fine lavorazione deve essere compreso tra le 06.00 e le 19.00!'
        return (True, codice)    
    if end_time<start_time:
        codice='L\'orario di fine lavorazione deve essere superiore all\'orario di inizio!'        
        return (True, codice)  
    
    return(False,)
        


def check_time_range(start_time, end_time):
    if start_time<START_TIME or start_time>END_TIME:
        codice=f'L\'orario di inizio deve essere compreso tra le {START_TIME} e le {END_TIME}!'
        return (True, codice)
    if end_time:
        if end_time<START_TIME or end_time>END_TIME:
            codice=f'L\'orario di fine deve essere compreso tra le {START_TIME} e le {END_TIME}!'
            return (True, codice)
    
    return(False,)

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def get_if_media_tempo(comp_coll):
    if comp_coll.ore_medie_lavorazione==0 and comp_coll.minuti_medi_lavorazione==0 and comp_coll.secondi_medi_lavorazione==0:
        messaggio_tempo = f'Nessun tempo medio assegnato al codice!'
        return(False, messaggio_tempo)
    else:
        return(True,)
    

def get_tempo_medio(tempo, comp_coll):
    # ore_medie = comp_coll.ore_medie_lavorazione
    # minuti_medi = comp_coll.minuti_medi_lavorazione
    # secondi_medi = comp_coll.secondi_medi_lavorazione

    # tempo_medio = timedelta(hours=ore_medie, minutes=minuti_medi, seconds=secondi_medi)
    # tolleranza_percentuale = comp_coll.perc_tempo
    
    # if tolleranza_percentuale==0 or tolleranza_percentuale is None:
    #     tempo_massimo_consentito = tempo_medio
    # else:    
    #     tempo_massimo_consentito = tempo_medio + (tempo_medio * tolleranza_percentuale / 100)

    # if tempo.total_seconds() <= tempo_massimo_consentito.total_seconds():
    #     print("tempo medio funzione: " + str(tempo_medio) + " " + "tempo massimo: " + str(tempo_massimo_consentito))
    #     return True, tempo_medio, tempo_massimo_consentito
    # else:
    #     print("tempo medio funzione: " + str(tempo_medio) + " " + "tempo massimo: " + str(tempo_massimo_consentito))
    #     return False, tempo_medio, tempo_massimo_consentito

    if comp_coll.ore_medie_lavorazione is None:
        ore_medie=0
    else:
        ore_medie=comp_coll.ore_medie_lavorazione
    if comp_coll.minuti_medi_lavorazione is None:
        minuti_medi=0
    else:
        minuti_medi=comp_coll.minuti_medi_lavorazione
    if comp_coll.secondi_medi_lavorazione is None:
        secondi_medi=0
    else:
        secondi_medi = comp_coll.secondi_medi_lavorazione
    
    tempo_medio = timedelta(hours=ore_medie, minutes=minuti_medi, seconds=secondi_medi)
    tolleranza_percentuale = comp_coll.perc_tempo
    
    if tolleranza_percentuale==0 or tolleranza_percentuale is None:
        tempo_massimo_consentito = tempo_medio
    else:
        tempo_massimo_consentito = tempo_medio + (tempo_medio * tolleranza_percentuale / 100)
    
    if tempo.total_seconds() <= tempo_massimo_consentito.total_seconds():
        print("tempo medio funzione: " + str(tempo_medio) + " " + "tempo massimo: " + str(tempo_massimo_consentito))
        return True, tempo_medio, tempo_massimo_consentito
    else:
        print("tempo medio funzione: " + str(tempo_medio) + " " + "tempo massimo: " + str(tempo_massimo_consentito))
        return False, tempo_medio, tempo_massimo_consentito
        