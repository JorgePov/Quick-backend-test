
from django.http import HttpResponse
import csv
from clients.models import Client
from bills.models import Bill

def generate_client_csv_export():
    clients = Client.objects.all()
    data = [['Documento', 'Nombre Completo', 'Cantidad de Facturas']]

    for client in clients:
        full_name = f"{client.first_name} {client.last_name}"
        invoice_count = Bill.objects.filter(client=client).count()
        data.append([client.document, full_name, invoice_count])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients_export.csv"'

    file_path = 'export/clients_export.csv' 

    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)

    return response
