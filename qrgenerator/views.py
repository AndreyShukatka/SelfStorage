from django.shortcuts import render
import qrcode

def qrgenerator(request):
    qr_image = False
    if request.method == "POST":
        data = request.POST['data']
        img = qrcode.make(data)
        img.save("media/qr/test.png")
        qr_image = True
    return render(request, 'qrgenerator/qr.html', {'qr_image': qr_image})