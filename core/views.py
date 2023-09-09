from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from gestioneordini.models import tblTempiMaster, Tbldettaglioordini
# Import per stampa pdf
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.views import View
from gestioneordini.models import Tblgruppi, Tblpoli, Tblcave




'''
Stampa tabella griglie
'''

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


def view_grid_labels(request, iddettordine, labels_count):
        '''
        view aggiunta per vedere i tempi aperti su una singola linea 
        per poter selezionare quello da chiudere come da richiesta del 16/11/2022
        '''
        dettaglio=Tbldettaglioordini.objects.get(pk=iddettordine)
        labels=range(labels_count)
        if dettaglio.idcollegamento:
            gruppo = Tblgruppi.objects.get(idgruppo=dettaglio.idcollegamento.idgruppo)
            idpoli = Tblpoli.objects.get(idpoli=gruppo.idpoli) 
            poli = idpoli.poli
            idcave = Tblcave.objects.get(idcave=gruppo.idcave)
            cave = idcave.cave
        else:
            poli=""
            cave=""

        context={
                "dettaglio": dettaglio,
                "labels_count": labels,
                "poli": poli,
                "cave": cave
        }
        return render(request, "grid_label.html", context)