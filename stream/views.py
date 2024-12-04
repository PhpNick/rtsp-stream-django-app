import cv2
import base64
import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import RTSPLink
from .forms import RTSPLinkForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def stream_view(request, link_id=None):
    if link_id:
        rtsp_link = get_object_or_404(RTSPLink, pk=link_id, user=request.user)
        rtsp_url = rtsp_link.url
    else:
        rtsp_url = None

    if request.method == 'POST':
        link_id = request.POST.get('link_id')
        if link_id:
            rtsp_link = get_object_or_404(RTSPLink, pk=link_id, user=request.user)
            rtsp_url = rtsp_link.url

    if rtsp_url:
        conversion_url = 'http://localhost:5000/convert'
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'rtsp_url': rtsp_url})

        response = requests.post(conversion_url, headers=headers, data=data)

        if response.status_code == 202:
            response_data = response.json()
            hls_url = response_data.get('hls_link')
            if hls_url:
                hls_url = 'http://localhost:5000' + hls_url
           
                return render(request, 'stream/stream.html', {'hls_url': hls_url})

    links = RTSPLink.objects.filter(user=request.user)
    return render(request, 'stream/select_link.html', {'links': links})

def check_stream(request):
    hls_url = request.GET.get('url', '')
    try:
        response = requests.head(hls_url)
        stream_ready = response.status_code == 200
    except requests.RequestException:
        stream_ready = False

    return JsonResponse({'stream_ready': stream_ready})


@login_required
def stream_page(request):
    hls_url = request.GET.get('url', '')
    return render(request, 'stream/stream_page.html', {'hls_url': hls_url})

@login_required
def link_list(request):
    links = RTSPLink.objects.filter(user=request.user)
    return render(request, 'stream/link_list.html', {'links': links})

@login_required
def link_create(request):
    if request.method == 'POST':
        form = RTSPLinkForm(request.POST)
        if form.is_valid():
            rtsp_link = form.save(commit=False)
            rtsp_link.user = request.user
            rtsp_link.save()
            return redirect('link_list')
    else:
        form = RTSPLinkForm()
    return render(request, 'stream/link_form.html', {'form': form})

@login_required
def link_update(request, pk):
    rtsp_link = get_object_or_404(RTSPLink, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RTSPLinkForm(request.POST, instance=rtsp_link)
        if form.is_valid():
            form.save()
            return redirect('link_list')
    else:
        form = RTSPLinkForm(instance=rtsp_link)
    return render(request, 'stream/link_form.html', {'form': form})

@login_required
def link_delete(request, pk):
    rtsp_link = get_object_or_404(RTSPLink, pk=pk, user=request.user)
    if request.method == 'POST':
        rtsp_link.delete()
        return redirect('link_list')
    return render(request, 'stream/link_confirm_delete.html', {'link': rtsp_link})
