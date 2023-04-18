from django.shortcuts import render


def index(requests):
    return render(requests, 'index.html')


def boxes(requests):
    return render(requests, 'boxes.html')


def faq(requests):
    return render(requests, 'faq.html')


def my_rent(requests):
    return render(requests, 'my-rent.html')


def my_rent_empty(requests):
    return render(requests, 'my-rent-empty.html')
