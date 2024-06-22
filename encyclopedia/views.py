from django.shortcuts import render

from django.http import Http404

from django.http import HttpResponse

from . import util

from django import forms

from markdown2 import markdown

from django.shortcuts import redirect

import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_to_html(name):
    content = util.get_entry(name)
    if content is None:
        return None
    else:
        return markdown(content)

        

def page(request, name):
    if request.method == 'GET':
        content = md_to_html(name)
        if content == None:
            return render(request,'encyclopedia/error.html',{
                "name": name
            })
        else:
            return render(request, 'encyclopedia/converter.html', {
                "name": name, "lists": content
            })
    if request.method == 'POST':
        content = request.POST['text']
        name = request.POST['title']
        util.save_entry(name, content)
        new_content = md_to_html(name)
        return render(request, 'encyclopedia/converter.html',{
            "name": name, "lists":new_content
        })

def search(request):
    if request.method == "POST":
        entry = request.POST['q']
        content = md_to_html(entry)
        if content is not None:
            return render(request, 'encyclopedia/converter.html', {
                'lists': content
            })
        else:
            result = count(entry)
            if result is not None:
                return render(request, 'encyclopedia/list.html', {
                    "lists": result
                })
            else:
                return render(request, "encyclopedia/list.html", {
                    "lists": util.list_entries()
                })
    if request.method == 'GET':
        return render(request,'encyclopedia/index.html',{
            "entries": util.list_entries()
        })
            

            


def count(title):
    result = []
    list_of_entries = util.list_entries()
    for list in list_of_entries:
        if title.lower() in list.lower():
            result.append(list)
    if result:
        return result
    else:
        return None
    
def new_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html')
    if request.method == 'POST':
        new_entry = request.POST['q']
        content = request.POST['text']
        list_of_entries = util.list_entries()
        for entry in list_of_entries:
            if new_entry.lower() == entry.lower():
                return render(request, 'encyclopedia/wrong_entry.html',{
                    "name": new_entry
                })
        util.save_entry(new_entry, content)
        return redirect('name', name=new_entry)
    
def edit(request):
    if request.method == 'POST':
        name_of_entry = request.POST['edit_page']
        content = util.get_entry(name_of_entry)
        return render(request, 'encyclopedia/edit.html',{
            'content': content, 'name': name_of_entry
        })

def random_entry():
    entries = util.list_entries()
    random_entry = random.Random()
    return random_entry.choice(entries)


def random_page(request):
    if request.method == 'GET':
        page = random_entry()
        return redirect('name', name=page )






    
 



    

                


