import requests
from django.shortcuts import render
import qrcode
import base64
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    short_url = None
    qr_code_data =None

    if request.method == 'POST':
        original_url = request.POST.get('url')

        # Shorten URL with an open source API
        response = requests.get(f'https://is.gd/create.php?format=simple&url={original_url}')
        short_url = response.text  # La réponse contient l'URL raccourcie

        # Generate QR Code
        qr_img = qrcode.make(short_url)
        buffered = BytesIO()
        qr_img.save(buffered, format="PNG")
        qr_code_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render(request, 'shorten/home.html', {'short_url': short_url, 'qr_code_data': qr_code_data})
