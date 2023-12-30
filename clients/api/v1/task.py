
from django.http import HttpResponse
import csv
from clients.api.v1.serializers import ClientResgisterSerializer
from clients.models import Client
from bills.models import Bill
from datetime import datetime


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

def bulk_client_csv_import():
    clients_data = []
    failed_emails = []
    try:
        with open('import/clients_import.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                client_data = {
                    'email': row[0],
                    'document': row[1],
                    'password': row[2],
                    'first_name': row[3],
                    'last_name': row[4],
                }
                clients_data.append(client_data)
        serializer = ClientResgisterSerializer(data=clients_data, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            failed_emails.extend(client_data.get('email') for client_data in clients_data if 'email' in client_data)

        return True
    except Exception as e:
        print(e)
        raise e
    finally:
        if failed_emails:
            file_name = f'import/failed_emails_{datetime.now().strftime("%Y%m%d%H%M%S")}.txt'
            with open(file_name, 'w') as txt_file:
                txt_file.write('\n'.join(failed_emails))
            print(f'Los emails que no se pudieron guardar se han guardado en el archivo: {file_name}')

    
    