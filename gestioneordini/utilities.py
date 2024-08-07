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
    '''Restituisce un check per sapere se è stato associato un tempo medio al codice/collegamento'''
    if (
        (comp_coll.ore_medie_lavorazione == 0 or comp_coll.ore_medie_lavorazione is None) and
        (comp_coll.minuti_medi_lavorazione == 0 or comp_coll.minuti_medi_lavorazione is None) and
        (comp_coll.secondi_medi_lavorazione == 0 or comp_coll.secondi_medi_lavorazione is None)
    ):
        messaggio_tempo = f'Nessun tempo medio assegnato al codice!'
        print(f'comp_coll.minuti_medi_lavorazione: {comp_coll.minuti_medi_lavorazione}')
        print(f"messaggio tempo: {messaggio_tempo}")
        return(False, messaggio_tempo)
    else:
        print("Tempo assegnato")
        print(f'comp_coll.minuti_medi_lavorazione: {comp_coll.minuti_medi_lavorazione}')
        messaggio_tempo = f'Tempo medio assegnato al codice.'
        return(True, messaggio_tempo)
    

def get_tempo_medio(tempo, comp_coll):
    '''Restituisce i dati relativi al tempo medio inserito nell'app 
        anagrafica del codice componente/collegamento. C'è un primo controllo per verificare i campi,
        per passare poi al controllo e all'applicazione della tolleranza percentuale.
        comp_coll: passare il componente/collegamento da analizzare;
        tempo: è il tempo medio. Serve per calcolare se siamo in media o no.
    '''
    print(f"comp_coll: {comp_coll}")
    if comp_coll.ore_medie_lavorazione is None or comp_coll.ore_medie_lavorazione==0:
        ore_medie=0
    else:
        ore_medie=comp_coll.ore_medie_lavorazione
        
    if comp_coll.minuti_medi_lavorazione is None or comp_coll.minuti_medi_lavorazione==0:
        minuti_medi=0
    else:
        minuti_medi=comp_coll.minuti_medi_lavorazione
    if comp_coll.secondi_medi_lavorazione is None or comp_coll.secondi_medi_lavorazione==0:
        secondi_medi=0
    else:
        secondi_medi = comp_coll.secondi_medi_lavorazione
    print(f"ore_medie: {ore_medie}; minuti_medi: {minuti_medi}; secondi_medi: {secondi_medi}")
    tempo_medio = timedelta(hours=ore_medie, minutes=minuti_medi, seconds=secondi_medi)
    print(f'tempo medio in get_tempo_medio: {tempo_medio}')
    tolleranza_percentuale = comp_coll.perc_tempo
    
    if tolleranza_percentuale==0 or tolleranza_percentuale is None:
        tempo_massimo_consentito = tempo_medio
        tolleranza_percentuale==0
    else:
        tempo_massimo_consentito = tempo_medio + (tempo_medio * tolleranza_percentuale / 100)
    
    if tempo.total_seconds() <= tempo_massimo_consentito.total_seconds():
        print("tempo medio funzione: " + str(tempo_medio) + " " + "tempo massimo: " + str(tempo_massimo_consentito))
        return True, tempo_medio, tempo_massimo_consentito, tolleranza_percentuale
    else:
        print("tempo medio funzione: " + str(tempo_medio) + " " + "tempo massimo: " + str(tempo_massimo_consentito))
        return False, tempo_medio, tempo_massimo_consentito, tolleranza_percentuale
        
def get_tempo_nominale(comp_coll):
    '''06/07/2024: richiesto da Ivano. Abbiamo aggiunto i campi al modello TempoMaster, in modo da fotografare
        quali erano i tempi medi consentiti alla data di chiusura del tempo.
    FORSE ELIMINA
    '''
    
    if comp_coll.ore_medie_lavorazione is None or comp_coll.ore_medie_lavorazione==0:
        ore_medie=0
    else:
        ore_medie=comp_coll.ore_medie_lavorazione
    if comp_coll.minuti_medi_lavorazione is None or comp_coll.minuti_medi_lavorazione==0:
        minuti_medi=0
    else:
        minuti_medi=comp_coll.minuti_medi_lavorazione
    if comp_coll.secondi_medi_lavorazione is None or comp_coll.secondi_medi_lavorazione==0:
        secondi_medi=0
    else:
        secondi_medi = comp_coll.secondi_medi_lavorazione
    tolleranza_percentuale = comp_coll.perc_tempo
    print(f"comp_coll: " + str(comp_coll) + " ore_medie: " + str(ore_medie) + " minuti_medi: " + str(minuti_medi) + " secondi_medi: " + str(secondi_medi) + " perc: " + str(tolleranza_percentuale))
    return ore_medie, minuti_medi, secondi_medi, tolleranza_percentuale

def get_tempo_nominale_registrato(tempomaster):
    '''23/07/2024: richiesto da Ivano. Abbiamo aggiunto i campi al modello TempoMaster, in modo da fotografare
        quali erano i tempi medi consentiti alla data di chiusura del tempo.
    '''
    
    if tempomaster.ore_medie_lavorazione is None or tempomaster.ore_medie_lavorazione==0:
        ore_medie=0
    else:
        ore_medie=tempomaster.ore_medie_lavorazione
    if tempomaster.minuti_medi_lavorazione is None or tempomaster.minuti_medi_lavorazione==0:
        minuti_medi=0
    else:
        minuti_medi=tempomaster.minuti_medi_lavorazione
    if tempomaster.secondi_medi_lavorazione is None or tempomaster.secondi_medi_lavorazione==0:
        secondi_medi=0
    else:
        secondi_medi = tempomaster.secondi_medi_lavorazione
    tolleranza_percentuale = tempomaster.perc_tempo
    tempo_medio_registrato = timedelta(hours=ore_medie, minutes=minuti_medi, seconds=secondi_medi)
    print(f"tempo_medio_registrato get_tempo_nominale_registrato: {tempo_medio_registrato}")
    if tolleranza_percentuale==0 or tolleranza_percentuale is None:
        tempo_massimo_consentito = tempo_medio_registrato
        tolleranza_percentuale==0
    else:
        tempo_massimo_consentito = tempo_medio_registrato + (tempo_medio_registrato * tolleranza_percentuale / 100)
    
    print(f"tempo_massimo_consentito get_tempo_nominale_registrato: {tempo_massimo_consentito}")
    print(f"ore_medie: " + str(ore_medie) + " minuti_medi: " + str(minuti_medi) + " secondi_medi: " + str(secondi_medi) + " perc: " + str(tolleranza_percentuale))
    return tempo_medio_registrato, tempo_massimo_consentito

# Ivano chiede la differenza tra tempo di produzione e tempo nominale. Questa differenza va calcolata
# come percentuale sul tempo maggiorato della percentuale di tolleranza. 02/10/2023        
def get_perc_differenza(tempo_medio_produzione, tempo_massimo_consentito, tempo_medio_nominale):
    ore_tmp, minuti_tmp, secondi_tmp = map(int, tempo_medio_produzione.split(':'))
    ore_tmc, minuti_tmc, secondi_tmc = map(int, tempo_massimo_consentito.split(':'))
    #ore_tmn, minuti_tmn, secondi_tmn = map(int, tempo_medio_nominale.split(':'))
    
    
    timedelta_object = tempo_medio_nominale
    

    totale_secondi_tmp = ore_tmp * 3600 + minuti_tmp * 60 + secondi_tmp
    totale_secondi_tmc = ore_tmc * 3600 + minuti_tmc * 60 + secondi_tmc
    #totale_secondi_tmn = ore_tmn * 3600 + minuti_tmn * 60 + secondi_tmn
    totale_secondi_tmn=timedelta_object.total_seconds()
    # Se si è impiegato più tempo del previsto 
    if tempo_massimo_consentito < tempo_medio_produzione:
        differenza_tempo = totale_secondi_tmp - totale_secondi_tmn
        print('differenza_tempo: ' + str(differenza_tempo))
        print("totale_secondi_tmp: " + str(totale_secondi_tmp) + 'totale_secondi_tmc: ' + str(totale_secondi_tmc))
        differenza_percentuale = round(((differenza_tempo/totale_secondi_tmc)*100))
        
        return (differenza_percentuale)
    # altrimenti
    else:
        differenza_tempo = totale_secondi_tmc - totale_secondi_tmp 
        print("totale_secondi_tmp: " + str(totale_secondi_tmp) + 'totale_secondi_tmc: ' + str(totale_secondi_tmc))
        differenza_percentuale = round(((differenza_tempo/totale_secondi_tmc)*100)*-1)
        return (differenza_percentuale)
        
        
    
    